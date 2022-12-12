import requests
import config as cfg

URL = cfg.KEITARO_FORM
HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }
THEADER = {"Api-Key": cfg.API_TOKEN}


def get_users():
    response = requests.get(cfg.ALL_USERS_PAGE)
    userdict = {item['id']: item for item in response.json()}

    result = {'response': response, 'data': userdict}
    return result


def get_user(logins):  # Find and get users by login
    response = requests.get(cfg.ALL_USERS_PAGE)
    data = {}

    for k, v in get_users()['data'].items():
        for i in logins:
            if i == v['login']:
                data[k] = v

    result = {'response': response, 'data': data}
    return result


def get_campaign(values):  # Get campaigns by bundles
    response = requests.get(cfg.ALL_CAMPAIGNS_PAGE)
    bundledict = {item['id']: item for item in response.json()}
    data = {}

    for k, v in bundledict.items():
        for i in values:
            if i in v['name']:
                data[k] = v

    result = {'response': response, 'data': data}
    return result


def get_app_id(bundles):  # Get app id by bundle
    response = requests.get(f'{cfg.DOMAIN}/traffic_sources', headers=THEADER)
    appsdict = {item['id']: item for item in response.json()}
    data = []

    for k, v in appsdict.items():
        for i in bundles:

            if i in v['name']:
                data[k] = v

    result = {'response': response, 'data': data}
    return result


def get_group_id(key):  # Get group id by search key
    response = requests.get(f'{cfg.DOMAIN}/groups?type=campaigns', headers=THEADER)
    groupsdict = {item['id']: item for item in response.json()}
    data = {}

    for k, v in groupsdict.items():
        if key in v['name']:
            data['id'] = v['id']
            data['name'] = v['name']

    result = {'response': response, 'data': data}
    return result


def get_last_open_sub():  # Get last opened sub number
    pass


def get_result():  # Get result after execute commands from end of page
    pass


def add_user(login, source, sub, lead):
    pass


def del_user(logins):
    pass


def add_sub(login, source, sub):
    data = {
        "add_new_stream": "Добавить",
        "keitaro[]": login,
        "source[]": source,
        "stream[]": sub
    }

    result = requests.post(URL, data=data, headers=HEADER)
    return result


def add_camp(login, bundle, sub):
    pass


def open_org(logins, bundles):
    campaigns = get_campaign([f'ORG {i}'for i in bundles])['data']
    users = get_user(logins)['data']
    data = {
        "add_specific_visibility": "Готово",
        "campaigns[]": [campaigns[i]['name'] for i in campaigns],
        "keitaro_master[]": [users[i]['id'] for i in users]
    }

    result = requests.post(URL, data=data, headers=HEADER)
    return result


def close_org(logins, bundles):
    campaigns = get_campaign([f'ORG {i}' for i in bundles])['data']
    users = get_user(logins)['data']
    data = {
        "delete_specific_visibility": "Готово",
        "campaigns[]": [campaigns[i]['name'] for i in campaigns],
        "keitaro_master[]": [users[i]['id'] for i in users]
    }

    result = requests.post(URL, data=data, headers=HEADER)
    return result


def a_edit_org(logins, bundles):
    users = get_user(logins)['data']
    data = {
        "allow_edit_organic": "",
        "app[]": get_app_id(bundles).get('data'),
        "keitaro": [users[i]['id'] for i in users]
    }

    result = requests.post(URL, data=data, headers=HEADER)
    return result


def open_fin_visibility(bundles):
    campaign = get_campaign(bundles)
    data = campaign['campaign'][0]
    data |= {
        "group_id": get_group_id('TB_UAC_ORG')['data']['id']
    }
    response = requests.put(f'{cfg.DOMAIN}/campaigns/{campaign["data"][0]}', headers=THEADER, data=data)

    result = {'response': response, 'data': response.json()}
    return result
