import asyncio
from .base import AbstractClient
from aiohttp import ClientConnectorError
from datetime import datetime
from usernamer.exceptions import NumbersClientError
from collections import ChainMap


class NumbersClient(AbstractClient):
    def __init__(self, session, config):
        super().__init__(session, config)

    async def get_data(self,
                       timestamp: datetime,
                       year_fact=True,
                       date_fact=True):
        tasks = []
        if year_fact:
            tasks.append(self.get_year_fact(timestamp))
        if date_fact:
            tasks.append(self.get_date_fact(timestamp))
        try:
            result = await asyncio.gather(*tasks)
        except ClientConnectorError as e:
            raise NumbersClientError(e)
        return dict(ChainMap(*result))

    async def get_year_fact(self, timestamp: datetime):
        data = await self._request(uri=f'{timestamp.year}/year?json')
        return {'year_fact': data.get('text')}

    async def get_date_fact(self, timestamp: datetime):
        data = await self._request(uri=f'{timestamp.month}/{timestamp.day}/date?json')
        return {'date_fact': data.get('text')}
