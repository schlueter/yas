# YAS
###### Yet Another Slack bot
The operations team at Refinery29 was replacing a old system for
launching development systems which utilized an older version of
[Hubot](https://hubot.github.com/). At the time our team was more
comfortable with python than the Node/Coffeescript which Hubot is
built on, and we were already familiar with python modules with
which we could interface with the systems we wanted our new bot to
interact with. Thus YAS was born.

YAS is framework which tests Slack messages which are available to
it against handlers which will operate on a message if they are the
first handler to produce a truthy result upon running a test
against the message. A simple practical example is the built in id
handler. This handler has a test which looks for a message
starting with `id`. If it does, the handler is invoked, replying
with some information about the server yas is running on.

Slack has a number of message types of which only a few are
initiated by a user and in most cases only a subset of user
initiated messages will be meant to be handled by your bot. To
handle these cases a number of handlers are included with yas, but
are not automatically added, and must be included in the list of
handlers when that is configured.

## Setup
Yas may be run directly, but it won't do much, so setup including
one or more additional handlers will be included here.

The easiest method (as of version 2.0) is to construct a Docker
image based on the yas image and install the additional handlers
and configure them. Alternatively, if any of the handlers has a
Dockerfile available, that could be used as a base on which to
add any others, but since Docker files need to be manually
combined it is likely easier to simply construct a new image
based directly on yas'. For instance, the yas-jenkins handler
can be built with a Dockerfile such as:

```
FROM schlueter/yas:latest

ENV YAS_JENKINS_JOBS '{}'
ENV YAS_JENKINS_URL ''
ENV YAS_JENKINS_USERNAME ''
ENV YAS_JENKINS_PASSWORD ''

COPY . .
RUN python -m pip install yas-jenkins
```

To add an additional handler, its configuration need only be added
and it installed as well.

Once built, the resulting image may be run with the appropriate
configuration provided in environment variables with:

```
docker run --rm --tty \
 --env YAS_SLACK_TOKEN=xoxb-XXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXX \
 --env YAS_BOT_NAME=yas \
 --env YAS_JENKINS_URL=https://jenkins.example.com \
 --env YAS_JENKINS_USERNAME=yas \
 --env YAS_JENKINS_PASSWORD=supersecret \
 --env YAS_JENKINS_JOBS='{"MyJob": "build (?P<branch>\\w+)"}' \
 --env YAS_HANDLER_LIST=yas.handlers.ignored_types_handler.,yas.handlers.not_talking_to_bot_handler.,yas.handlers.help_handler.,yas.handlers.identify_handler.,YasJenkinsHandler.,yas.handlers.rules_handler.,yas.handlers.default_handler. \
 my-yas-image:my-tag
```

For yas to function, the `YAS_SLACK_TOKEN`, `YAS_BOT_NAME`, and
`YAS_HANDLER_LIST` variables must be provided. The token and name
must be obtained/configured from a new or existing bot in your
Slack organization. A new bot may be created at
https://my.slack.com/services/new/bot.

The handler list should include most of the default handlers,
potentially discluding those not being generally necessary to
yas' normal functioning being the identify_handler, rules_handler, and
the default_handler. The help_handler is also not necessary to yas
operating in a reasonable manner, but it may be utilized by other
plugins to make help functionality available.





