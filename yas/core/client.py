import hashlib
import time
from threading import Thread

from slackclient import SlackClient
from slackclient._server import SlackConnectionError, SlackLoginError

from yas.core.handler_manager import HandlerManager
from yas.core.logging import Logger
from yas.core.yaml_file_config import YamlConfiguration


def rough_hash(string):
    return hashlib.md5(str(string).encode('utf-8')).hexdigest()

class Client(SlackClient):

    def __init__(self, ignored_types=None):
        self.config = YamlConfiguration()
        self.log = Logger(self.config.log_level).log
        super().__init__(self.config.slack_app_token)
        self.handler_manager = HandlerManager(self.config, self.api_call, self.log)

    def process_changes(self, data):
        super().process_changes(data)
        self.log.debug(f"Raw data: {data}")
        channel = data.get('channel')
        def reply(message, channel=channel, thread=None, reply_broadcast=None):
            if channel:
                self.rtm_send_message(channel, message, thread, reply_broadcast)
        data['yas_hash'] = rough_hash(data)
        self.log.info(f"Processing: {data}")
        try:
            thread = Thread(target=self.handler_manager.handle, args=(data, reply))
            thread.start()
        # pylint: disable=broad-except
        except Exception as exception:
            reply(self.config.handler_exception_message.format(exception=exception))
            # pylint: disable=raising-bad-type
            raise exception

    def listen(self):
        try:
            self.rtm_connect()
            self.log.info(f"Slack bot connected as {self.config.bot_name} and running!")
            while True:
                self.rtm_read()
                time.sleep(0.01)
        except (SlackConnectionError, SlackLoginError):
            self.log.fatal(
                "Connection failed. If this occured after the bot had been running "
                "a while, it was probably just a connection blip; otherwise, confirm "
                "the yas.yml has a valid token and name."
            )
