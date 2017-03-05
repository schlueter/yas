from yas.logging import log

class YasHandler:
    pass

class HandlerError(Exception):
    pass

class SlackClientFailure(Exception):
    def __init__(self, msg):
        log.fatal(msg)

class NoBot(SlackClientFailure):
    def __init__(self, bot_name):
        log.fatal(f"Could not find bot user with the name {bot_name}, please check your yas config.")

class NotAHandler(HandlerError):
    def __init__(self, not_a_handler):
        super().__init__(f"{not_a_handler} is not a handler.")
