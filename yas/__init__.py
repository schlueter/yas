import re


class YasHandler:

    def __init__(self, bot):
        self.bot = bot

    def setup(self):
        self.bot.log.debug(f"Noop setup for {self}")


class RegexHandler(YasHandler):

    def __init__(self, regexp_string, bot):
        super().__init__(bot)
        self.regexp = re.compile(regexp_string, flags=re.IGNORECASE)
        self.bot.log.info(f"{self.__class__} initialized and matching {regexp_string}!")
        bot_id = self.bot.retrieve_user_id(self.bot.config.bot_name)
        self.at_bot = "<@" + bot_id + ">"

    def test(self, data):
        text = data.get('text', '').replace(self.at_bot, '').strip()
        self.current_match = self.regexp.search(text)
        return self.current_match
