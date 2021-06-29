import sys
import logging
logging.basicConfig(level=logging.INFO, format = '[%(asctime)s] %(levelname)s %(message)s')

from src import app

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        app.run()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stopping program")
        sys.exit()
