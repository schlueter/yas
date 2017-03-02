import imp
import inspect
import sys


def log(*msg):
    print(*msg, file=sys.stderr)

def import_from_dotted_path(dotted_names, path=None):
    """ import_from_dotted_path('foo.bar') -> from foo import bar; return bar

    This function borrowed from Chase Seibert at
    http://chase-seibert.github.io/blog/2014/04/23/python-imp-examples.html
    """
    next_module, remaining_names = dotted_names.split('.', 1)
    file, pathname, description = imp.find_module(next_module, path)
    module = imp.load_module(next_module, file, pathname, description)

    if hasattr(module, remaining_names):
        return getattr(module, remaining_names)

    if '.' not in remaining_names:
        return module

    return import_from_dotted_path(remaining_names, path=module.__path__)

def is_valid_handler(handler):
    public_methods = [
        member[0] for member in inspect.getmembers(test_class)
        if not member[0].startswith('__')
    ]

    class_inherits_yas_handler = YasHandler in test_class.__bases__
    class_defines_required_methods = 'handle' in public_methods and 'test' in public_methods

    return class_inherits_yas_handler and class_defines_required_methods

class Handler:

    def __init__(self, handler_class):
        self.handler_class = import_from_dotted_path(handler_class)
        self.instance = self.handler_class()
        self.test = self.instance.test
        self.handle = self.instance.handle


class HandlerManager:
    def __init__(self, handler_list):
        self.handler_list = []
        for handler_class in handler_list:
            try:
                self.handler_list.append(Handler(handler_class))
            except Exception as e:
                log(f'Failed to load handler {handler_class}, caught: {e}')


    def handle(self, data, reply, api_call):
        for handler in self.handler_list:
            if handler.test(data):
                handler.handle(data, reply, api_call, self)
            break
        else:
            log(f'No handler found for {data}')
