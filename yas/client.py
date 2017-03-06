import hashlib

from slackclient import SlackClient

from yas.handler_manager import HandlerManager
from yas.logging import logger
from yas.yaml_file_config import YamlConfiguration


config = YamlConfiguration()

def hash(string):
    return hashlib.md5(str(string).encode('utf-8')).hexdigest()

class Client(SlackClient):

    def __init__(self, ignored_types=None):
        super().__init__(config.slack_app_token)

        self.ignored_types = ignored_types or config.ignored_types

        self.handler_manager = HandlerManager(
                config.handler_list,
                config.bot_name,
                self.api_call,
                debug=config.debug)

    def process_changes(self, data):
        super().process_changes(data)
        logger.log.debug(f"Raw data: {data}")
        channel = data.get('channel')
        def reply(message, channel=channel, thread=None, reply_broadcast=None):
            if channel:
                self.rtm_send_message(channel, message, thread, reply_broadcast)
        data['yas_hash'] = hash(data)
        logger.log.info(f"Processing: {data}")
        try:
            self.handler_manager.handle(data, reply)
        except Exception as exception:
            reply(f"Err, sorry, that threw an exception: {exception}. Try again or reach out to the maintainers.")

    def listen(self):
        if self.rtm_connect():
            logger.log.info(f"Slack bot connected as {config.bot_name} and running!")
            while True:
                self.rtm_read()
        else:
            logger.log.fatal(
                "Connection failed. If this occured after the bot had been running"
                "a while, it was probably just a connection blip; otherwise, confirm"
                "the yas.yml has a valid token and name.")
