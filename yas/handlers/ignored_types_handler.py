from yas import YasHandler


class IgnoredTypesHandler(YasHandler):
    def test(self, data):
        return data.get('type') in self.bot.config.ignored_types

    def handle(self, data, _):
        pass
