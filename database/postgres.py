from typing import Optional

from tortoise import Tortoise, exceptions

from cfg import logger
from .models import User, Const, GraphPage


class Postgres:
    def __init__(self, dsn: str):
        self.dsn = dsn

    async def init_orm(self):
        await Tortoise.init(
            db_url=self.dsn,
            modules={'models': ['database.models']},
        )
        await self.create_tables()
        # if the schemas aren`t generated, an error will occur
        logger.info('All necessary tables have been created')
        logger.info('Initialized Tortoise ORM')
        logger.info('Database active')

    @staticmethod
    async def close_orm():
        await Tortoise.close_connections()
        logger.info('Postgres connections was closed')

    @staticmethod
    async def create_tables():
        try:
            await Tortoise.generate_schemas()
        except exceptions.BaseORMException as e:
            logger.info(f'While generating schemas error has been occurred: {e.args}')
            raise e

    # @staticmethod
    # async def drop_tables():
    #     ...
    #     logger.info('Databases was dropped')

    # ---------- USER ----------
    @staticmethod
    async def insert_user_tg_data(user_id: int, full_name: str, username: str):
        user, created = await User.update_or_create(
            user_id=user_id,
            defaults={'full_name': full_name, 'username': username}
        )
        if created:
            logger.info('New user has been logged')
        return user

    @staticmethod
    async def get_user(user_id: int) -> Optional[User]:
        return await User.get_or_none(user_id=user_id)

    @staticmethod
    async def delete_user(user_id: int) -> bool:
        res = await User.filter(user_id=user_id).delete()
        return bool(res)

    # --------- CONST ----------
    @staticmethod
    async def insert_const(name: str, value: str):
        const, created = await Const.update_or_create(
            name=name,
            value=value
        )
        if created:
            logger.info('New const has been saved')
        return const

    @staticmethod
    async def get_const(name: str) -> Optional[Const]:
        return await Const.get_or_none(name=name)

    @staticmethod
    async def delete_const(name: str) -> bool:
        res = await Const.filter(name=name).delete()
        return bool(res)

    # --------- GRAPH ----------
    @staticmethod
    async def insert_graph_page(alias: str, graph_page: GraphPage):    # path: str, url: str, title: str, author_name: str, author_url: str):
        graph_page, created = await GraphPage.update_or_create(
            alias=alias,
            path=graph_page.path,
            url=graph_page.url,
            title=graph_page.title,
            author_name=graph_page.author_name,
            author_url=graph_page.author_url
        )
        if created:
            logger.info('New page has been saved')
        return graph_page

    @staticmethod
    async def get_graph_page(alias: str) -> Optional[GraphPage]:
        return await GraphPage.get_or_none(alias=alias)

    @staticmethod
    async def delete_graph_page(alias: str) -> bool:
        res = await GraphPage.filter(alias=alias).delete()
        return bool(res)