FROM python:alpine

ENV YAS_SLACK_TOKEN ''
ENV YAS_DEBUG ''
ENV YAS_BOT_NAME 'YAS'

COPY . .
RUN python setup.py install && rm -rf build dist
CMD yas
