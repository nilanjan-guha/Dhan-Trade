import logging
import datetime
from collections import defaultdict
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class OrderFlowFootprintEngine:
    """
    Computes real-time Footprint charts and Delta matrices from streaming ticks/depth.
    Tracks:
    - Bid Volume & Ask Volume per price level inside the candle.
    - Candle Delta = Ask Volume - Bid Volume.
    - Cumulative Volume Delta (CVD).
    - Point of Control (POC): Price with the highest traded volume.
    - Diagonal Bid/Ask Imbalances (Order Flow buying/selling pressure).
    """

    def __init__(self, candle_duration_sec=300, imbalance_ratio=2.5):
        self.candle_duration_sec = candle_duration_sec
        self.imbalance_ratio = imbalance_ratio
        self.current_candle_start = None
        self.candles = []
        self.cvd = 0.0  # Cumulative Volume Delta

        # Structure for active candle: price -> {'bid_vol': int, 'ask_vol': int}
        self.price_volume_ladder = defaultdict(lambda: {'bid_vol': 0, 'ask_vol': 0})
        self.candle_ohlc = {'open': None, 'high': None, 'low': None, 'close': None, 'volume': 0}

    def process_tick(self, tick_time, price, volume, last_trade_side):
        """
        Process a single trade tick.
        last_trade_side: 'BUY' (hit ask / aggressive buyer) or 'SELL' (hit bid / aggressive seller)
        """
        if self.current_candle_start is None:
            self.current_candle_start = tick_time
            self.candle_ohlc['open'] = price
            self.candle_ohlc['high'] = price
            self.candle_ohlc['low'] = price
            self.candle_ohlc['close'] = price

        # Check for candle roll over
        elapsed = (tick_time - self.current_candle_start).total_seconds()
        if elapsed >= self.candle_duration_sec:
            self._close_candle()
            self.current_candle_start = tick_time
            self.price_volume_ladder.clear()
            self.candle_ohlc = {'open': price, 'high': price, 'low': price, 'close': price, 'volume': 0}

        # Update OHLCV
        self.candle_ohlc['high'] = max(self.candle_ohlc['high'], price)
        self.candle_ohlc['low'] = min(self.candle_ohlc['low'], price)
        self.candle_ohlc['close'] = price
        self.candle_ohlc['volume'] += volume

        # Update Bid / Ask ladder
        if last_trade_side == 'BUY':
            self.price_volume_ladder[price]['ask_vol'] += volume
            self.cvd += volume
        else:
            self.price_volume_ladder[price]['bid_vol'] += volume
            self.cvd -= volume

    def _close_candle(self):
        """Finalizes the candle and computes Footprint metrics."""
        total_ask = sum(data['ask_vol'] for data in self.price_volume_ladder.values())
        total_bid = sum(data['bid_vol'] for data in self.price_volume_ladder.values())
        candle_delta = total_ask - total_bid

        # Calculate Point of Control (POC)
        poc_price = None
        max_vol = -1
        for p, data in self.price_volume_ladder.items():
            tot = data['bid_vol'] + data['ask_vol']
            if tot > max_vol:
                max_vol = tot
                poc_price = p

        # Check for stacked buying or selling imbalances
        buying_imbalances = []
        selling_imbalances = []
        sorted_prices = sorted(self.price_volume_ladder.keys())

        # Diagonal imbalance check
        for i in range(len(sorted_prices) - 1):
            curr_p = sorted_prices[i]
            next_p = sorted_prices[i + 1]
            ask_v = self.price_volume_ladder[next_p]['ask_vol']
            bid_v = self.price_volume_ladder[curr_p]['bid_vol']

            if bid_v > 0 and (ask_v / bid_v) >= self.imbalance_ratio:
                buying_imbalances.append(next_p)
            elif ask_v > 0 and (bid_v / ask_v) >= self.imbalance_ratio:
                selling_imbalances.append(curr_p)

        candle_summary = {
            'start_time': self.current_candle_start,
            'open': self.candle_ohlc['open'],
            'high': self.candle_ohlc['high'],
            'low': self.candle_ohlc['low'],
            'close': self.candle_ohlc['close'],
            'volume': self.candle_ohlc['volume'],
            'delta': candle_delta,
            'cvd': self.cvd,
            'poc': poc_price,
            'buying_imbalances': len(buying_imbalances),
            'selling_imbalances': len(selling_imbalances),
            'ladder': dict(self.price_volume_ladder)
        }
        self.candles.append(candle_summary)
        return candle_summary


class SMCTrendAnalyzer:
    """
    Identifies Smart Money Concepts (SMC) on the Index / Option:
    - Break of Structure (BOS)
    - Change of Character (CHoCH)
    - Fair Value Gap (FVG)
    - Order Blocks
    """

    @staticmethod
    def identify_fvg(df):
        """
        Detects Bullish & Bearish Fair Value Gaps (FVG) on a 3-candle sequence:
        - Bullish FVG: Candle 1 High < Candle 3 Low (Gap between High[0] and Low[2])
        - Bearish FVG: Candle 1 Low > Candle 3 High (Gap between Low[0] and High[2])
        """
        fvgs = []
        if len(df) < 3:
            return fvgs

        for i in range(2, len(df)):
            c1_high = df.iloc[i - 2]['high']
            c1_low = df.iloc[i - 2]['low']
            c3_high = df.iloc[i]['high']
            c3_low = df.iloc[i]['low']

            if c3_low > c1_high:
                fvgs.append({
                    'type': 'BULLISH_FVG',
                    'bottom': c1_high,
                    'top': c3_low,
                    'time': df.iloc[i]['datetime'] if 'datetime' in df.columns else i
                })
            elif c3_high < c1_low:
                fvgs.append({
                    'type': 'BEARISH_FVG',
                    'top': c1_low,
                    'bottom': c3_high,
                    'time': df.iloc[i]['datetime'] if 'datetime' in df.columns else i
                })
        return fvgs

    @staticmethod
    def detect_market_structure(df):
        """
        Detects Higher Highs / Higher Lows (Uptrend) vs Lower Highs / Lower Lows (Downtrend)
        Returns: 'BULLISH', 'BEARISH', or 'SIDEWAYS'
        """
        if len(df) < 10:
            return 'SIDEWAYS'

        recent_highs = df['high'].rolling(window=3, center=True).apply(
            lambda x: x.iloc[1] if (x.iloc[1] > x.iloc[0] and x.iloc[1] > x.iloc[2]) else np.nan
        ).dropna().tail(2)

        recent_lows = df['low'].rolling(window=3, center=True).apply(
            lambda x: x.iloc[1] if (x.iloc[1] < x.iloc[0] and x.iloc[1] < x.iloc[2]) else np.nan
        ).dropna().tail(2)

        if len(recent_highs) >= 2 and len(recent_lows) >= 2:
            if recent_highs.iloc[-1] > recent_highs.iloc[-2] and recent_lows.iloc[-1] > recent_lows.iloc[-2]:
                return 'BULLISH'
            elif recent_highs.iloc[-1] < recent_highs.iloc[-2] and recent_lows.iloc[-1] < recent_lows.iloc[-2]:
                return 'BEARISH'

        return 'SIDEWAYS'
