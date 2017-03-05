import hashlib

from slackclient import SlackClient

from yas import SlackClientFailure, NoBot, HandlerError
from yas.handler_manager import HandlerManager
from yas.logging import logger
from yas.yaml_file_config import YamlConfiguration


config = YamlConfiguration()

def hash(string):
    return hashlib.md5(str(string).encode('utf-8')).hexdigest()

class Client(SlackClient):

    def __init__(self, data_filter=None, ignored_types=None):
        super().__init__(config.slack_app_token)

        self.bot_id = self.__retrieve_bot_user_id()

        self.at_bot = "<@" + self.bot_id + ">"
        self.data_filter = data_filter

        self.ignored_types = ignored_types or config.ignored_types

        self.handler_manager = HandlerManager(config.handler_list)

    def __retrieve_bot_user_id(self):
        logger.log.info("Retrieving users list for self identification...")
        api_call = self.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == config.bot_name:
                    return user.get('id')
            else:
                raise NoBot(config.bot_name)
        else:
            raise SlackClientFailure("Unable to query api")

    def process_changes(self, data):
        super().process_changes(data)
        logger.log.debug(f"Raw data: {data}")
        if self.data_filter(self, data):
            channel = data.get('channel')
            def reply(message, channel=channel, thread=None, reply_broadcast=None):
                self.rtm_send_message(channel, message, thread, reply_broadcast)
            data['yas_hash'] = hash(data)
            logger.log.info(f"Processing: {data}")
            try:
                self.handler_manager.handle(data, reply)
            except Exception as exception:
                reply(f"Err, sorry, that threw an exception: {exception}. Try again or reach out to the maintainers.")

    def listen(self):
        if self.rtm_connect():
            logger.log.info("Slack bot connected as {}<{}> and running!".format(config.bot_name, self.bot_id))
            while True:
                self.rtm_read()
        else:
            logger.log.fatal("Connection failed. Invalid Slack token or bot ID?")
