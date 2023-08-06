import sys
from logging import getLogger

import inspect

if 'client.py' in sys.argv[0]:
    LOGGER = getLogger('client_logger')
else:
    LOGGER = getLogger('server_logger')


# для примера использовал как декоратор в client.py
def log(decorate_it):
    """
    Декоратор, выполняющий логирование вызовов функций.
    Сохраняет события типа debug, содержащие
    информацию о имени вызываемой функиции, параметры с которыми
    вызывается функция, и модуль, вызывающий функцию.
    """

    def wrap(*args, **kwargs):
        result = decorate_it(*args, **kwargs)
        LOGGER.debug(f'Функция {decorate_it.__name__} '
                     f'была вызвана с аргументами: {args}, {kwargs}. '
                     f'Вызов происходит из функции {inspect.stack()[1][3]}.',
                     stacklevel=2)
        return result

    return wrap


# для примера использовал как декоратор в server.py
class Log:
    def __call__(self, decorate_it):
        def wrap(*args, **kwargs):
            result = decorate_it(*args, **kwargs)
            LOGGER.debug(f'Функция {decorate_it.__name__} '
                         f'была вызвана с аргументами: {args}, {kwargs}. '
                         f'Вызов происходит из функции {inspect.stack()[1][3]}',
                         stacklevel=2)
            return result

        return wrap
