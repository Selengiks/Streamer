import config as cfg
from aiogram import md, types
from loguru import logger
from support.bots import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import bot.crm_api as capi

logger.debug("Bot commands module loaded")

admin = cfg.admins

"""====================    FSM     ===================="""


class FSM(StatesGroup):
    primary = State()  # main state of the bot

    find_user = State()

    """Add user logic"""
    add_user_step_user = State()
    add_user_step_source = State()
    add_user_step_sub = State()
    add_user_step_teamlead = State()

    """Delete user logic"""
    del_user_step_user = State()

    """Add user sub logic"""
    add_sub_step_user = State()  #
    add_sub_step_source = State()  #
    add_sub_step_sub = State()  #

    """Add user campaign logic"""
    add_camp_step_user = State()
    add_camp_step_app = State()
    add_camp_step_sub = State()

    """Open organic logic"""
    open_org_step_user = State()  #
    open_org_step_app = State()  #

    """Close organic logic"""
    close_org_step_user = State()  #
    close_org_step_app = State()  #

    "Allow organic edit logic"
    allow_edit_org_step_user = State()  #
    allow_edit_org_step_app = State()  #

    """Check user visibility logic"""
    check_user_visib_step_user = State()

    temp_state = State()


"""====================    MENU Keyboard     ===================="""

add_user_key = InlineKeyboardButton('Add user', callback_data='/add_user')
del_user_key = InlineKeyboardButton('Delete user', callback_data='/del_user')
add_user_sub_key = InlineKeyboardButton('Add user sub', callback_data='/add_sub')
add_user_camp_key = InlineKeyboardButton('Add user campaign', callback_data='/add_camp')
open_org_key = InlineKeyboardButton('Open organic', callback_data='/open_org')
close_org_key = InlineKeyboardButton('Close organic', callback_data='/close_org')
allow_org_edit_key = InlineKeyboardButton('Accept organic edit', callback_data='/a_org_edit')
open_camp_visib_key = InlineKeyboardButton('Open campaign visibility', callback_data='/o_camp_vis')
close_camp_visib_key = InlineKeyboardButton('Close campaign visibility', callback_data='/c_camp_vis')
check_user_visib_key = InlineKeyboardButton('Check user visibility', callback_data='/check_user_vis')
keyboard = InlineKeyboardMarkup(row_width=2).add(add_user_key, del_user_key, add_user_sub_key, add_user_camp_key,
                                                 open_org_key, close_org_key, allow_org_edit_key, open_camp_visib_key,
                                                 close_camp_visib_key, check_user_visib_key)

help_key = InlineKeyboardButton('Help', callback_data='/help')
keyboard.add(help_key)

"""====================    Userlist keyboard     ===================="""


def user_search(name_to_search: str):
    userdata = capi.get_users().get("data")
    users = {}
    for v in userdata.values():
        users[v["id"]] = {"user": v["login"]}

    data = []
    for k, v in users.items():
        data.append(v['user'])
    if result := tuple(app_name for app_name in data if name_to_search.lower() in app_name.lower()):
        return result

    else:
        def is_any_serched_word_in_string(string: str):
            return any(True for word in name_to_search.lower().split() if word in string.lower())

        return tuple(filter(is_any_serched_word_in_string, data))


users_cb = CallbackData('user', 'id', 'action')  # user:<id>:<action>   -> types.InlineKeyboardMarkup


def get_users_list(user):
    users = user_search(user)
    markup = types.InlineKeyboardMarkup()
    count = 1
    for i in users:
        markup.add(
            types.InlineKeyboardButton(
                i,
                callback_data=users_cb.new(id=i, action='choose')),
        )
        count += 1
    return markup


"""====================    Main body     ===================="""

logins = []
sources = []
subs = []
bundles = []


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
        await FSM.find_user.set()
        FSM.temp_state = FSM.add_sub_step_user
        await bot.send_message(callback_query.from_user.id, text="Enter to whom to add")

    elif code == '/add_camp':
        await bot.answer_callback_query(callback_query.id, text='Not implemented yet!', show_alert=True)

    elif code == '/open_org':
        await FSM.find_user.set()
        FSM.temp_state = FSM.open_org_step_user
        await bot.send_message(callback_query.from_user.id, text="Enter to whom to open")

    elif code == '/close_org':
        await FSM.find_user.set()
        FSM.temp_state = FSM.close_org_step_user
        await bot.send_message(callback_query.from_user.id, text="Enter to whom to close")

    elif code == '/a_org_edit':
        await FSM.find_user.set()
        FSM.temp_state = FSM.allow_edit_org_step_user
        await bot.send_message(callback_query.from_user.id, text="Enter to whom to allow")

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
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.find_user
)
async def find_user(self: types.Message, state: FSMContext):
    try:
        logger.info("find_user")
        await self.reply('Type again one of the names you are looking for:\n', reply_markup=get_users_list(self.text))
        await FSM.temp_state.set()

    except Exception as e:
        out = f'find_user, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.add_sub_step_user
)
async def add_sub_step_user(self: types.Message, state: FSMContext):
    try:
        logger.info("add_sub_step_user")
        logins.append(self.text)
        await FSM.add_sub_step_source.set()
        await self.answer(f'Enter source for target sub')

    except Exception as e:
        out = f'add_sub_step_user, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.add_sub_step_source
)
async def add_sub_step_source(self: types.Message, state: FSMContext):
    try:
        logger.info("add_sub_step_source")
        for i in self.text.split('\n'):
            sources.append(i)
        await FSM.add_sub_step_sub.set()
        await self.answer(f'Enter sub numbers')

    except Exception as e:
        out = f'add_sub_step_source, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.add_sub_step_sub
)
async def add_sub_step_sub(self: types.Message, state: FSMContext):
    try:
        logger.info("add_sub_step_sub")
        for i in self.text.split('\n'):
            subs.append(i)
        result = capi.add_sub(logins, sources, subs)
        logins.clear()
        sources.clear()
        subs.clear()
        await FSM.primary.set()
        if result.ok:
            await self.reply(f'Operation done')
            with open("test.txt", "w", encoding="utf-8") as file:
                file.write(result.text)
        else:
            await self.reply(f'Response code {result.status_code}, unsuccessful!')

    except Exception as e:
        out = f'add_sub_step_sub, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.open_org_step_user
)
async def open_org_step_user(self: types.Message, state: FSMContext):
    try:
        logins.append(self.text)
        await FSM.open_org_step_app.set()
        await self.answer(f'Enter what to open')

    except Exception as e:
        out = f'open_org_step_user, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.open_org_step_app
)
async def open_org_step_app(self: types.Message, state: FSMContext):
    try:
        logger.info("open_org_step_app")
        for i in self.text.split('\n'):
            bundles.append(i)
        result = capi.open_org(logins, bundles)
        logins.clear()
        bundles.clear()
        await FSM.primary.set()
        if result.ok:
            await self.reply(f'Operation done')
            with open("test.txt", "w", encoding="utf-8") as file:
                file.write(result.text)
        else:
            await self.reply(f'Response code {result.status_code}, unsuccessful!')

    except Exception as e:
        out = f'open_org_step_app, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.close_org_step_user
)
async def close_org_step_user(self: types.Message, state: FSMContext):
    try:
        logger.info("close_org_step_user")
        logins.append(self.text)
        await FSM.close_org_step_app.set()
        await self.answer(f'Enter what to close')

    except Exception as e:
        out = f'close_org_step_user, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.close_org_step_app
)
async def close_org_step_app(self: types.Message, state: FSMContext):
    try:
        logger.info("close_org_step_app")
        for i in self.text.split('\n'):
            bundles.append(i)
        result = capi.close_org(logins, bundles)
        logins.clear()
        bundles.clear()
        await FSM.primary.set()
        if result.ok:
            await self.reply(f'Operation done')
            with open("test.txt", "w", encoding="utf-8") as file:
                file.write(result.text)
        else:
            await self.reply(f'Response code {result.status_code}, unsuccessful!')

    except Exception as e:
        out = f'close_org_step_app, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.allow_edit_org_step_user
)
async def allow_edit_org_step_user(self: types.Message, state: FSMContext):
    try:
        logger.info("allow_edit_org_step_user")
        logins.append(self.text)
        await FSM.allow_edit_org_step_app.set()
        await self.answer(f'Enter what to allow')

    except Exception as e:
        out = f'allow_edit_org_step_user, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.allow_edit_org_step_app
)
async def allow_edit_org_step_app(self: types.Message, state: FSMContext):
    try:
        logger.info("allow_edit_org_step_app")
        for i in self.text.split('\n'):
            bundles.append(i)
        result = capi.a_edit_org(logins, bundles)
        logins.clear()
        bundles.clear()
        await FSM.primary.set()
        if result.ok:
            await self.reply(f'Operation done')
            with open("test.txt", "w", encoding="utf-8") as file:
                file.write(result.text)
        else:
            await self.reply(f'Response code {result.status_code}, unsuccessful!')

    except Exception as e:
        out = f'allow_edit_org_step_app, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    state="*",
    commands="start",
    user_id=admin
)
async def main_menu(message: types.Message):
    await FSM.primary.set()
    get_users_list(message.text)
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
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.primary,
    commands="sukablyatebuchayaklava"
)
async def del_keyb(message: types.Message):
    delete = types.ReplyKeyboardRemove(True)
    await message.answer(f'Done', reply_markup=delete)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.primary,
    commands="test"
)
async def test(message: types.Message):
    result = user_search(message.text.split(" ")[1])
    await message.answer(' '.join(result))


@dp.message_handler(
    state="*"
)
async def echo(message: types.Message):
    result = f'Unrecognized command\n\n{message.text}'
    logger.info(result)
    await message.answer(result)
