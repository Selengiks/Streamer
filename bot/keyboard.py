from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
import bot.crm_api as capi

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
open_fin_visib_key = InlineKeyboardButton('Add for financier visibility', callback_data='/open_fin_vis')
keyboard = InlineKeyboardMarkup(row_width=2).add(add_user_key, del_user_key, add_user_sub_key, add_user_camp_key,
                                                 open_org_key, close_org_key, allow_org_edit_key, open_camp_visib_key,
                                                 close_camp_visib_key, open_fin_visib_key)

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
