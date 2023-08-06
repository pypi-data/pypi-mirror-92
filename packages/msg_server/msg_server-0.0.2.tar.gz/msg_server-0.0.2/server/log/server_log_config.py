import sys
import os
from logging import Formatter, StreamHandler, handlers, getLogger, INFO
from common.settings import LOGGING_LEVEL

# формировщик логов
SERV_FORMATTER = Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s')

# путь к лог файлу
PATH = os.getcwd()
PATH = os.path.join(PATH, 'log', 'server.log')


# поток вывода логов в консоль
CONSOLE_LOG = StreamHandler(sys.stderr)
CONSOLE_LOG.setFormatter(SERV_FORMATTER)
CONSOLE_LOG.setLevel(INFO)

# поток вывода логов в файл
FILE_LOG = handlers.TimedRotatingFileHandler(PATH, encoding='utf-8',
                                             interval=1, when='D')
FILE_LOG.setFormatter(SERV_FORMATTER)

# настройка логгера
LOG = getLogger('server_logger')
LOG.addHandler(CONSOLE_LOG)
LOG.addHandler(FILE_LOG)
LOG.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOG.critical('Критическая ошибка')
    LOG.error('Ошибка')
    LOG.debug('Отладка')
    LOG.info('Информационное сообщение')
