from yas import YasHandler, HandlerError
from yas.yaml_file_config import YamlConfiguration


config = YamlConfiguration()

class NotTalkingToBotHandler(YasHandler):

    def __init__(self, bot_name, api_call=None, log=None):
        super().__init__(bot_name, api_call, log=log)
        self.bot_id = self.__retrieve_bot_user_id()
        self.at_bot = "<@" + self.bot_id + ">"
        self.api_call = api_call

    def __retrieve_bot_user_id(self):
        self.log("INFO", "Retrieving users list for self identification...")
        api_call = self.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    return user.get('id')
            else:
                raise NoBot(self.bot_name)
        else:
            raise SlackClientFailure("Unable to query api! This is usually due to an incorrect api key, please check your yas config.")


    def test(self, data):
        channel = data.get('channel')
        channel_info = self.api_call('channels.info', channel=channel)
        if channel_info.get('ok') and not self.at_bot in data['text']:
            self.log('DEBUG', f"Message contained {self.at_bot}, {data['yas_hash']}")
            return True
        group_info = self.api_call('groups.info', channel=channel)
        if channel_info.get('ok', False) and group_info.get('ok', False):
            self.log('DEBUG', f"Direct message to bot, {data['yas_hash']}")
            return True

    def handle(self, data, _):
        pass


class SlackClientFailure(HandlerError):
    def __init__(self, msg):
        super().__init__(msg)


class NoBot(SlackClientFailure):
    def __init__(self, bot_name):
        super().__init__(f"Could not find bot user with the name {bot_name}, please check your yas config.")


