from yas.yaml_file_config import YamlConfiguration
from yas.logging import logger, log


class YasHandler:
    def __init__(self, bot_name, api_call, log=log):
        self.bot_name = bot_name
        self.api_call = api_call
        self.log = log

class YasError(Exception):
    def __init__(self, msg):
        logger.log.fatal(msg)

class HandlerError(YasError):
    def __init__(msg):
        super().__init__(msg)
