How to use Handlers
===================

Yas uses handlers to manage interactions on slack. A handler is a pair of functions, a test, which is checked against data packets from the Slack rtm stream, and an action which is applied to the data packets if the test is positive.

Slack rtm data packets are filtered before they are tested against handlers. The default data filter Yas applies removes from consideration data packets of any type in the Yas configuration's ignored_types list, those without a channel, and events initiated by the bot itself. It also checks if messages were directed at the bot, either in a shared channel by @-messaging the bot, or a direct message.

Handlers are then tested against the data in the order they exist in the configuration and the first match is given the data to take action against. A default catch all handler exists which replys to all messages with the default response in the configuration.
