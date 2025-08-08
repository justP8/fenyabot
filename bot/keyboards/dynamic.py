from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from loader import postgres


__all__ = ['get_admin_start_ikb', 'get_rules_msg_ikb']


async def get_admin_start_ikb() -> InlineKeyboardBuilder:
    admin_start_ikb = InlineKeyboardBuilder()
    page = await postgres.get_graph_page('rules')
    if page:
        admin_start_ikb.button(text='Изменить правила', callback_data='change rules')
    else:
        admin_start_ikb.button(text='Установить правила', callback_data='set rules')
    return admin_start_ikb


async def get_rules_msg_ikb() -> InlineKeyboardBuilder | bool:
    rules_msg_ikb = InlineKeyboardBuilder()
    page = await postgres.get_graph_page('rules')
    if page:
        rules_msg_ikb.button(text='Правила чата', url=page.url)
        return rules_msg_ikb
    else:
        return False
