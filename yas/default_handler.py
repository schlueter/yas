from yas import YasHandler, HandlerError
from yas.yaml_file_config import YamlConfiguration


config = YamlConfiguration()

class DefaultHandler(YasHandler):
    '''
    YasHandlers, when registered with a Yas installation in the active yas.yml,
    are tested against, and upon matching applied to, incoming messages by Yas
    as they are receieved.
    '''

    def test(self, data):
        '''
        If this method returns truthy, this class's handle method is called with the data.
        By default, this handler is registered with yas. To disable, remove
        yas.handler from the handler_list in your yas.yml.

        Arguments:

        data :: dict :: An event from the slack RTM websocket. To see the raw
            stream, enable the raw_response handler. The objects are pre filtered by
            the yas client's data_filter method, which by default filters out any
            ignored types from the yas config, objects not associated with a
            channel, and objects originating from the bot. The implementation of this
            behaviour is likely to change in the future, but the default filters are not.
        '''
        return True

    def handle(self, data, reply):
        '''
        Handles a matched data object. If a HandlerError is raised here, it will be caught,
        and its message sent to the originating channel; other errors are not caught and
        will crash yas, which shouldn't be a problem if one of the included daemon scripts
        is used as they will restart yas after a crash.

        Arguments:

        data :: dict :: See test.

        reply :: function(response, channel=channel, thread=None, reply_broadcast=None) ::
            A shortcut function to reply to a message. The response is your message back
            to the channel. The channel, which defaults to the data's channel, is where
            the message will be delivered; besides the default, another useful channel
            is the data's originating user, which would direct message that user. The
            thread is the parent message ID, if you wish to initiate a thread.
            The reply_broadcast argument takes a boolean value and indicates whether a
            threaded message should also reply in the parent channel.

        api_call :: function(method, timeout=None, **kwargs) :: The api_call method of
            the yas client listening for messages. This is provided so that handler
            authors may shoot themselves in the foot. Available methods may be found
            at https://api.slack.com/methods. This function may be restricted or
            removed in the future as it is rather dangerous.

        handler_manager :: yas.handler.HandlerManager :: The HandlerManager instance
            the YasHandler instance is bound to. This is provided so that query response
            listeners may be registered. This argument may be replaced in the future with
            something more explicit.
        '''
        reply(config.default_response)
