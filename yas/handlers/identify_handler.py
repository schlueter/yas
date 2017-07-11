import socket

from yas import RegexHandler


class IdentifyHandler(RegexHandler):
    """`id` is replied to with information about the bot."""
    triggers = ['id']

    def __init__(self, bot):
        super().__init__(r'^id', bot)

    def handle(self, _, reply):
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.connect(("8.8.8.8", 80))
        my_ip = soc.getsockname()[0]
        my_hostname = socket.gethostbyaddr(socket.gethostname())[0]
        reply(f"My host is {my_hostname} at {my_ip}.")
