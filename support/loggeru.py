from sys import stdout
from loguru import logger


def start(debug):

    logger.remove()
    logger.add("logs/log_{time}.txt", rotation="1 day")

    info_filter = lambda record: record["level"].name == "INFO"
    info_format = "<green>{time:DD.MM.YY H:mm:ss}</green> | " \
                  "<yellow><b>{level}</b></yellow> | " \
                  "<magenta>{file}</magenta> | " \
                  "<cyan>{message}</cyan>"

    logger.add(stdout, filter=info_filter, level="INFO", colorize=True, format=info_format)

    debug_filter = lambda record: record["level"].name == "DEBUG"
    debug_format = "<green>{time:DD.MM.YY H:mm:ss}</green> | " \
                   "<red><b>{level}</b></red> | " \
                   "<magenta>{file}</magenta> | " \
                   "<yellow>{message}</yellow>"

    if debug:
        logger.add(stdout, filter=debug_filter, level="DEBUG", colorize=True, format=debug_format)

    logger.debug("Logger configured")
