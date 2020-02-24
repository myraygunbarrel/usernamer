import multiprocessing

from .base import CONFIG


bind = "{}:{}".format(CONFIG['app']['host'], CONFIG['app']['port'])
worker_class = "aiohttp.GunicornWebWorker"
workers = multiprocessing.cpu_count() * 2 + 1
