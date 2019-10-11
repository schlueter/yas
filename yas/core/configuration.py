FILE_NAME = 'etc/yas/yas.yml'

PARAMETERS = dict(
    ignored_types=['desktop_notification', 'user_typing'],
    slack_app_token=None,
    bot_name=None,
    handler_list=[
        'yas.handlers.ignored_types_handler.',
        'yas.handlers.not_talking_to_bot_handler.',
        'yas.handlers.help_handler.',
        'yas.handlers.identify_handler.',
        'yas.handlers.rules_handler.',
        'yas.handlers.default_handler.'
    ],
    debug=False,
    default_response='Sure...write some more code then I can do that!',
    log_level='WARN',
    handler_exception_message="Err, sorry, that threw an exception: " +
    "{exception}. Try again or reach out to the maintainers."
)
