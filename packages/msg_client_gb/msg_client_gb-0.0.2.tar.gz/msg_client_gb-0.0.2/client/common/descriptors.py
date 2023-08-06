import sys
from logging import getLogger
from ipaddress import ip_address

LOGGER = getLogger('server_logger')


class Port:
    """
    Класс - дескриптор, проверяющий номер порта. Порт должен быть в диапазоне
    с 1024 по 65536.
    """

    def __set__(self, unit, value):
        if not 1023 < value < 65536:
            LOGGER.critical(
                f'Попытка запуска сервера. Недопустимый номер пора {value}.'
                f'Номер порта должен быть в пределах от 1024 по 65535.')
            sys.exit(1)
        else:
            unit.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class IPAddress:
    """
    Класс - дескриптор. Проверяет на корректность IP адрес, передаваемый
    в аргументах при запуске клиентской программы.
    """
    def __set__(self, unit, value):
        try:
            ip_address(value)
        except ValueError:
            LOGGER.critical(
                f'В качестве аргумента было передано значение {value}, '
                f'которое не является IP адресом.'
                f' Проверьте правильность ввода.')
            sys.exit(1)
        else:
            unit.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
