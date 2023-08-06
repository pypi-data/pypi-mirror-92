import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from client import create_presence, create_registration, create_authentication, process_ans, send_and_receive
from common.vars import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, PASSWORD, EMAIL, ALERT


class TestClientClass(unittest.TestCase):
    def setUp(self):
        self.pres = create_presence('Rick')
        self.reg = create_registration('Ruslan', 'Password1', 'ruslan@mail.ru')
        self.auth = create_authentication('Ruslan', 'Password1')
        self.answer_200 = process_ans({RESPONSE: 200, ALERT: "Presence completed"})
        self.answer_400 = process_ans({RESPONSE: 400, ERROR: 'Bad Request'})
        self.answer_200_reg = process_ans({RESPONSE: 200, ALERT: "Вы зарегистрировали аккаунт"})
        self.answer_400_reg = process_ans({RESPONSE: 400, ERROR: 'Ошибка регистрации'})
        self.answer_200_auth = process_ans({RESPONSE: 200, ALERT: "Authentication completed"})
        self.answer_400_auth = process_ans({RESPONSE: 400, ERROR: 'Authentication error'})

        self.presence = {
            ACTION: 'presence',
            TIME: 1,
            USER: {
                ACCOUNT_NAME: 'Rick'
            }
        }

        self.registration = {
            ACTION: 'registration',
            TIME: 1,
            USER: {
                ACCOUNT_NAME: 'Ruslan',
                PASSWORD: 'Password1',
                EMAIL: 'ruslan@mail.ru'
            }
        }

        self.authentication = {
            ACTION: 'authenticate',
            TIME: 1,
            USER: {
                ACCOUNT_NAME: 'Ruslan',
                PASSWORD: 'Password1'
            }
        }

    def test_normal_presence(self):
        self.pres[TIME] = 1
        self.assertEqual(self.pres, self.presence)

    def test_name(self):
        self.assertNotEqual(self.pres[USER][ACCOUNT_NAME], 'Guest')

    def test_normal_registration(self):
        self.reg[TIME] = 1
        self.assertEqual(self.reg, self.registration)

    def test_normal_authentication(self):
        self.auth[TIME] = 1
        self.assertEqual(self.auth, self.authentication)

    def test_200(self):
        self.assertEqual(self.answer_200, '200 : OK \nPresence completed')

    def test_400(self):
        self.assertEqual(self.answer_400, '400 : Bad Request')

    def test_200_reg(self):
        self.assertEqual(self.answer_200_reg, '200 : OK \nВы зарегистрировали аккаунт')

    def test_400_reg(self):
        self.assertEqual(self.answer_400_reg, '400 : Ошибка регистрации')

    def test_200_auth(self):
        self.assertEqual(self.answer_200_auth, '200 : OK \nAuthentication completed')

    def test_400_auth(self):
        self.assertEqual(self.answer_400_auth, '400 : Authentication error')

    def test_bad_response(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
