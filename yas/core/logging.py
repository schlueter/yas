import logging

class Logger:

    def __init__(self, log_level='WARNING'):
        self.log = logging.getLogger('yas')
        self.log.setLevel(logging._nameToLevel[log_level])
