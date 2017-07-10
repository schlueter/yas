from yas import YasHandler


class HelpHandler(YasHandler):
    triggers = ['help']

    def setup(self):
        self.help_texts = dict()
        self.unaliased_commands = []
        for handler in self.bot.handler_list:
            self.bot.log.debug(f"checking {handler} for triggers variable")
            if hasattr(handler, 'triggers') and handler.__doc__:
                self.unaliased_commands.append(handler.triggers[0])

                aliases = ''
                if len(handler.triggers) > 1:
                    aliases = f"Aliases: `{', '.join(handler.triggers)}`"

                for trigger in handler.triggers:
                    self.help_texts[trigger] = handler.__doc__ + aliases

        self.bot.log.debug(f"Found help texts {self.help_texts}")

    def test(self, data):
        bot_id = self.bot.retrieve_user_id(self.bot.config.bot_name)
        message_words = [element for element in data.get('text', '').split(' ')
                         if element != "<@" + bot_id + ">"]

        if 'help' == message_words[0]:
            self.message_words = set(message_words)
            return True
        else:
            return False

    def handle(self, data, reply):
        requested_help_texts = self.message_words.difference(set(self.triggers))
        if not requested_help_texts:
            return reply(f"Documented commands: `{', '.join(self.unaliased_commands)}`\n\n" +
                         f"Use `help <command> [<command> ..]` for help with specific commands.\n")
        for word in requested_help_texts:
            if word in self.help_texts.keys():
                reply(f"*`{word}`*: {self.help_texts[word]}" + "\n\n")
