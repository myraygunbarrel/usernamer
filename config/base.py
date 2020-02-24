import os
from usernamer import __version__

CONFIG = {
    'app': {
        'host': os.environ.get('APP_HOST'),
        'port': os.environ.get('APP_PORT')
    },
    'timeout': 15,
    'postgres': {
        'user': os.environ.get('POSTGRES_USER'),
        'database': os.environ.get('POSTGRES_NAME'),
        'host': os.environ.get('POSTGRES_HOST'),
        'port': os.environ.get('POSTGRES_EXTERNAL_PORT'),
        'password': os.environ.get('POSTGRES_PASSWORD')
    },
    'swagger': {
        'swagger_path': '/api',
        'title': 'Usernamer',
        'url': "/api/docs/swagger.json",
        'version': __version__
    },
    'services': {
        'numbers': {
            'api_url': 'http://numbersapi.com/'
        }
    },
    'sentry_dsn': os.environ.get('SENTRY_DSN'),
    'logging': os.environ.get('LOG_LEVEL')
}
