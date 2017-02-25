import os
import re
import sys
import time

from slackclient import SlackClient

from slackbot.handlers import handlers

class SlackClientFailure(Exception):
    pass

def log(*msg): print(*msg, file=sys.stderr)

BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_NAME = os.environ.get('SLACK_BOT_NAME')
READ_WEBSOCKET_DELAY = float(os.environ.get('READ_WEBSOCKET_DELAY', 1))

class Client(SlackClient):

    def __init__(self):
        super().__init__(BOT_TOKEN)
        self.bot_id = self.__retrieve_bot_user_id()
        self.at_bot = "<@" + self.bot_id + ">"

    def __retrieve_bot_user_id(self):
        log("Retrieving users list.")
        api_call = self.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            log(f"Pulling the ID for the bot, {BOT_NAME}.")
            for user in users:
                if 'name' in user and user.get('name') == BOT_NAME:
                    return user.get('id')
            else:
                raise NoBot("could not find bot user with the name " + BOT_NAME)
        else:
            raise SlackClientFailure()

    def handle_command(self, command, channel):
        """
            Receives commands directed at the bot and determines if they
            are valid commands. If so, then acts on the commands. If not,
            returns back what it needs for clarification.
        """

        log(f'handling {command}')
        for regex in handlers:
            match = regex.match(command)
            if match:
                groups = match.groups()
                return self.reply(channel, handlers[regex](*groups))
        else:
            return "Sure...write some more code then I can do that!"

    def reply(self, channel, response):
        return self.api_call(
            "chat.postMessage",
            channel=channel,
            text=response,
            as_user=True
        )

    def parse_slack_output(self, rtm_output):
        """
            The Slack Real Time Messaging API is an events firehose.
            this parsing function returns None unless a message is
            directed at the Bot, based on its ID.
        """
        if rtm_output and len(rtm_output) > 0:
            for output in [output for output in rtm_output
                              if output
                                  and 'channel' in output
                                  and 'text' in output
                                  and not output.get('user') == self.bot_id]:
                channel_info = self.api_call('channels.info', channel=output.get('channel'))
                if channel_info.get('ok', False) and AT_BOT in output['text']:
                    log(f"receieved message in {output['channel']} from {output['user']}: {output['text']}")
                    return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
                group_info = self.api_call('groups.info', channel=output.get('channel'))
                if not channel_info.get('ok', False) and not group_info.get('ok', False):
                    log(f"receieved direct message from {output['user']}: {output['text']}")
                    return output['text'].strip().lower(), output['channel']
        return None, None

    def listen(self):
        if self.rtm_connect():
            log("Slack bot connected as {}<{}> and running!".format(BOT_NAME, self.bot_id))
            while True:
                command, channel = self.parse_slack_output(self.rtm_read())
                if command and channel:
                    self.handle_command(command, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            log("Connection failed. Invalid Slack token or bot ID?")

def main():
    client = Client()
    client.listen()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log('Caught keyboard interrupt, exiting...')
        exit()
