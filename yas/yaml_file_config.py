import os

import yaml

from . import configuration


def find_config():
    for directory in configuration.DIRECTORIES:
        potential_config_file = os.path.join(directory, configuration.FILE_NAME)
        if os.path.isfile(potential_config_file):
            return potential_config_file

    raise NoConfigFileFound

class YamlConfigError(Exception):
    pass


class NoConfigFileFound(YamlConfigError):
    '''No config file found in search path. Please add a config file, {config_file_name}, to one of the following directories:

{fdirectories}

The first one found will be used. The following parameters are available, "None" values must be populated:

{fparameters}'''

    def __init__(self):
        fdirectories = '\n'.join([f'- {directory}' for directory in configuration.DIRECTORIES])
        raw_parameters = configuration.PARAMETERS
        fparameters = '\n'.join([f'{key}: {raw_parameters[key]}' for key in raw_parameters])
        super().__init__(self.__doc__.format(fdirectories=fdirectories,
                                           fparameters=fparameters,
                                           config_file_name=configuration.FILE_NAME))

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
        config_file = find_config()
        self.__parse_config(config_file)
