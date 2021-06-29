from typing import List, Any
import logging

from binance.websocket.spot.websocket_client import SpotWebsocketClient as WS

logger = logging.getLogger(__name__)

class Kline:
    """
    Candle/Kline class. Connects to Binance and downloads candle data
    """
    def __init__(self, symbols: List[str], interval: str, callback: Any):
        """
        Kline class constructor.

        :param symbols: Tuple of symbols to monitor (consult https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams).
        :param interval: Candle interval
        :param callback: Callback function to use on each update
        """
        self.callback = callback
        self.symbols = symbols
        self.interval = interval

    def run(self) -> WS:
        """
        Starts WebSocket connection to Binance

        :return: Binance WS connection handle
        """
        logger.info("Starting Binance WS connection")

        ws_client = WS()
        ws_client.start()

        [ws_client.kline(symbol=symbol,
                         id=symbol_id,
                         interval=self.interval,
                         callback=self.callback, )
         for symbol_id, symbol
         in enumerate(self.symbols)]

        return ws_client
