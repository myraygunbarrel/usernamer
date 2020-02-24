from abc import ABC, abstractmethod
import aiohttp
import json
import logging
from usernamer.exceptions import ValidationError, NumbersClientError

logger = logging.getLogger(__name__)


class AbstractClient(ABC):
    @abstractmethod
    def __init__(self, session, config):
        self._session = session
        self.url = config['services'][str(self)]['api_url']

    def __str__(self):
        return self.__class__.__name__.lower().replace('client', '')

    async def _request(self, uri, **kwargs):
        url = self.url + uri
        async with self._session.get(url, params=kwargs) as resp:
            text = await resp.text()
            logger.info(self.form_log_message(resp, text, **kwargs))

            try:
                ans = await resp.json()
            except (json.decoder.JSONDecodeError,
                    aiohttp.ContentTypeError) as e:
                raise NumbersClientError(text, resp.status)

            if resp.status == 400:
                raise ValidationError(ans, resp.status)
            return ans

    def form_log_message(self, resp, answer, **kwargs):
        message = f'\n{str(self)} API request:\n'\
                  f'{resp.method} {resp.url}\n'\
                  f'Data:\n{kwargs}\n'\
                  f'HTTP Code: {resp.status} {resp.reason}\n'\
                  f'Response:\n{answer}'
        return message

