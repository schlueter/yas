# pylint: disable=unused-import
from slackclient._server import SlackConnectionError, SlackLoginError

class SlackClientNotOk(Exception):
    pass

class NoSuchUser(Exception):
    pass
