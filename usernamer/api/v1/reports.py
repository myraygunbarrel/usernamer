from aiohttp import web
from aiohttp_apispec import docs, querystring_schema
from usernamer.models.user import UserTable
from usernamer.reporter import Reporter
from usernamer.schemas.reporter import ReporterQuery, UserReporterSchema

user_row_schema = UserReporterSchema()


class ReporterView(web.View):
    @docs(
        tags=["CSV-Reports"],
        summary="Get users",
        description="Получить таблицу юзеров",
    )
    @querystring_schema(ReporterQuery)
    async def get(self):
        intervals = self.request['querystring']
        data = await UserTable.get_report(intervals)
        data = [user_row_schema.dump(item) for item in data]
        reporter = Reporter(data)
        return web.Response(
            body=reporter.csv,
            headers={
                'Content-Disposition': f'attachment; filename={reporter.filename}',
                'Content-Type': 'text / csv'
            },
            status=200
        )
