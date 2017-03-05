FILE_NAME = 'etc/yas/yas.yml'

PARAMETERS = dict(
    ignored_types=['desktop_notification', 'user_typing'],
    slack_app_token=None,
    bot_name=None,
    handler_list=['yas.default_handler'],
    debug=False,
    default_response='Sure...write some more code then I can do that!',
    log_level='WARN'
)
