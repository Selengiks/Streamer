from loguru import logger
from support import loggeru
import config_data_priv

loggeru.start()

logger.debug("Bot connection establish")

TOKEN = config_data_priv.BOT_TOKEN
DOMAIN = config_data_priv.DOMAIN
SCRIPT_API = config_data_priv.SCRIPT_API
GET_USERS_API = config_data_priv.GET_USERS_API
GET_BUNDLES_API = config_data_priv.GET_BUNDLES_API
API_TOKEN = config_data_priv.API_KEY
PROXIES = config_data_priv.PROXIES

# local_server_url = "http://127.0.0.1:8888"
local_server_url = None

admins = ['290522978']  # Global admins

GLOBAL_DELAY = .09
