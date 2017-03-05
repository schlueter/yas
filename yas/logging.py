import logging
from systemd import journal
from yas.yaml_file_config import YamlConfiguration


config = YamlConfiguration()

class Logger:

    def __init__(self, log_level='WARNING'):
        self.log = logging.getLogger('yas')
        self.log.addHandler(journal.JournaldLogHandler())
        self.log.setLevel(logging._nameToLevel[log_level])

logger = Logger(config.log_level)

def log(level_str, msg):
    level = logging._nameToLevel[level_str]
    logger.log.log(level, msg)
