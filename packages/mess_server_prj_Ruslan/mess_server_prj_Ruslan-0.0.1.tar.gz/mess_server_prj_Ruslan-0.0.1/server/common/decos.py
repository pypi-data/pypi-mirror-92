"""Logger decorators"""

import sys
import logging

import traceback
import inspect

if sys.argv[0].find('client') == -1:
    LOG = logging.getLogger('server_log')
else:
    LOG = logging.getLogger('client_log')


def log(func):
    """Decorating logger function"""
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        LOG.info(
            f'Была вызвана функция {func.__name__}, с параметрами:\n{args} {kwargs}.'
            f'\nВызов из модуля {func.__module__}. '
            f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}. '
            f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
        return ret

    return wrapper


class Log:
    """Decorating logger class"""
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            LOG.info(
                f'Была вызвана функция {func.__name__}, с параметрами:\n{args} {kwargs}.'
                f'\nВызов из модуля {func.__module__}. '
                f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}. '
                f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
            return ret

        return wrapper
