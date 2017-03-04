import os
import sys

from slackclient import SlackClient

from yas.handler_manager import HandlerManager
from yas.errors import HandlerError, SlackClientFailure
from yas.yaml_file_config import YamlConfiguration as Config


def log(*msg):
    print(*msg, file=sys.stderr)

class Client(SlackClient):

    def __init__(self, data_filter=None, ignored_types=None):
        self.config = Config()
        super().__init__(self.config.slack_app_token)
        self.bot_name = self.config.bot_name
        self.bot_id = self.__retrieve_bot_user_id()
        self.at_bot = "<@" + self.bot_id + ">"
        self.data_filter = data_filter or self.__default_data_filter
        self.ignored_types = ignored_types or self.config.ignored_types
        self.handler_manager = HandlerManager(self.config.handler_list)

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
                self.handler_manager.handle(data, reply, self.api_call)
            except HandlerError as e:
                self.rtm_send_message(channel, str(e))

    def listen(self):
        if self.rtm_connect():
            log("Slack bot connected as {}<{}> and running!".format(self.bot_name, self.bot_id))
            while True:
                self.rtm_read()
        else:
            log("Connection failed. Invalid Slack token or bot ID?")


class YasHandler:
    '''
    YasHandlers, when registered with a Yas installation in the active yas.yml,
    are tested against, and upon matching applied to, incoming messages by Yas
    as they are receieved.
    '''

    def test(self, data):
        '''
        If this method returns truthy, this class's handle method is called with the data.
        By default, this handler is registered with yas. To disable, remove
        yas.handler from the handler_list in your yas.yml.

        Arguments:

        data :: dict :: An event from the slack RTM websocket. To see the raw
            stream, enable the raw_response handler. The objects are pre filtered by
            the yas client's data_filter method, which by default filters out any
            ignored types from the yas config, objects not associated with a
            channel, and objects originating from the bot. The implementation of this
            behaviour is likely to change in the future, but the default filters are not.
        '''
        return True

    def handle(self, data, reply, api_call, handler_manager):
        '''
        Handles a matched data object. If a HandlerError is raised here, it will be caught,
        and its message sent to the originating channel; other errors are not caught and
        will crash yas, which shouldn't be a problem if one of the included daemon scripts
        is used as they will restart yas after a crash.

        Arguments:

        data :: dict :: See test.

        reply :: function(response, channel=channel, thread=None, reply_broadcast=None) ::
            A shortcut function to reply to a message. The response is your message back
            to the channel. The channel, which defaults to the data's channel, is where
            the message will be delivered; besides the default, another useful channel
            is the data's originating user, which would direct message that user. The
            thread is the parent message ID, if you wish to initiate a thread.
            The reply_broadcast argument takes a boolean value and indicates whether a
            threaded message should also reply in the parent channel.

        api_call :: function(method, timeout=None, **kwargs) :: The api_call method of
            the yas client listening for messages. This is provided so that handler
            authors may shoot themselves in the foot. Available methods may be found
            at https://api.slack.com/methods. This function may be restricted or
            removed in the future as it is rather dangerous.

        handler_manager :: yas.handler.HandlerManager :: The HandlerManager instance
            the YasHandler instance is bound to. This is provided so that query response
            listeners may be registered. This argument may be replaced in the future with
            something more explicit.
        '''

        raise HandlerError("Sure...write some more code then I can do that!")
