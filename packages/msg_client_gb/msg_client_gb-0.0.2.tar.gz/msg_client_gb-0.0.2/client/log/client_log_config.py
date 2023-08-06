import sys
import os
from logging import Formatter, StreamHandler, getLogger, FileHandler, INFO
from common.settings import LOGGING_LEVEL

sys.path.append('/')
# формировщик логов
CLI_FORMATTER = Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# путь к лог файлу
PATH = os.getcwd()
PATH = os.path.join(PATH, 'log', 'client.log')


# поток вывода логов в консоль
CONSOLE_LOG = StreamHandler(sys.stderr)
CONSOLE_LOG.setFormatter(CLI_FORMATTER)
CONSOLE_LOG.setLevel(INFO)

# поток вывода логов в файл
FILE_LOG = FileHandler(PATH, encoding='utf-8')
FILE_LOG.setFormatter(CLI_FORMATTER)

# настройка логгера
LOG = getLogger('client_logger')
LOG.addHandler(CONSOLE_LOG)
LOG.addHandler(FILE_LOG)
LOG.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOG.critical('Критическая ошибка')
    LOG.error('Ошибка')
    LOG.debug('Отладка')
    LOG.info('Информационное сообщение')
