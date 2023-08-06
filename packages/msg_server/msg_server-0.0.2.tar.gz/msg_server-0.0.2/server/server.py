import sys
import os
from logging import getLogger

import configparser
from argparse import ArgumentParser
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

import log.server_log_config
from common.settings import *
from common.decos import Log
from server.server_database import ServerStorage
from server.server_core import Server
from server.main_window import MainWindow

SERV_LOGGER = getLogger('server_logger')


@Log()
def srv_arguments_parser(default_port, default_address):
    """
    Разбор аргументов, переданных в командной строке.
    Пример вызова:
    server.py -p 8888 -a 192.168.1.2 --no_gui
    :return:
    """
    SERV_LOGGER.debug(
        f'Инициализация парсера аргументов коммандной строки: {sys.argv}')
    parser = ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    args_list = parser.parse_args(sys.argv[1:])
    listen_port = args_list.p
    listen_address = args_list.a
    gui_flag = args_list.no_gui
    return listen_address, listen_port, gui_flag


@Log()
def get_config():
    """Функция-парсер конфигурационного ini файла"""
    config = configparser.ConfigParser()
    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'server_config.ini'}")
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEF_PORT))
        config.set('SETTINGS', 'Listen_Address', '0.0.0.0')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_base.db3')
        return config


def main():
    """Основная функция серверной части."""
    config = get_config()

    listen_address, listen_port, gui_flag = srv_arguments_parser(
        config['SETTINGS']['Default_port'],
        config['SETTINGS']['Listen_Address'])
    # print(listen_port, listen_address)
    database = ServerStorage(os.path.join(
        config['SETTINGS']['Database_path'],
        config['SETTINGS']['Database_file']))

    server = Server(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # если указан параметр без графического интерфейса
    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                # Если выход, то завршаем основной цикл сервера.
                server.running = False
                server.join()
                break
    # если параметра про GUI нет, то запускаем GUI
    else:
        # Создаём графическое окуружение для сервера:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

        # Запускаем GUI
        server_app.exec_()

        # По закрытию окон останавливаем обработчик сообщений
        server.running = False


if __name__ == '__main__':
    main()
