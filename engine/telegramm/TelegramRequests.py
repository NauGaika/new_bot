import pprint

from .TelegramRequestsMethod import TelegramRequestsMethod
from .TelegramRequestsProperty import TelegramRequestsProperty
from .TelegramRequestsInline import TelegramRequestsInline


class TelegramRequests(TelegramRequestsMethod, TelegramRequestsProperty, TelegramRequestsInline):
    """Класс по работе с запросами на телегу."""
    token = None

    def __init__(self, update):
        self.obj = update

    def print_obj(self):
        print('')
        pprint.pprint(self.obj)