import re


class YasHandler:

    def __init__(self, bot):
        self.bot = bot


class RegexHandler(YasHandler):

    def __init__(self, regexp_string, bot):
        super().__init__(bot)
        self.regexp = re.compile(regexp_string)
        self.bot.log.info(f"{self.__class__} initialized and matching {regexp_string}!")

    def test(self, data):
        self.current_match = self.regexp.search(data.get('text'))
        return self.current_match
