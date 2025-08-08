from contextlib import asynccontextmanager
from typing import Dict

import uvicorn
from aiogram import types
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from cfg import logger, WEBAPP_HOST, WEBHOOK_PATH, WEBAPP_PORT
from loader import bot, dp
from .routers import routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await bot.set_webhook(url=WEBHOOK_PATH, allowed_updates=dp.resolve_used_update_types(), drop_pending_updates=True)
        await include_routers()
        logger.info('Bot active')
        yield
        await bot.delete_webhook()
    except Exception as e:
        logger.error(f'Во время запуска бота произошла ошибка: {e}')


app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


async def include_routers():
    dp.include_routers(*routers)


# Answering on webhook
@app.post('/webhook')
async def webhooks(request: Request) -> Dict:
    update = types.Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return {'status': 'Webhook deleted'}


# If the user goes to WEBHOOK_PATH
@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request) -> str:
    return 'GET OUT OF HERE'

# main bot function
async def run_webhook():
    config = uvicorn.Config(app, port=WEBAPP_PORT, host=WEBAPP_HOST)
    server = uvicorn.Server(config)
    return await server.serve()
