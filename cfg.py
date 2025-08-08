from abc import abstractmethod, ABC
from dataclasses import dataclass

from environs import Env
from loguru import logger
from telegraph import Telegraph

logger.add(sink='logs/info.log',
           level='INFO',
           format='{time} | {name}:{function}:{line} | {message}',
           rotation='1 MB',
           compression='zip')

WEBAPP_HOST, WEBAPP_PORT = 'localhost', 8080
WEBHOOK_PATH = 'https://l1bqbn-2a01-540-a9d8-5600-dc46-649d-22a0-b1e9.ru.tuna.am' + '/webhook'


class BaseDataclass(ABC):
    @staticmethod
    @abstractmethod
    def from_env(env: Env):
        ...

    def get_values(self):
        return tuple(self.__dict__.values())


@dataclass
class Bot(BaseDataclass):
    """
    Some data for bot
    """
    token: str
    admins: list[str]

    @staticmethod
    def from_env(env: Env) -> "Bot":
        token = env.str('BOT_TOKEN')
        admins = env.list('ADMINS')
        return Bot(token, admins)


@dataclass
class Postgres(BaseDataclass):
    """
    Data for database connection
    """
    database: str
    user: str
    password: str
    host: str
    port: int
    dsn: str
    scheduler_dsn: str

    @staticmethod
    def from_env(env: Env) -> "Postgres":
        database = env.str('DATABASE')
        user = env.str('USER')
        password = env.str('PASSWORD')
        host = env.str('HOST')
        port = env.int('PORT')
        dsn = f'postgres://{user}:{password}@{host}:{port}/{database}'
        scheduler_dsn = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'
        return Postgres(database, user, password, host, port, dsn, scheduler_dsn)


@dataclass
class GraphData(BaseDataclass):
    """
    Data of current telegraph account
    """
    token: str

    def from_env(env: Env) -> "GraphData":
        # {'short_name': 'Fenya',
        # 'author_name': '',
        # 'author_url': '',
        # 'access_token': '33804368245640184c6ba66f773a7a5e744ce2562273dc97dadc2ef9a0d3',
        # 'auth_url': 'https://edit.telegra.ph/auth/H3A9SP4H4uQrLmLET8Q88MLGZGtjJfsph0w7PAOR4E'}
        token = env.str('GRAPH_TOKEN')
        return GraphData(token)


@dataclass
class Config:
    """
    All data from env
    """
    bot: Bot
    postgres: Postgres
    graph: GraphData

    @staticmethod
    def load() -> "Config":
        env = Env()
        env.read_env()
        return Config(bot=Bot.from_env(env),
                      postgres=Postgres.from_env(env),
                      graph=GraphData.from_env(env))
