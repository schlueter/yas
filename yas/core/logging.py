#pylint: disable=no-self-use
from datetime import datetime
import inspect

class Logger:
    def __init__(self, level):
        pass

    def __log(self, *msg):
        now = datetime.now()
        method_name = inspect.stack()[1].function
        print(now, '[' + method_name.upper() + ']', *msg)

    def debug(self, *msg): self.__log(*msg)
    def warn(self, *msg): self.__log(*msg)
    def fatal(self, *msg): self.__log(*msg)
    def info(self, *msg): self.__log(*msg)
    def error(self, *msg): self.__log(*msg)
