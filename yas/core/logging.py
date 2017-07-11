import logging

from systemd import journal


class Logger:

    def __init__(self, log_level='WARNING'):
        self.log = logging.getLogger('yas')
        self.log.addHandler(journal.JournaldLogHandler())
        self.log.setLevel(logging._nameToLevel[log_level])
