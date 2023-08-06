import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.vars import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_PORT, MAX_CONNECTIONS, \
    MAX_PACKAGE_LENGTH, ENCODING, PASSWORD, ALERT, EMAIL
from common.utils import send_message, receive_message
from sock_test import TestSocket


class TestUtilsClass(unittest.TestCase):
    def setUp(self):
        self.test_dict_send = {
            ACTION: PRESENCE,
            TIME: 111111.111111,
            USER: {
                ACCOUNT_NAME: 'test_test'
            }
        }
        self.test_dict_recv_ok = {RESPONSE: 200}

        self.test_dict_recv_err = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }

    def test_send_message(self):
        test_socket = TestSocket(self.test_dict_send)

        # вызов тестируемой функции, результаты будут сохранены в тестовом сокете
        send_message(test_socket, self.test_dict_send)

        # проверка корретности кодирования словаря.
        # сравниваем результат довренного кодирования и результат от тестируемой функции
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)

        # дополнительно, проверим генерацию исключения, при не словаре на входе.
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket)

    def test_get_message(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)

        # тест корректной расшифровки корректного словаря
        self.assertEqual(receive_message(test_sock_ok), self.test_dict_recv_ok)

        # тест корректной расшифровки ошибочного словаря
        self.assertEqual(receive_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
