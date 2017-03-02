import re
import sys
from pprint import pformat

from yas import YasHandler, log


def log(*msg):
    print(*msg, file=sys.stderr)

class ExampleHandler(YasHandler):

    def __init__(self):
        self.handlers = {
            re.compile('(?:list)\ ?([a-z\.=,]+)?(?:\ fields\ )?([\-a-zA-Z0-9\,_]+)?'): self.list_handler,
            re.compile('(?:launch|start|create)\ ([-\w]+)(?:\ on\ )?([-\w]+:?[-\w]+)?'): self.create_handler,
            re.compile('(?:delete|drop|terminate|bust a cap in|pop a cap in) ([-\ \w]+)'): self.delete_handler
        }

    def test(self, data):
        for regexp in self.handlers:
            if regexp.match(data.get('text')):
                return True

    def handle(self, data, reply, api_call, handler_manager):
        for regex in self.handlers:
            match = regex.match(data.get('text'))
            if match:
                groups = match.groups()
                return reply(self.handlers[regex](*groups))
        else:
            raise HandlerError("ExampleHandler does not understand")

    def list_handler(self, search_opts, result_fields):
        if search_opts:
            search_opts = dict([opt.split('=') for opt in search_opts.split(' ')])
        else:
            search_opts = {}

        if result_fields:
            result_fields.split(',')
        else:
            result_fields = ['name', 'tags', 'description', 'status', 'addresses']

        return pformat((search_opts, result_fields))

    def create_handler(self, name, branch):
        response = f'Requested creation of {name}'
        if branch:
            response += 'on {branch}'
        return response


    def delete_handler(self, name):
        return f'Successfully deleted {name}.'


