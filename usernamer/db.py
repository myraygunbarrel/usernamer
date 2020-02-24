from gino.ext.aiohttp import Gino
from sqlalchemy.schema import MetaData

db: MetaData = Gino()
