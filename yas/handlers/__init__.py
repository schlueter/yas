import re
import sys
from pprint import pformat

class HandlerError(Exception):
    pass

def log(*msg): print(*msg, file=sys.stderr)

def list_handler(search_opts, result_fields):
    log(f'Received search request {search_opts}\nfor fields result_fields')
    if search_opts:
        search_opts = dict([opt.split('=') for opt in search_opts.split(' ')])
    else:
        search_opts = {}

    if result_fields:
        result_fields.split(',')
    else:
        result_fields = ['name', 'tags', 'description', 'status', 'addresses']
    log(f'Initiating search')

    return pformat((search_opts, result_fields))

def create_handler(name, branch):
    log(f'Received request to create {name} on {branch}')
    log(f'Creating {name}')
    response = f'Requested creation of {name}'
    if branch:
        response += 'on {branch}'
    return response


def delete_handler(name):
    log(f'Received request to delete {name}')
    log(f'Deleted {name}')
    return f'Successfully deleted {name}.'

handlers = {
    re.compile('(?:list)\ ?([a-z\.=,]+)?(?:\ fields\ )?([\-a-zA-Z0-9\,_]+)?'): list_handler,
    re.compile('(?:launch|start|create)\ ([-\w]+)(?:\ on\ )?([-\w]+:?[-\w]+)?'): create_handler,
    re.compile('(?:delete|drop|terminate|bust a cap in|pop a cap in) ([-\ \w]+)'): delete_handler
}

def handler(data, reply):
    for regex in handlers:
        match = regex.match(data.get('text'))
        if match:
            groups = match.groups()
            return reply(handlers[regex](*groups))
    else:
        raise HandlerError("Sure...write some more code then I can do that!")
