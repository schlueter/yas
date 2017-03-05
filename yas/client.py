from slackclient import SlackClient

from yas import SlackClientFailure, NoBot
from yas.handler_manager import HandlerManager
from yas.logging import log
from yas.yaml_file_config import YamlConfiguration


class Client(SlackClient):

    def __init__(self, data_filter=None, ignored_types=None):
        self.config = YamlConfiguration()

        log.info(f"Slack application token is {self.config.slack_app_token}")
        super().__init__(self.config.slack_app_token)

        self.bot_id = self.__retrieve_bot_user_id()

        self.at_bot = "<@" + self.bot_id + ">"
        self.data_filter = data_filter
        self.ignored_types = ignored_types or self.config.ignored_types

        self.handler_manager = HandlerManager(self.config.handler_list, debug=self.config.debug)
        log.info(self)
        log.info(self.__dict__)

    def __retrieve_bot_user_id(self):
        log.info("Retrieving users list for self identification...")
        api_call = self.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.config.bot_name:
                    return user.get('id')
            else:
                raise NoBot(self.config.bot_name)
        else:
            raise SlackClientFailure("Unable to query api")

    def process_changes(self, data):
        super().process_changes(data)
        if self.data_filter(self, data):
            log.info(f'Processing: {data}')
            channel = data.get('channel')
            def reply(message, channel=channel, thread=None, reply_broadcast=None):
                self.rtm_send_message(channel, message, thread, reply_broadcast)
            try:
                self.handler_manager.handle(data, reply, self.api_call)
            except HandlerError as e:
                self.rtm_send_message(channel, str(e))
                # self.rtm_send_message(channel, "Sure...write some more code then I can do that!")

    def listen(self):
        if self.rtm_connect():
            log.info("Slack bot connected as {}<{}> and running!".format(self.config.bot_name, self.bot_id))
            while True:
                self.rtm_read()
        else:
            log.fatal("Connection failed. Invalid Slack token or bot ID?")
