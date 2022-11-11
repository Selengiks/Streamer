import json
from collections import OrderedDict

import requests
from loguru import logger
import config as cfg

URL = cfg.SCRIPT_API
HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }
THEADER = {"Api-Key": cfg.API_TOKEN}


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

            if f'ORG {i}' in v['name']:
                data.append(v['id'])

    result = {'response': response, 'data': data}
    return result


def get_app_id(bundles):
    get_apps_url = cfg.DOMAIN
    response = requests.get(f'{get_apps_url}traffic_sources', headers=THEADER)
    appsdict = {item['id']: item for item in response.json()}
    data = []

    for k, v in appsdict.items():
        for i in bundles:

            if i in v['name']:
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
    data = {
        "add_specific_visibility": "Готово",
        "campaigns[]": get_campaign_id(bundles).get('data'),
        "keitaro_master[]": get_user_id(logins).get('data')
    }

    result = requests.post(URL, data=data, headers=HEADER)
    return result


def close_org(logins, bundles):
    data = {
        "delete_specific_visibility": "Готово",
        "campaigns[]": get_campaign_id(bundles).get('data'),
        "keitaro_master[]": get_user_id(logins).get('data')
    }

    result = requests.post(URL, data=data, headers=HEADER)
    return result


def a_edit_org(logins, bundles):
    data = {
        "allow_edit_organic": "",
        "app[]": get_app_id(bundles).get('data'),
        "keitaro": get_user_id(logins).get('data')
    }

    result = requests.post(URL, data=data, headers=HEADER)
    return result


def check_visibility(login):
    pass
