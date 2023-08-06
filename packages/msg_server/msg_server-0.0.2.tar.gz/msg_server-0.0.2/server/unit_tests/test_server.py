import unittest
from common.settings import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, GUEST
from server import client_massage_handler


class TestServer(unittest.TestCase):

    def setUp(self):
        self.no_error_response = {RESPONSE: 200}
        self.error_response = {
            RESPONSE: 400,
            ERROR: 'Bad request'
        }

    def test_no_action(self):
        """Если в переданном клиентом сообщении нет поля ACTION"""
        self.assertEqual(client_massage_handler(
            {TIME: '9999.9999', USER: {ACCOUNT_NAME: GUEST}}), self.error_response)

    def test_action_is_not_presence(self):
        """Значение поля ACTION отличается от требуемого"""
        self.assertEqual(client_massage_handler(
            {ACTION: 'Hello', TIME: '9999.9999', USER: {ACCOUNT_NAME: GUEST}}), self.error_response)

    def test_no_time(self):
        """В переданном сообщении  нет поля TIME"""
        self.assertEqual(client_massage_handler(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: GUEST}}), self.error_response)

    def test_no_user(self):
        """В переданном сообщении нет поля USER"""
        self.assertEqual(client_massage_handler({ACTION: PRESENCE, TIME: '9999.9999'}), self.error_response)

    def test_wrong_user(self):
        """В поле USER некорректное имя"""
        self.assertEqual(client_massage_handler(
            {ACTION: PRESENCE, TIME: '9999.9999', USER: {ACCOUNT_NAME: 'Гость'}}), self.error_response)

    def test_correct_answer(self):
        """Тест с корректным ответом"""
        self.assertEqual(client_massage_handler(
            {ACTION: PRESENCE, TIME: '9999.9999', USER: {ACCOUNT_NAME: GUEST}}), self.no_error_response)


if __name__ == '__main__':
    unittest.main()
