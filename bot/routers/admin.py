from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from database.models import GraphPage
from ..keyboards import get_admin_start_ikb, confirmation_ikb
from ..states import MyStates
from loader import postgres, graph


__all__ = ['admin_router']

admin_router = Router()


@admin_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    page = await postgres.get_graph_page('rules')
    builder = await get_admin_start_ikb()
    if page:
        await state.update_data(page=page)
        await message.answer(f'Сейчас установлены следующие правила: {page.url}', reply_markup=builder.as_markup())
    else:
        await message.answer('У вас не установлены правила', reply_markup=builder.as_markup())


@admin_router.callback_query(F.data == 'set rules')
async def set_rules(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(MyStates.setting_rules)
    await callback_query.message.answer('Напишите правила в виде простого сообщения, можно использовать форматирование - оно сохранится в конечном варианте.')

@admin_router.message(MyStates.setting_rules)
async def setting_rules(message: types.Message, state: FSMContext):
    mte = await message.answer('Секундочку, подготавливаем страницу с вашими правилами чата...')
    page = await graph.create_page('rules', message.html_text)
    await state.update_data(page=page)
    await mte.edit_text(f'Ваша страница готова: {page.url}.\n'
                        f'Подтверждаете изменение правил?', reply_markup=confirmation_ikb.as_markup())
    await state.set_state(MyStates.rules_confirmation)


@admin_router.callback_query(MyStates.rules_confirmation)
async def rules_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    page = await state.get_value('page')
    match callback_query.data:
        case 'confirm':
            await postgres.insert_graph_page('rules', page)
            await callback_query.message.edit_text('Новые правила установлены')
            await state.clear()
        case 'reject':
            await callback_query.message.edit_text(f'Отправьте новое сообщение или измените правила вручную перейдя сначала по первой ссылке: {await graph.get_auth_url()}\n'
                                                   f'а после по второй: {page.url}\n'
                                                   f'Для отмены нажмите на кнопку снизу\n\n'
                                                   f'ВАЖНО! Если вы изменили правила вручную, то нажмите на кнопку снизу', reply_markup=confirmation_ikb.as_markup())
    await state.set_state(MyStates.resetting_rules)


@admin_router.callback_query(MyStates.resetting_rules)
async def resetting_rules_cbq(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    match callback_query.data:
        case 'confirm':
            page = await state.get_value('page')
            await postgres.insert_graph_page('rules', page)
            await callback_query.message.edit_text('Новые правила установлены')
            await state.clear()
        case 'reject':
            await callback_query.message.edit_text('Отменено')
            await state.clear()


@admin_router.message(MyStates.resetting_rules)
async def resetting_rules_msg(message: types.Message, state: FSMContext):
    mte = await message.answer('Секундочку, переподготавливаем страницу с вашими правилами чата...')
    path_to_page = (await state.get_value('page')).path
    page = await graph.edit_page('rules', path_to_page, message.html_text)
    await state.update_data(page=page)
    await mte.edit_text(f'Ваша страница готова: {page.url}.\n'
                        f'Подтверждаете изменение правил?', reply_markup=confirmation_ikb.as_markup())
    await state.set_state(MyStates.rules_confirmation)


@admin_router.callback_query(F.data == 'change rules')
async def change_rules(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    page = await state.get_value('page')
    await callback_query.message.answer(f'Отправьте сообщение c новыми правилами или измените их вручную перейдя сначала по первой ссылке: {await graph.get_auth_url()}\n'
                                        f'а после по второй: {page.url}\n'
                                        f'Для отмены нажмите на кнопку снизу\n\n'
                                        f'ВАЖНО! Если вы изменили правила вручную, то нажмите на кнопку снизу', reply_markup=confirmation_ikb.as_markup())
    await state.set_state(MyStates.resetting_rules)