from aiohttp import web, ClientSession, ClientTimeout
from .clients.numbers import NumbersClient
from .exceptions import error_middleware, prepare_cors
from usernamer.api.v1.user import IndexView, UserView, GetUserView
from usernamer.api.v1.reports import ReporterView
from usernamer.db import db
from aiohttp_apispec import setup_aiohttp_apispec
import logging
import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from aiohttp_apispec import validation_middleware

logger = logging.getLogger(__name__)

CLIENTS = [('numbers', NumbersClient)]


class Usernamer:
    def __init__(self, config):
        self.config = config
        self.db = db
        self.app = self.get_app()

    def get_app(self) -> web.Application:
        sentry_sdk.init(dsn=self.config['sentry_dsn'],
                        integrations=[AioHttpIntegration(), SqlalchemyIntegration()])
        app = web.Application(middlewares=[
            error_middleware,
            validation_middleware,
            self.db])
        self.init_clients(app)
        self.init_postgres(app)
        self.init_routes(app)
        app.on_response_prepare.append(prepare_cors)
        app.on_shutdown.append(self.stop)
        return app

    def init_clients(self, app: web.Application):
        app['http_client'] = ClientSession(timeout=ClientTimeout(total=self.config['timeout']))
        app['services'] = {}
        for name, client in CLIENTS:
            app['services'][name] = client(session=app['http_client'], config=self.config)
            logger.info(f'{name} client is ready')

    def init_postgres(self, app: web.Application):
        self.db.init_app(app, config=self.config['postgres'])
        logger.info(f"Connected to database: {self.config['postgres']}")

    def init_routes(self, app: web.Application):
        app.add_routes([
            web.view('/', IndexView),
            web.view('/api/v1/user', UserView),
            web.view('/api/v1/user/{user_id}', GetUserView),
            web.view('/api/v1/reports', ReporterView)
        ])
        setup_aiohttp_apispec(
            app=app,
            **self.config['swagger']
        )

    def run(self):
        web.run_app(self.app, **self.config['app'])

    @staticmethod
    async def stop(app: web.Application):
        await app['http_client'].close()
