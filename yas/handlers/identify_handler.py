import socket

from yas import RegexHandler


class IdentifyHandler(RegexHandler):
    """`id` is replied to with information about the bot."""
    triggers = ['id']

    def __init__(self, bot):
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.connect(("8.8.8.8", 80))
        self.ip_address = soc.getsockname()[0]
        self.hostname = socket.gethostbyaddr(socket.gethostname())[0]
        super().__init__(r'^id', bot)

    # Pylint thinks this method could be a function because it does not use `self`.
    # In fact, this class must meet a specification which requires a method `handle`,
    # but that method need not access
    # pylint: disable=no-self-use
    def handle(self, _, reply):
        reply(f"My host is {self.hostname} at {self.ip_address}.")
