import imp
import inspect
import sys

from yas import YasHandler, NotAHandler, HandlerError
from yas.logging import log



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

def is_handler(test_class):
    log.info(f"Checking if {test_class} is a handler")
    public_methods = [
        member[0] for member in inspect.getmembers(test_class)
        if not member[0].startswith('__')
    ]

    class_derives_yas_handler = str(YasHandler) in [str(base) for base in test_class.__bases__]
    class_defines_required_methods = 'handle' in public_methods and 'test' in public_methods
    log.info(f"{'✔' if class_derives_yas_handler else '✘'} {test_class} derives {YasHandler}")
    log.info(f"{'✔' if class_defines_required_methods else '✘'} {test_class} defines required methods")
    return class_derives_yas_handler and class_defines_required_methods

def find_handlers_in_module(handler_module):
    return [handler[1]() for handler in inspect.getmembers(handler_module, inspect.isclass)
            if is_handler(handler[1])]

class HandlerManager:
    def __init__(self, handler_list, debug=False):

        log.info(f"Loading handlers from {handler_list}")

        self.handler_list = []
        for handler_name in handler_list:
            log.info(f"Searching for {handler_name}")
            try:

                handler = import_from_dotted_path(handler_name)
                if type(handler) is type and is_handler(handler):
                    log.info(f"Found handler {handler}.")
                    self.handler_list.append(handler())
                    continue

                module_handlers = find_handlers_in_module(handler)
                if module_handlers:
                    log.info(f"Found handlers in {handler_name}: {module_handlers}")
                    self.handler_list.extend(module_handlers)
                    continue

                raise NotAHandler(handler_name)

            except Exception as exception:
                log.warn(f'Failed to load handler {handler_name}, caught: {exception}')
                if debug:
                    raise exception

        log.info(f'Loaded handlers: {self.handler_list}')

    def handle(self, data, reply):
        log.info(f"Handling {data['yas_hash']}")
        for handler in self.handler_list:
            if handler.test(data):
                handler.handle(data, reply)
            break
        else:
            log.info(f'No handler found for {data}')
