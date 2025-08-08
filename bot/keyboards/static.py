from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


__all__ = ['confirmation_ikb']

confirmation_ikb = InlineKeyboardBuilder().add(
    InlineKeyboardButton(text='✅', callback_data='confirm'),
    InlineKeyboardButton(text='❌', callback_data='reject')
)
