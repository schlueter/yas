import imp
import inspect
import sys
import traceback

from yas import YasHandler


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

def get_ancestors(target_class):
    bases = []
    if target_class is not object:
        for base in target_class.__bases__:
            bases.extend(get_ancestors(base))

    bases.extend(target_class.__bases__)
    return bases


class HandlerManager:

    def __init__(self, config, api_call, log):

        self.config = config
        self.api_call = api_call
        self.log = log
        self.users_list = self.__retrieve_users_list()
        self.log.info(f"Loading handlers from {self.config.handler_list}")

        handler_class_list = []
        for handler_name in self.config.handler_list:

            self.log.info(f"Searching for {handler_name}")
            handler = import_from_dotted_path(handler_name)

            if type(handler) is type and self.is_handler(handler):
                self.log.info(f"Found handler {handler}.")
                handler_class_list.append(handler)
                continue

            module_handlers = self.find_handlers_in_module(handler)
            if module_handlers:
                self.log.info(f"Found handlers in {handler_name}: {module_handlers}")
                handler_class_list.extend(module_handlers)
                continue

            self.log.warn(f"{handler_name} is not a handler.")

        self.handler_list = []
        self.handler_list.extend(self.instantiate_handlers(handler_class_list))
        self.setup_handlers(self.handler_list)

        self.log.info(f'Loaded handlers: {self.handler_list}')

    def find_handlers_in_module(self, handler_module):
        return [handler[1] for handler in inspect.getmembers(handler_module, inspect.isclass)
                if self.is_handler(handler[1])]


    def is_handler(self, test_class):
        self.log.info(f"Checking if {test_class} is a handler")
        methods = [member[0] for member in inspect.getmembers(test_class)]

        test_class_bases = get_ancestors(test_class)
        self.log.debug(f"{test_class} has bases {test_class_bases}")

        class_derives_yas_handler = str(YasHandler) in [str(base) for base in test_class_bases]
        class_defines_required_methods = 'handle' in methods and 'test' in methods

        check_or_x = {True: '✔', False: '✘'}

        self.log.info(f"{check_or_x[class_derives_yas_handler]} {test_class} derives YasHandler")
        self.log.info(f"{check_or_x[class_defines_required_methods]} {test_class} defines required methods")

        return class_derives_yas_handler and class_defines_required_methods

    def instantiate_handlers(self, handler_classes):
        handlers = []
        for handler_class in handler_classes:
            try:
                new_handler = handler_class(self)
                handlers.append(new_handler)
            except Exception as exception:
                self.log.error(f'Failed to load handler {handler_class}, caught:\n{traceback.format_exc()}')
                if self.config.debug:
                    raise exception

        return handlers

    def setup_handlers(self, handlers):
        for handler in handlers:
            try:
                handler.setup()
            except Exception as exception:
                self.log.error(f'Failed to setup handler {handler}, caught:\n{traceback.format_exc()}')
                if self.config.debug:
                    raise exception

        return handlers

    def __retrieve_users_list(self):
        self.log.info("Retrieving users list...")
        api_call = self.api_call("users.list")
        if not api_call.get('ok'):
            raise SlackClientFailure("Unable to query api! This is usually due to an incorrect api key, please check your yas config.")
        return api_call.get('members')

    def retrieve_user_id(self, username):
        for user in self.users_list:
            if 'name' in user and user.get('name') == username:
                return user.get('id')
        else:
            raise NoSuchUser(self.bot_name)

    def retrieve_user_info(self, user_id):
        try:
            creator_info = self.api_call('users.info', user=user_id)
        except Exception as e:
            self.log.warn(f"Caught {e} while retrieving creator_info.")
            creator_info = None
        return creator_info

    def handle(self, data, reply):
        self.log.debug(f"Considering {data}")
        for handler in self.handler_list:
            self.log.debug(f"Testing {data['yas_hash']} against {handler}")
            if handler.test(data):
                self.log.info(f"Handling {data['yas_hash']} with {handler}")
                try:
                    handler.handle(data, reply)
                except Exception as exception:
                    self.log.error(f"Caught {exception} while handling {data['yas_hash']} with {handler}:\n{traceback.format_exc()}")
                    raise exception
                break
        else:
            self.log.info(f'No handler found for {data}')
