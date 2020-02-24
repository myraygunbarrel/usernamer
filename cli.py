import logging.config
from usernamer.app import Usernamer
from config.base import CONFIG
import sys

level = logging.getLevelName(CONFIG['logging'])
logging.basicConfig(stream=sys.stdout, level=level)

application = Usernamer(CONFIG)

if __name__ == '__main__':
    application.run()
