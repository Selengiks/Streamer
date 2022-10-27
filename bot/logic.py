import config as cfg
from aiogram import md, types
from loguru import logger
from support.bots import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logger.debug("Bot commands module loaded")

admin = cfg.admins

"""====================    FSM     ===================="""


class FSM(StatesGroup):
    primary = State()  # main state of the bot

    """Add user logic"""
    add_user_step_user = State()
    add_user_step_source = State()
    add_user_step_sub = State()
    add_user_step_teamlead = State()

    """Delete user logic"""
    del_user_step_user = State()

    """Add user sub logic"""
    add_sub_step_user = State()
    add_sub_step_source = State()
    add_sub_step_sub = State()

    """Add user campaign logic"""
    add_camp_step_user = State()
    add_camp_step_app = State()
    add_camp_step_sub = State()

    """Open organic logic"""
    open_org_step_user = State()
    open_org_step_app = State()

    """Close organic logic"""
    close_org_step_user = State()
    close_org_step_app = State()

    "Allow organic edit logic"
    allow_edit_org_step_user = State()
    allow_edit_org_step_app = State()

    """Deny organic edit logic"""
    deny_edit_org_step_user = State()
    deny_edit_org_step_app = State()

    """Check user visibility logic"""
    check_user_visib_step_user = State()


"""====================    Keyboard     ===================="""

add_user_key = InlineKeyboardButton('Add user', callback_data='/add_user')
del_user_key = InlineKeyboardButton('Delete user', callback_data='/del_user')
add_user_sub_key = InlineKeyboardButton('Add user sub', callback_data='/add_sub')
add_user_camp_key = InlineKeyboardButton('Add user campaign', callback_data='/add_camp')
open_org_key = InlineKeyboardButton('Open organic', callback_data='/open_org')
close_org_key = InlineKeyboardButton('Close organic', callback_data='/close_org')
allow_org_edit_key = InlineKeyboardButton('Accept organic edit', callback_data='/a_org_edit')
deny_org_edit_key = InlineKeyboardButton('Deny organic edit', callback_data='/d_org_edit')
open_camp_visib_key = InlineKeyboardButton('Open campaign visibility', callback_data='/o_camp_vis')
close_camp_visib_key = InlineKeyboardButton('Close campaign visibility', callback_data='/c_camp_vis')
check_user_visib_key = InlineKeyboardButton('Check user visibility', callback_data='/check_user_vis')
keyboard = InlineKeyboardMarkup(row_width=2).add(add_user_key, del_user_key, add_user_sub_key, add_user_camp_key,
                                                 open_org_key, close_org_key, allow_org_edit_key, deny_org_edit_key,
                                                 open_camp_visib_key, close_camp_visib_key, check_user_visib_key)

help_key = InlineKeyboardButton('Help', callback_data='/help')
keyboard.add(help_key)

"""====================    Main body     ===================="""


@dp.callback_query_handler(
    lambda c: c.data,
    state=FSM.primary,
    user_id=admin
)
async def process_callback_commands(callback_query: types.CallbackQuery):
    code = callback_query.data
    logger.debug(f'Pressed inline button. Code= {code}')

    if code == '/add_user':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/del_user':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/add_sub':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/add_camp':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/open_org':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/close_org':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/a_org_edit':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/d_org_edit':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/o_camp_vis':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/c_camp_vis':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/check_user_vis':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/help':
        await bot.answer_callback_query(callback_query.id, text='/help')
        await help(callback_query.message)

    else:
        await bot.answer_callback_query(callback_query.id)


"""====================    Bot control layer     ===================="""


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    state="*",
    commands="start",
    user_id=admin
)
async def main_menu(message: types.Message):
    await FSM.primary.set()
    botinfo = await dp.bot.me
    result = f'{botinfo.full_name} [{md.hcode(f"@{botinfo.username}")}] on line!'
    logger.info(result)
    await message.reply(result, reply_markup=keyboard)


@dp.message_handler(
    state='*',
    commands='cancel',
    user_id=admin
)
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.debug(f'/cancel executed. Return to primary state')
    await FSM.primary.set()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state="*",
    commands="help"
)
async def help(self: types.Message):
    result = f"HELP"
    logger.info(result)
    await self.answer(result)


@dp.message_handler(
    state="*"
)
async def echo(message: types.Message):
    result = f'Unrecognized command\n\n{message.text}'
    logger.info(result)
    await message.answer(result)


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.primary,
    commands="sukablyatebuchayaklava"
)
async def del_keyb(message: types.Message):
    delete = types.ReplyKeyboardRemove(True)
    await message.answer(f'Done', reply_markup=delete)
