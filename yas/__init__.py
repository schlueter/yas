import re

from yas.yaml_file_config import YamlConfiguration
from yas.logging import logger, log


class YasHandler:

    def __init__(self, bot_name, api_call, log=log):
        self.bot_name = bot_name
        self.api_call = api_call
        self.log = log
        self.all_users = self.__retrieve_users_list()

    def __retrieve_users_list(self):
        self.log("INFO", "Retrieving users list...")
        api_call = self.api_call("users.list")
        if not api_call.get('ok'):
            raise SlackClientFailure("Unable to query api! This is usually due to an incorrect api key, please check your yas config.")
        return api_call.get('members')

    def __retrieve_user_id(self, username):
        for user in self.all_users:
            if 'name' in user and user.get('name') == username:
                return user.get('id')
        else:
            raise NoSuchUser(self.bot_name)

    def __get_user_info(self, user_id):
        try:
            creator_info = self.api_call('users.info', user=user_id)
        except Exception as e:
            self.log('WARN', f"Caught {e} while retrieving creator_info.")
            creator_info = None
        return creator_info


class YasError(Exception):
    def __init__(self, msg):
        logger.log.fatal(msg)

class HandlerError(YasError):
    def __init__(self, msg):
        logger.log.warn(msg)

class RegexHandler(YasHandler):

    def __init__(self, regexp_string, bot_name, api_call, log=print):
        super().__init__(bot_name, api_call, log=log)
        self.regexp = re.compile(regexp_string)
        self.log('INFO', f"{self.__class__} initialized and matching {regexp_string}!")

    def test(self, data):
        self.current_match = self.regexp.search(data.get('text'))
        return self.current_match

class NoSuchUser(YasError):
    def __init__(self,msg):
        logger.log.warn(msg)

class SlackClientFailure(YasError):
    pass
