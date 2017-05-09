import socket

from yas import RegexHandler
from yas.yaml_file_config import YamlConfiguration


CONFIG = YamlConfiguration()

class IdentifyHandler(RegexHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(r'id', *args, **kwargs)

    def handle(self, data, reply):
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.connect(("8.8.8.8", 80))
        my_ip = soc.getsockname()[0]
        my_hostname = socket.gethostbyaddr(socket.gethostname())[0]
        reply(f"My host is {my_hostname} at {my_ip}.")
