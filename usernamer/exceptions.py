from aiohttp import web, web_exceptions
from asyncio import TimeoutError
import logging
from asyncpg.exceptions import UniqueViolationError

logger = logging.getLogger('Telemetry-API')


class AddUserError(Exception):
    pass


class NumbersClientError(Exception):
    pass


class ValidationError(Exception):
    pass


@web.middleware
async def error_middleware(request, handler):
    try:
        result = await handler(request)
    except TimeoutError:
        return web.json_response(dict(error='NumbersApi Timeout'), status=408)
    except UniqueViolationError as e:
        return web.json_response(dict(error=str(e)), status=409)
    except web.HTTPNotFound:
        return web.json_response(dict(error='Not found'), status=404)
    except (web_exceptions.HTTPBadRequest, ValidationError) as e:
        return web.json_response(dict(error=str(e)), status=400)
    except AddUserError as e:
        return web.json_response(dict(error=str(e)), status=502)
    except NumbersClientError as e:
        return web.json_response(dict(error='NumbersApi is unavailable now'), status=503)
    if isinstance(result, (dict, list)):
        return web.json_response(result, status=200)
    return result


async def prepare_cors(request, response):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Request-Method': 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    }
    response.headers.update(headers)
