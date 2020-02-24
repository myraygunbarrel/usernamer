from aiohttp import web
from usernamer.exceptions import AddUserError
from usernamer.models.user import UserTable
from asyncpg import PostgresError
from aiohttp_apispec import docs, json_schema, match_info_schema
from usernamer.schemas.user import UserBody, UserGetPath, UserUpdateBody, UserSchema


class IndexView(web.View):
    async def get(self):
        raise web.HTTPFound('/api')


class UserView(web.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.numbers_client = self.request.app['services']['numbers']

    @docs(
        tags=["Users"],
        summary="Add user",
        description="Добавить нового юзера",
    )
    @json_schema(UserBody)
    async def post(self):
        data = self.request['json']
        fun_facts = await self.numbers_client.get_data(
            timestamp=data['date_of_birth']
        )
        data.update(fun_facts)
        try:
            await UserTable.create(**data)
        except PostgresError as e:
            raise AddUserError(e)

        return web.Response(status=201)

    @docs(
        tags=["Users"],
        summary="Update user fun-facts",
        description="Сгенерить новые интересные факты",
    )
    @json_schema(UserUpdateBody)
    async def put(self):
        data = self.request['json']
        user = await UserTable.get_user(data['id'])
        fun_facts = await self.numbers_client.get_data(
            timestamp=user.date_of_birth,
            year_fact=data['year_fact'],
            date_fact=data['date_fact']
        )
        await user.update(**fun_facts).apply()

        return web.Response(status=204)


class GetUserView(web.View):
    @docs(
        tags=["Users"],
        summary="Get user",
        description="Получить карточку юзера",
    )
    @match_info_schema(UserGetPath)
    async def get(self):
        user = await UserTable.get_user(self.request['match_info']['user_id'])
        return UserSchema().dump(user)





