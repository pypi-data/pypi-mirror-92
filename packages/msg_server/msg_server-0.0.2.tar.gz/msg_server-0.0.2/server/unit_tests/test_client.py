import unittest
from client import create_presence, server_massage_handler
from common.settings import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, GUEST


class TestClient(unittest.TestCase):

    def setUp(self):
        self.test_variable = create_presence()
        self.test_variable[TIME] = '9999.9999'

    def test_create_presence(self):
        """Проверяет корректность формирования запроса к серверу"""
        self.assertEqual(self.test_variable, {ACTION: PRESENCE, TIME: '9999.9999', USER: {ACCOUNT_NAME: GUEST}})

    def test_correct_answer(self):
        """Проверка корректного разбора ответа"""
        self.assertEqual(server_massage_handler({RESPONSE: 200}), '200 : OK')

    def test_incorrect_answer(self):
        """Проверка некорректного разбора ответа"""
        self.assertEqual(server_massage_handler({RESPONSE: 400, ERROR: 'Bad request'}), '400 : Bad request')

    def test_without_response(self):
        """Проверка срабатывания исклюения, если в ответе нет поля RESPONSE"""
        self.assertRaises(ValueError, server_massage_handler, {ERROR: 'Bad request'})


if __name__ == '__main__':
    unittest.main()
