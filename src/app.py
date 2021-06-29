from time import sleep
import logging

from src.kline import Kline
from src.moving_average_logger import MovingAverageLogger

logger = logging.getLogger(__name__)

def run():
    """
    Runs the program
    :return:
    """

    malogger = MovingAverageLogger(window_size=5)

    kline = Kline(symbols=["btcusdt", "ethusdt", "bnbbtc"],
                  interval="1m",
                  callback=malogger.process_payload)

    ws_client = kline.run()

    try:
        while True:
            sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Closing Binance WS conenction")
        ws_client.stop()
        raise
