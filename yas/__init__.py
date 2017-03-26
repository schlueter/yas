import re

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
    def __init__(self, msg):
        logger.log.warn(msg)

class RegexHandler(YasHandler):

    def __init__(self, regexp_string, bot_name, api_call, log=print):
        super().__init__(bot_name, api_call, log=log)
        self.regexp = re.compile(regexp_string)
        self.log('INFO', f"{self.__class__} initialized and matching {regexp_string}!")

    def test(self, data):
        self.current_match = self.regexp.search(data.get('text'))
        return self.current_match
