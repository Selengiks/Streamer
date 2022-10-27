import config as cfg
from aiogram import md, types
from loguru import logger
from support.bots import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

logger.debug("Bot commands module loaded")

admin = cfg.admins

"""====================    FSM     ===================="""


class FSM(StatesGroup):
    primary = State()  # main state of the bot


"""====================    Main body     ===================="""


@dp.callback_query_handler(
    lambda c: c.data,
    state=FSM.primary,
    user_id=admin
)
async def process_callback_commands(callback_query: types.CallbackQuery):

    code = callback_query.data
    logger.debug(f'Нажата инлайн кнопка! code= {code}')

    if code == 'a':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == 'b':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/help':
        await bot.answer_callback_query(callback_query.id, text='/help')
        await help(callback_query.message)

    else:
        await bot.answer_callback_query(callback_query.id)


"""====================    Bot control layer     ===================="""


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
    logger.debug(result)
    await self.answer(result)


"""====================     Commands for all users     ===================="""


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    state="*",
    commands="start",
    user_id=admin
)
async def main_menu(message: types.Message):
    await FSM.primary.set()
    botinfo = await dp.bot.me
    result = f'{botinfo.full_name} [{md.hcode(f"@{botinfo.username}")}] на связи!\n\nMENU'
    logger.debug(result)
    await message.reply(result)


@dp.message_handler(
    state="*"
)
async def echo(message: types.Message):
    result = f'Неопознанная команда\n\n{message.text}'
    logger.debug(result)
    await message.answer(result)


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.primary,
    commands="sukablyatebuchayaklava"
)
async def del_keyb(message: types.Message):
    delete = types.ReplyKeyboardRemove(True)
    await message.answer(f'Done', reply_markup=delete)
