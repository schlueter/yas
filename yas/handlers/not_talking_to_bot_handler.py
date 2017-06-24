from yas import YasHandler


class NotTalkingToBotHandler(YasHandler):

    def __init__(self, bot):
        super().__init__(bot)
        bot_id = self.bot.retrieve_user_id(self.bot.config.bot_name)
        self.at_bot = "<@" + bot_id + ">"

    def test(self, data):

        # @message the bot
        if self.at_bot in data.get('text', ''):
            return False

        channel = data.get('channel')
        channel_info = self.bot.api_call('channels.info', channel=channel)
        group_info = self.bot.api_call('groups.info', channel=channel)

        # Direct message
        if not channel_info.get('ok') and not group_info.get('ok'):
            return False

        return True

    def handle(self, data, _):
        pass
