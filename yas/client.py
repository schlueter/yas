import hashlib
from threading import Thread
import time

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

        self.all_users = self._retrieve_users_list()
        self.handler_manager = HandlerManager(
                config.handler_list,
                config.bot_name,
                self.api_call,
                debug=config.debug)

    def _retrieve_users_list(self):
        self.log("INFO", "Retrieving users list...")
        api_call = self.api_call("users.list")
        if not api_call.get('ok'):
            raise SlackClientFailure("Unable to query api! This is usually due to an incorrect api key, please check your yas config.")
        return api_call.get('members')

    def _retrieve_user_id(self, username):
        for user in self.all_users:
            if 'name' in user and user.get('name') == username:
                return user.get('id')
        else:
            raise NoSuchUser(self.bot_name)

    def _retrieve_user_info(self, user_id):
        try:
            creator_info = self.api_call('users.info', user=user_id)
        except Exception as e:
            self.log('WARN', f"Caught {e} while retrieving creator_info.")
            creator_info = None
        return creator_info


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
            self.handler_manager.handle(data, reply, slack_client=self)
        except Exception as exception:
            reply(config.handler_exception_message.format(exception=exception))

    def listen(self):
        if self.rtm_connect():
            logger.log.info(f"Slack bot connected as {config.bot_name} and running!")
            while True:
                thread = Thread(target=self.rtm_read)
                thread.start()
                time.sleep(0.01)
        else:
            logger.log.fatal(
                "Connection failed. If this occured after the bot had been running"
                "a while, it was probably just a connection blip; otherwise, confirm"
                "the yas.yml has a valid token and name.")
