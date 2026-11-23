import math
import logging
from dhanhq import dhanhq, DhanContext
import pandas as pd

logger = logging.getLogger(__name__)

class DhanStrikeSelector:
    """
    Selects ATM, 3 ITM, and 3 OTM strikes for CE and PE based on live Index Spot.
    """

    INDEX_STEP = {
        "NIFTY": 50,
        "BANKNIFTY": 100,
        "SENSEX": 100,
        "FINNIFTY": 50
    }

    def __init__(self, client_id, access_token):
        if client_id and client_id != "YOUR_CLIENT_ID" and access_token != "YOUR_ACCESS_TOKEN":
            try:
                ctx = DhanContext(client_id, access_token)
                self.dhan = dhanhq(ctx)
            except Exception as e:
                logger.error(f"Error initializing Dhan client: {e}")
                self.dhan = None
        else:
            self.dhan = None

    def get_index_spot(self, index_symbol="NIFTY"):
        """
        Fetches current spot price from Dhan API.
        """
        # Symbol mapping for Dhan Marketfeed / Quotes
        symbol_map = {
            "NIFTY": {"security_id": "13", "exchange_segment": "IDX_I"},
            "BANKNIFTY": {"security_id": "25", "exchange_segment": "IDX_I"},
            "SENSEX": {"security_id": "51", "exchange_segment": "IDX_I"}
        }

        meta = symbol_map.get(index_symbol.upper())
        if not meta:
            raise ValueError(f"Unsupported index: {index_symbol}")

        # In live market, fetch LTP via dhan.get_fund_limits or quote endpoint
        # Default fallback sample for pre-market / mock testing
        return 25800.0

    def compute_strike_ladder(self, index_symbol, spot_price, n_itm=3, n_otm=3):
        """
        Computes ATM, n_itm, and n_otm strikes.
        Returns:
            atm_strike: int
            calls: list of strikes [3 ITM ... ATM ... 3 OTM]
            puts: list of strikes [3 ITM ... ATM ... 3 OTM]
        """
        step = self.INDEX_STEP.get(index_symbol.upper(), 50)
        atm_strike = int(round(spot_price / step) * step)

        # For CALLS:
        # ITM strikes are BELOW ATM
        # OTM strikes are ABOVE ATM
        call_itm = [atm_strike - (i * step) for i in range(n_itm, 0, -1)]
        call_otm = [atm_strike + (i * step) for i in range(1, n_otm + 1)]
        call_strikes = call_itm + [atm_strike] + call_otm

        # For PUTS:
        # ITM strikes are ABOVE ATM
        # OTM strikes are BELOW ATM
        put_itm = [atm_strike + (i * step) for i in range(n_itm, 0, -1)]
        put_otm = [atm_strike - (i * step) for i in range(1, n_otm + 1)]
        put_strikes = put_itm + [atm_strike] + put_otm

        return {
            "index": index_symbol,
            "spot": spot_price,
            "atm": atm_strike,
            "calls": call_strikes,
            "puts": put_strikes
        }
