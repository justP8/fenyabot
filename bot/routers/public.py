from aiogram import Router, types, F
from loader import bot, postgres
from ..keyboards import get_rules_msg_ikb


__all__ = ['public_router']

public_router = Router()


@public_router.message(F.new_chat_members)
async def on_user_join(message: types.Message):
    print(f'{message=}')
    if message.new_chat_members[0].id == (await bot.me()).id:
        return
    builder = await get_rules_msg_ikb()
    if builder:
        await message.reply('Перед вступлением в чат обязательно прочитай наши правила', reply_markup=builder.as_markup())


@public_router.message(F.is_automatic_forward)
async def under_posts(message: types.Message):
    builder = await get_rules_msg_ikb()
    if builder:
        await message.reply('Перед вступлением в чат обязательно прочитай наши правила', reply_markup=builder.as_markup())
