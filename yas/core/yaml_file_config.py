import os
import sys

import yaml

from . import configuration


class YamlConfigError(Exception):
    pass

class RequiredParameter(YamlConfigError):
    '''{parameter} is a required configuration parameter and must be set to a non empty value. Please correct this in your configuration file at {config_file}.'''
    def __init__(self, parameter, config_file):
        self.message = self.__doc__.format(parameter=parameter, config_file=config_file)

class YamlConfiguration(object):

    def __parse_config(self, config_file_path):
        with open(config_file_path, 'r') as config_file:
            raw_config = yaml.load(config_file)

            parameters = configuration.PARAMETERS
            for parameter in parameters:
                default = parameters[parameter]
                value = raw_config.get(parameter, default)

                if not value and default is None:
                    raise RequiredParameter(parameter, config_file_path)

                setattr(self, parameter, value)

    def __init__(self):
        config_file = os.path.join(sys.prefix, configuration.FILE_NAME)
        self.__parse_config(config_file)
