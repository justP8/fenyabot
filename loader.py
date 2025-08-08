from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from database import Postgres
from cfg import Config
from bot.middlewares import AccessMiddleware
from utils import Graph


config = Config.load()

bot = Bot(token=config.bot.token)#, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=MemoryStorage())
dp.update.outer_middleware(
    AccessMiddleware(config.bot.admins)
)

postgres = Postgres(config.postgres.dsn)
graph = Graph(config.graph.token)
