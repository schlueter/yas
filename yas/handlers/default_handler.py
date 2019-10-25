import os

from yas import YasHandler


class DefaultHandler(YasHandler):
    '''The default handler replys to everything with the default response as defined in the bot config'''
    triggers = ["default"]

    '''
    YasHandlers, when registered with a Yas installation in the active yas.yml,
    are tested against, and upon matching applied to, incoming messages by Yas
    as they are receieved.
    '''

    test = lambda _, __: True

    def __init__(self, bot):
        super().__init__(bot)
        self.default_response = os.environ.get(
            'YAS_DEFAULT_RESPONSE',
            'Sure...write some more code then I can do that!'
        )

    def handle(self, _, reply):
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
        reply(self.default_response)
