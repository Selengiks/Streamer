import config as cfg
from aiogram import md, types
from loguru import logger
from support.bots import dp, bot
from aiogram.dispatcher import FSMContext
from bot import crm_api as capi, FSM as fsm, keyboard as kb

logger.debug("Bot commands module loaded")

admin = cfg.admins

FSM = fsm.FSM()


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

    elif code == '/open_fin_vis':
        await FSM.open_fin_visib_step_app.set()
        await bot.send_message(callback_query.from_user.id, text="Enter app bundle to open")

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
    await main_menu(message)


@dp.message_handler(
    chat_type=[types.ChatType.PRIVATE],
    state="*",
    commands="start",
    user_id=admin
)
async def main_menu(message: types.Message):
    await FSM.primary.set()
    kb.get_users_list(message.text)
    botinfo = await dp.bot.me
    result = f'{botinfo.full_name} [{md.hcode(f"@{botinfo.username}")}] on line!'
    logger.info(result)
    await message.reply(result, reply_markup=kb.keyboard)


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
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.find_user
)
async def find_user(self: types.Message):
    try:
        logger.info("find_user")
        await self.reply('Finded users, type manual, buttons inactive:\n', reply_markup=kb.get_users_list(self.text))
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
async def add_sub_step_user(self: types.Message):
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
async def add_sub_step_source(self: types.Message):
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
async def add_sub_step_sub(self: types.Message):
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

        else:
            await self.reply(f'Response code {result.status_code}, unsuccessful!')

    except Exception as e:
        out = f'add_sub_step_sub, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)

    finally:
        await main_menu(self)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.open_org_step_user
)
async def open_org_step_user(self: types.Message):
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
async def open_org_step_app(self: types.Message):
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

        else:
            await self.reply(f'Response code {result.status_code}, unsuccessful!')

    except Exception as e:
        out = f'open_org_step_app, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)

    finally:
        await main_menu(self)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.close_org_step_user
)
async def close_org_step_user(self: types.Message):
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
async def close_org_step_app(self: types.Message):
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

        else:
            await self.reply(f'Response code {result.status_code}, unsuccessful!')

    except Exception as e:
        out = f'close_org_step_app, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)

    finally:
        await main_menu(self)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.allow_edit_org_step_user
)
async def allow_edit_org_step_user(self: types.Message):
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
async def allow_edit_org_step_app(self: types.Message):
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

        else:
            await self.reply(f'Response code {result.status_code}, unsuccessful!')

    except Exception as e:
        out = f'allow_edit_org_step_app, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)

    finally:
        await main_menu(self)


@dp.message_handler(
    user_id=admin,
    chat_type=[types.ChatType.PRIVATE],
    state=FSM.open_fin_visib_step_app
)
async def open_fin_visib_step_app(self: types.Message):
    try:
        logger.info("open_fin_visib_step_app")
        bundles.append(self.text)
        result = capi.open_fin_visibility(bundles)
        bundles.clear()
        await FSM.primary.set()
        if result['response'].ok:
            await self.reply(f'Operation done')

        else:
            await self.reply(f'Response code {result.status_code}, unsuccessful!')

    except Exception as e:
        out = f'open_fin_visib_step_app, something get wrong!\n Raised "{str(e)}" error!'
        logger.info(out)
        await self.reply(out)

    finally:
        await main_menu(self)


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
    result = kb.user_search(message.text.split(" ")[1])
    await message.answer(' '.join(result))


@dp.message_handler(
    state="*"
)
async def echo(message: types.Message):
    result = f'Unrecognized command\n\n{message.text}'
    logger.info(result)
    await message.answer(result)
