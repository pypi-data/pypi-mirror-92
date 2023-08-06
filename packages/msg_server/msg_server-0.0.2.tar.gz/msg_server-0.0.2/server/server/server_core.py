import os
import json
import socket
from threading import Thread
from logging import getLogger

import binascii
import hmac
from select import select

from common.descriptors import Port, IPAddress
from common.settings import *
from common.utils import *

SERV_LOGGER = getLogger('server_logger')


# основной класс сервера
class Server(Thread):
    """
    Основной класс сервера. Принимает соединения, словари пакеты от клиентов,
    обрабатывает входящие сообщения. Работает в отдельном потоке.
    """
    port = Port()
    address = IPAddress()

    def __init__(self, listen_address, listen_port, database):
        self.address = listen_address
        self.port = listen_port

        self.database = database

        self.sock = None

        # список подключенных клиентов
        self.clients_list = []

        # сокеты
        self.listen_sockets = None
        self.error_sockets = None

        # флаг продолжения работы
        self.running = True

        # словарь - имена:сокеты
        self.users_dict = {}

        super().__init__()

    def run(self):
        """Метод основной цикл потока."""
        # инициализация Сокета
        self.init_socket()

        # основной цикл программы сервера
        while self.running:
            # Ждём подключения, если таймаут вышел, ловим исключение.
            try:
                client_sock, client_addr = self.sock.accept()
            except OSError:
                pass
            else:
                SERV_LOGGER.info(f'Установлено соедение с ПК {client_addr}')
                client_sock.settimeout(5)
                self.clients_list.append(client_sock)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            # проверяем на наличие ждущих клиентов
            try:
                if self.clients_list:
                    recv_data_lst, self.listen_sockets, self.error_sockets = select(
                        self.clients_list, self.clients_list, [], 0)
            except OSError as err:
                SERV_LOGGER.error(f'Ошибка работы с сокетами: {err.errno}')

            # принимаем сообщения и если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.client_massage_handler(
                            receive_message(client_with_message),
                            client_with_message)
                    except (OSError, json.JSONDecodeError, TypeError) as err:
                        SERV_LOGGER.debug(
                            f'Получаем информацию об исключении.',
                            exc_info=err)
                        self.remove_client(client_with_message)

    # удаляет клиента, с которым прервалась связь
    def remove_client(self, client_sock):
        """
        Метод обрабатывет пользователя, с которым прервана связь.
        Удалаяет его из списка клиентов и из БД.
        """
        SERV_LOGGER.info(
            f'Клиент {client_sock.getpeername()} отключился от сервера.')
        for name in self.users_dict:
            if self.users_dict[name] == client_sock:
                self.database.user_logout(name)
                del self.users_dict[name]
                break
        self.clients_list.remove(client_sock)
        client_sock.close()

    # инициализируем серверный сокет
    def init_socket(self):
        """Метод инициализации сокета."""
        SERV_LOGGER.info(
            f'Запущен сервер, порт для подключений: {self.port},'
            f' адрес с которого принимаются подключения: {self.address}.'
            f' Если адрес не указан, принимаются соединения с любых адресов.')
        # готовим сокет
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_sock.bind((self.address, self.port))
        serv_sock.settimeout(0.5)

        # начинаем слушать сокет.
        self.sock = serv_sock
        self.sock.listen(MAX_CONN)

    # отправляет сообщения клиенту
    def transmit_message_to_client(self, message):
        """Метод отправки сообщения клиенту."""
        # {'action': 'message', 'from': 'user2', 'to': 'user1',
        # 'time': 1608053378.0309482, 'mess_text': 'tetris'}
        if message[DESTINATION] in self.users_dict and self.users_dict[
            message[DESTINATION]] in self.listen_sockets:
            try:
                send_message(self.users_dict[message[DESTINATION]], message)
                SERV_LOGGER.info(
                    f'Отправлено сообщение пользователю {message[DESTINATION]}'
                    f' от пользователя {message[SENDER]}.')
            except OSError:
                self.remove_client(message[DESTINATION])
        elif message[DESTINATION] in self.users_dict and self.users_dict[
            message[DESTINATION]] not in self.listen_sockets:
            SERV_LOGGER.error(
                f'Связь с клиентом {message[DESTINATION]} была потеряна.'
                f' Соединение закрыто, доставка невозможна.')
            self.remove_client(self.users_dict[message[DESTINATION]])
        else:
            SERV_LOGGER.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован на'
                f' сервере, отправка сообщения невозможна.')

    # обрабатывает входящие сообщения от клиента, в
    # случае необходимости отправляет ответ
    def client_massage_handler(self, message, client_sock):
        """Метод обработчик входящих сообщений."""
        SERV_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
        # если это сообщение о присутствии, принимаем и отвечаем
        if ACTION in message and message[
            ACTION] == PRESENCE and TIME in message and USER in message:
            # Если сообщение о присутствии то вызываем функцию авторизации.
            self.autorize_user(message, client_sock)

        # сообщение другому пользователю, отправляем его получателю.
        elif ACTION in message and message[
            ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message and \
                self.users_dict[message[SENDER]] == client_sock:
            if message[DESTINATION] in self.users_dict:
                self.database.count_message(message[SENDER],
                                            message[DESTINATION])
                self.transmit_message_to_client(message)
                try:
                    send_message(client_sock, RESPONSE_GOOD)
                except OSError:
                    self.remove_client(client_sock)
            else:
                response = RESPONSE_BAD
                response[ERROR] = 'Пользователь не зарегистрирован на сервере.'
                try:
                    send_message(client_sock, response)
                except OSError:
                    pass
            return

        # клиент выходит
        elif ACTION in message and message[
            ACTION] == EXIT and ACCOUNT_NAME in message \
                and self.users_dict[message[ACCOUNT_NAME]] == client_sock:
            self.remove_client(client_sock)

        # запрос листа контактов
        elif ACTION in message and message[
            ACTION] == GET_CONTACTS and USER in message and \
                self.users_dict[message[USER]] == client_sock:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.get_contacts(message[USER])
            try:
                send_message(client_sock, response)
            except OSError:
                self.remove_client(client_sock)

        # добавление контакта
        elif ACTION in message and message[
            ACTION] == ADD_CONTACT and ACCOUNT_NAME in message and \
                USER in message \
                and self.users_dict[message[USER]] == client_sock:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client_sock, RESPONSE_GOOD)
            except OSError:
                self.remove_client(client_sock)

        # удаление контакта
        elif ACTION in message and message[
            ACTION] == REMOVE_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.users_dict[message[USER]] == client_sock:
            self.database.del_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client_sock, RESPONSE_GOOD)
            except OSError:
                self.remove_client(client_sock)

        # запрос уже известных пользователей
        elif ACTION in message and message[
            ACTION] == USERS_REQUEST and ACCOUNT_NAME in message \
                and self.users_dict[message[ACCOUNT_NAME]] == client_sock:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0] for user in
                                   self.database.users_list()]
            try:
                send_message(client_sock, response)
            except OSError:
                self.remove_client(client_sock)

        # запрос публичного ключа пользователя
        elif ACTION in message and message[
            ACTION] == PUBLIC_KEY_REQUEST and ACCOUNT_NAME in message:
            response = RESPONSE_511
            response[DATA] = self.database.get_pubkey(message[ACCOUNT_NAME])
            # может быть, что ключа ещё нет (пользователь
            # никогда не логинился, тогда шлём 400)
            if response[DATA]:
                try:
                    send_message(client_sock, response)
                except OSError:
                    self.remove_client(client_sock)
            else:
                response = RESPONSE_BAD
                response[
                    ERROR] = 'Нет публичного ключа для данного пользователя'
                try:
                    send_message(client_sock, response)
                except OSError:
                    self.remove_client(client_sock)

        # иначе отдаём Bad request
        else:
            response = RESPONSE_BAD
            response[ERROR] = 'Запрос некорректен.'
            try:
                send_message(client_sock, response)
            except OSError:
                self.remove_client(client_sock)

    # авиоризация пользователя
    def autorize_user(self, message, client_sock):
        """Метад реализующий аутентификацию пользователя на сервере."""
        # если имя пользователя уже занято то возвращаем 400
        SERV_LOGGER.debug(f'Начинаем процесс авторизации для {message[USER]}')
        if message[USER][ACCOUNT_NAME] in self.users_dict.keys():
            response = RESPONSE_BAD
            response[ERROR] = 'Имя пользователя уже занято.'
            try:
                SERV_LOGGER.debug(f'Имя занято, отвечаем {response}')
                send_message(client_sock, response)
            except OSError:
                SERV_LOGGER.debug('OS Error')
                pass
            self.clients_list.remove(client_sock)
            client_sock.close()
        # Проверяем что пользователь зарегистрирован на сервере.
        elif not self.database.check_user(message[USER][ACCOUNT_NAME]):
            response = RESPONSE_BAD
            response[ERROR] = 'Пользователь не зарегистрирован.'
            try:
                SERV_LOGGER.debug(
                    f'Неизвестный пользователь, отвечаем {response}')
                send_message(client_sock, response)
            except OSError:
                pass
            self.clients_list.remove(client_sock)
            client_sock.close()
        else:
            SERV_LOGGER.debug('Имя корректно, проверям пароль.')
            # Иначе отвечаем 511 и проводим процедуру авторизации
            # Словарь - заготовка
            message_auth = RESPONSE_511
            # Набор байтов в hex представлении
            random_str = binascii.hexlify(os.urandom(64))
            # В словарь байты нельзя, декодируем (json.dumps -> TypeError)
            message_auth[DATA] = random_str.decode('ascii')
            # Создаём хэш пароля и связки с рандомной строкой, сохраняем
            # серверную версию ключа
            hash = hmac.new(
                self.database.get_hash(message[USER][ACCOUNT_NAME]),
                random_str, 'MD5')
            digest = hash.digest()
            SERV_LOGGER.debug(f'Сообщение аутентификации = {message_auth}')
            try:
                # Обмен с клиентом
                send_message(client_sock, message_auth)
                answer = receive_message(client_sock)
            except OSError as err:
                SERV_LOGGER.debug('Ошибка аутентификации:', exc_info=err)
                client_sock.close()
                return
            client_digest = binascii.a2b_base64(answer[DATA])
            # Если ответ клиента корректный, то сохраняем его в список
            # пользователей.
            if RESPONSE in answer and answer[
                RESPONSE] == 511 and hmac.compare_digest(
                digest, client_digest):
                self.users_dict[message[USER][ACCOUNT_NAME]] = client_sock
                client_ip, client_port = client_sock.getpeername()
                try:
                    send_message(client_sock, RESPONSE_GOOD)
                except OSError:
                    self.remove_client(message[USER][ACCOUNT_NAME])
                # добавляем пользователя в список активных и
                # если у него изменился открытый ключ
                # сохраняем новый
                self.database.user_login(
                    message[USER][ACCOUNT_NAME],
                    client_ip,
                    client_port,
                    message[USER][PUBLIC_KEY])
            else:
                response = RESPONSE_BAD
                response[ERROR] = 'Неверный пароль.'
                try:
                    send_message(client_sock, response)
                except OSError:
                    pass
                self.clients_list.remove(client_sock)
                client_sock.close()

    # отправляет пользователям 205 сообщение
    def service_update_lists(self):
        """Метод реализует оправку сервисного сообщения 205 клиентам."""
        for client in self.users_dict:
            try:
                send_message(self.users_dict[client], RESPONSE_205)
            except OSError:
                self.remove_client(self.users_dict[client])

