from yas import YasHandler, HandlerError
from yas.yaml_file_config import YamlConfiguration


config = YamlConfiguration()

class IgnoredTypesHandler(YasHandler):
    def test(self, data):
        if data.get('type') in config.ignored_types:
            return True

    def handle(self, data, _):
        pass
