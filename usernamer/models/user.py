from usernamer.db import db
from sqlalchemy import select
from aiohttp import web


class BaseTable(db.Model):
    created_at = db.Column(
        db.TIMESTAMP(),
        server_default=db.text('statement_timestamp()'),
        nullable=False,
        comment='Дата создания',
    )

    updated_at = db.Column(
        db.TIMESTAMP(),
        server_default=db.text('statement_timestamp()'),
        onupdate=db.func.statement_timestamp(),
        nullable=False,
        comment='Дата модификации',
    )


class UserTable(BaseTable):
    __tablename__ = 'user'

    id = db.Column(db.INT(), autoincrement=True, primary_key=True, nullable=False)
    first_name = db.Column(db.VARCHAR(), comment='Имя')
    last_name = db.Column(db.VARCHAR(), nullable=False, comment='Фамилия')
    date_of_birth = db.Column(db.DATE(), comment='Дата рождения')
    date_fact = db.Column(db.VARCHAR(), comment='Интересный факт о дне рождения')
    year_fact = db.Column(db.VARCHAR(), comment='Интересный факт о годе рождения')

    @classmethod
    async def get_user(cls, user_id):
        user = await UserTable.get(user_id)
        if not user:
            raise web.HTTPNotFound
        return user

    @classmethod
    async def get_report(cls, intervals):
        data = await select(cls).where(
            cls.created_at.between(
                intervals['added_from'],
                intervals['added_to']
            )
        ).gino.all()
        if not data:
            raise web.HTTPNotFound
        return data
