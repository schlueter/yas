from yas import YasHandler, HandlerError
from yas.yaml_file_config import YamlConfiguration


config = YamlConfiguration()

class NotTalkingToBotHandler(YasHandler):

    def __init__(self, bot_name, api_call, log=None):
        super().__init__(bot_name, api_call, log=log)
        self.bot_id = self.__retrieve_user_id(self.bot_name)
        self.at_bot = "<@" + self.bot_id + ">"
        self.api_call = api_call

    def test(self, data):

        # @message the bot
        if self.at_bot in data.get('text', ''):
            self.log('DEBUG', f"Message contained {self.at_bot}, {data['yas_hash']}")
            return False

        channel = data.get('channel')
        channel_info = self.api_call('channels.info', channel=channel)
        group_info = self.api_call('groups.info', channel=channel)

        # Direct message
        if not channel_info.get('ok') and not group_info.get('ok'):
            self.log('DEBUG', f"Direct message to bot, {data['yas_hash']}")
            return False

        return True

    def handle(self, data, _):
        pass


class SlackClientFailure(HandlerError):
    def __init__(self, msg):
        super().__init__(msg)


class NoBot(SlackClientFailure):
    def __init__(self, bot_name):
        super().__init__(f"Could not find bot user with the name {bot_name}, please check your yas config.")
