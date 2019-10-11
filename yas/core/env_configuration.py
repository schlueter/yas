import os
import sys

DEFAULTS = dict(
    ignored_types=[
        'desktop_notification',
        'user_typing',
        'presence_change',
        'reconnect_url',
        'hello'
    ],
    handler_list=[
        'yas.handlers.ignored_types_handler.',
#        'yas.handlers.not_talking_to_bot_handler.',
        'yas.handlers.help_handler.',
        'yas.handlers.identify_handler.',
        'yas.handlers.rules_handler.',
        'yas.handlers.default_handler.'
    ],
    default_response='Sure...write some more code then I can do that!',
    log_level='WARN',
    handler_exception_message=(
        "Err, sorry, that threw an exception: {exception}. "
        "Try again or reach out to the maintainers."
    )
)

class EnvConfiguration:

    def __init__(self):
        self.slack_token = os.environ.get('YAS_SLACK_TOKEN')
        if not self.slack_token:
            print('YAS_SLACK_TOKEN required. Exitting.', file=sys.stderr)
            sys.exit(3)

        self.debug = os.environ.get('YAS_DEBUG')
        self.bot_name = os.environ.get('YAS_BOT_NAME', 'YAS')
        self.log_level = os.environ.get('YAS_LOG_LEVEL', DEFAULTS['log_level'])
        self.default_response = os.environ.get(
            'YAS_DEFAULT_RESPONSE',
            DEFAULTS['default_response']
        )
        self.handler_exception_message = os.environ.get(
            'YAS_HANDLER_EXCEPTION_MESSAGE',
            DEFAULTS['handler_exception_message']
        )
        self.ignored_types = (os.environ.get('YAS_IGNORED_TYPES', '').split(',').remove('')
                              or DEFAULTS['ignored_types'])
        self.handler_list = (os.environ.get('YAS_HANDLER_LIST', '').split(',').remove('')
                             or DEFAULTS['handler_list'])
        if self.debug:
            print('Configuration:\n', self.__dict__)
