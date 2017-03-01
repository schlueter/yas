import os
import sys

from slackclient import SlackClient

from yas.yaml_file_config import YamlConfiguration as Config
from yas.handlers import handler, HandlerError


def log(*msg): print(*msg, file=sys.stderr)

class Client(SlackClient):

    def __init__(self, data_filter=None, ignored_types=None):
        self.config = Config()
        super().__init__(self.config.slack_app_token)
        self.bot_name = self.config.bot_name
        self.bot_id = self.__retrieve_bot_user_id()
        self.at_bot = "<@" + self.bot_id + ">"
        self.data_filter = data_filter or self.__default_data_filter
        self.ignored_types = ignored_types or self.config.ignored_types

    def __default_data_filter(self, data):
        if data.get('type') not in self.ignored_types and \
                'channel' in data and data.get('user') != self.bot_id:
            channel = data['channel']
            channel_info = self.api_call('channels.info', channel=channel)
            if channel_info.get('ok') and self.at_bot in data['text']:
                return True
            group_info = self.api_call('groups.info', channel=channel)
            if not channel_info.get('ok', False) and not group_info.get('ok', False):
                return True

    def __retrieve_bot_user_id(self):
        log("Retrieving users list for self identification...")
        api_call = self.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    return user.get('id')
            else:
                raise NoBot("could not find bot user with the name " + self.bot_name)
        else:
            raise SlackClientFailure()

    def process_changes(self, data):
        super().process_changes(data)
        if self.data_filter(data):
            log(f'Processing: {data}')
            channel = data.get('channel')
            def reply(message, channel=channel, thread=None, reply_broadcast=None):
                self.rtm_send_message(channel, message, thread, reply_broadcast)
            try:
                self.handle_messages(data, reply)
            except HandlerError as e:
                self.rtm_send_message(channel, str(e))
                # self.rtm_send_message(channel, "Sure...write some more code then I can do that!")

    def handle_messages(self, data, reply):
        handler(data, reply)

    def listen(self):
        if self.rtm_connect():
            log("Slack bot connected as {}<{}> and running!".format(self.bot_name, self.bot_id))
            while True:
                self.rtm_read()
        else:
            log("Connection failed. Invalid Slack token or bot ID?")

class SlackClientFailure(Exception):
    pass

def main():
    client = Client()
    client.listen()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log('Caught keyboard interrupt, exiting...')
        exit()
