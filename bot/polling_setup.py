from loader import dp, bot
from cfg import logger
from .routers import routers


async def include_routers():
    dp.include_routers(*routers)


async def run_polling():
    await include_routers()
    logger.info('Bot active')
    await dp.start_polling(bot, skip_updates=True)
