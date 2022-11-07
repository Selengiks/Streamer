from collections import OrderedDict

import requests
from loguru import logger
import config as cfg

URL = cfg.SCRIPT_API


def get_user_id(logins):
    get_users_url = cfg.GET_USERS_API
    response = requests.get(get_users_url)
    userdict = {item['id']: item for item in response.json()}
    data = []

    for k, v in userdict.items():
        for i in logins:
            if i == v['login']:
                data.append(v['id'])

    result = {'response': response, 'data': data}

    return result


def get_campaign_id(bundles):
    get_bundles_url = cfg.GET_BUNDLES_API
    response = requests.get(get_bundles_url)
    bundledict = {item['id']: item for item in response.json()}
    data = []

    for k, v in bundledict.items():
        for i in bundles:

            if i == v['name']:
                data.append(v['id'])

    result = {'response': response, 'data': data}

    return result


def add_user(login, source, sub, lead):
    pass


def del_user(logins):
    pass


def add_sub(login, source, sub):
    pass


def add_camp(login, bundle, sub):
    pass


def open_org(logins, bundles):
    data = [
        {
            "add_specific_visibility": "",
            "campaigns": get_campaign_id(bundles),  # idшки компаний что открыть
            "keitaro_master": get_user_id(logins)  # масив айдишек юзеров кому открыть
        }
    ]
    # result = requests.post(URL, data=data)
    print(data)


def close_org(logins, bundles):
    data = [
        {
            "delete_specific_visibility": "",
            "campaigns": get_campaign_id(bundles),  # idшки компаний что открыть
            "keitaro_master": get_user_id(logins)  # масив айдишек юзеров кому открыть
        }
    ]
    # result = requests.post(URL, data=data)
    print(data)


def a_edit_org(logins, bundles):
    data = [
        {
            "allow_edit_organic": "",
            "app": get_campaign_id(bundles),  # бандлы прил где разрешить редачить органику
            "keitaro": get_user_id(logins)  # айдишка юзера кому открыть
        }
    ]
    # result = requests.post(URL, data=data)
    print(data)


def check_visibility(login):
    pass


test = ["22bet", "admin", "Aleksej Grund"]
test2 = ["", ""]
get_user_id(test)
get_campaign_id(test2)
