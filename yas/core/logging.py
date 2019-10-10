#pylint: disable=no-self-use
from datetime import datetime

class Logger:
    def __init__(self, level):
        pass

    def debug(self, msg):
        now = datetime.now()
        print(f"{now} [DEBUG] {msg}")

    def warn(self, msg):
        now = datetime.now()
        print(f"{now} [WARN] {msg}")

    def fatal(self, msg):
        now = datetime.now()
        print(f"{now} [FATAL] {msg}")

    def info(self, msg):
        now = datetime.now()
        print(f"{now} [INFO] {msg}")
