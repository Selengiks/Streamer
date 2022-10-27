import os

from loguru import logger
from support import loggeru
import config_data_priv

loggeru.start()

logger.debug("Bot connection establish")

TOKEN = config_data_priv.BOT_TOKEN
PROXIES = config_data_priv.PROXIES

# local_server_url = "http://127.0.0.1:8888"
local_server_url = None

admins = ['290522978']  # Глобальные админы

GLOBAL_DELAY = .09
