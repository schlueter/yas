from yas.yaml_file_config import YamlConfiguration
from yas.logging import logger


class YasError(Exception):
    def __init__(self, msg):
        self.logger = Logger(self.log_level)
        log.fatal(msg)

class HandlerError(YasError):
    def __init__(msg):
        super().__init__(msg)

class SlackClientFailure(YasError):
    def __init__(self, msg):
        super().__init__(msg)

class NoBot(SlackClientFailure):
    def __init__(self, bot_name):
        super().__init__(f"Could not find bot user with the name {bot_name}, please check your yas config.")

class NotAHandler(HandlerError):
    def __init__(self, not_a_handler):
        super().__init__(f"{not_a_handler} is not a handler.")

class YasHandler:
    pass

