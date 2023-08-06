import unittest
import json
from common.settings import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, ENCODING
from common.utils import receive_message, send_message


class TestSocket:
    """Тестовый класс"""

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_will_be_send):
        """Тестовая функуия отправки сообщения"""
        json_message = json.dumps(self.test_dict)
        self.encoded_message = json_message.encode(ENCODING)
        self.received_message = message_will_be_send

    def recv(self, max_pack_len):
        """Тестовая функуия для получения данных из сокета"""
        json_message = json.dumps(self.test_dict)
        return json_message.encode(ENCODING)


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.test_client_msg = {
            ACTION: PRESENCE,
            TIME: '9999.9999',
            USER: {
                ACCOUNT_NAME: 'test'
            }
        }
        self.test_resp_ok = {RESPONSE: 200}
        self.test_resp_not_ok = {
            RESPONSE: 400,
            ERROR: 'Bad request'
        }

    def test_send_message(self):
        """
        Тестирование функции отправки сообщения с помощью тестового сокета и тестового словаря.
        :return:
        """
        test_socket = TestSocket(self.test_client_msg)
        send_message(test_socket, self.test_client_msg)

        self.assertEqual(test_socket.encoded_message, test_socket.received_message)
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket)

    def test_receive_message(self):
        """
        Тестирование функции приема сообщения.
        :return:
        """
        test_socket_good = TestSocket(self.test_resp_ok)
        test_socket_bad = TestSocket(self.test_resp_not_ok)

        self.assertEqual(receive_message(test_socket_good), self.test_resp_ok)
        self.assertEqual(receive_message(test_socket_bad), self.test_resp_not_ok)


if __name__ == '__main__':
    unittest.main()
