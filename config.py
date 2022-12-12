from loguru import logger
from support import loggeru
import config_data_priv

DEBUG = 1  # 1 - Enable DEBUG output, 0 - disable DEBUG output
loggeru.start(DEBUG)

logger.debug("Bot connection establish")

TOKEN = config_data_priv.BOT_TOKEN
DOMAIN = config_data_priv.DOMAIN
KEITARO_FORM = config_data_priv.SCRIPT_API
ALL_USERS_PAGE = config_data_priv.ALL_USERS
ALL_CAMPAIGNS_PAGE = config_data_priv.ALL_CAMPAIGNS
API_TOKEN = config_data_priv.API_KEY
PROXIES = config_data_priv.PROXIES

# local_server_url = "http://127.0.0.1:8888"
local_server_url = None

admins = ['290522978']  # Global admins

GLOBAL_DELAY = .09
