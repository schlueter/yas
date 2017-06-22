from yas import YasHandler


class IgnoredTypesHandler(YasHandler):
    def test(self, data):
        if data.get('type') in self.bot.config.ignored_types:
            return True

    def handle(self, data, _):
        pass
