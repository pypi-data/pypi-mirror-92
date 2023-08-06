import sys
import os
import unittest
import time

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.vars import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, PASSWORD, EMAIL, ALERT
from server import process_client_message, authentication_check, user_validation


class TestServerClass(unittest.TestCase):
    def setUp(self):
        self.err_400 = {RESPONSE: 400, ERROR: 'Bad Request'}
        self.ok_200 = {RESPONSE: 200, ALERT: "Presence completed"}
        self.user_obj = {ACCOUNT_NAME: 'Ruslan', PASSWORD: 'password1'}
        self.wrong_user = {ACCOUNT_NAME: 'noname', PASSWORD: 'password1'}

        self.old_user_obj_reg = {ACCOUNT_NAME: 'Ruslan', PASSWORD: 'password1', EMAIL: "ruslan@mail.ru"}
        self.new_user_obj_reg = {ACCOUNT_NAME: 'noname', PASSWORD: 'password1', EMAIL: "noname@mail.ru"}

        self.auth = authentication_check(self.user_obj)
        self.bad_auth = authentication_check(self.wrong_user)

        self.reg = user_validation(self.new_user_obj_reg)
        self.bad_reg = user_validation(self.old_user_obj_reg)

        self.presence = process_client_message(
            {
                ACTION: 'presence',
                TIME: time.time(),
                USER: {
                    ACCOUNT_NAME: 'Guest'
                }
            })

        self.presence_no_time = process_client_message(
            {
                ACTION: 'presence',
                USER: {
                    ACCOUNT_NAME: 'Guest'
                }
            })

        self.presence_no_action = process_client_message(
            {
                TIME: 1,
                USER: {
                    ACCOUNT_NAME: 'Guest'
                }
            })

        self.presence_wrong_action = process_client_message(
            {
                ACTION: 'exit',
                TIME: 1,
                USER: {
                    ACCOUNT_NAME: 'Guest'
                }
            })

    def test_response_in_400(self):
        self.assertIn(RESPONSE, self.err_400)

    def test_error_in_400(self):
        self.assertIn(ERROR, self.err_400)

    def test_ok_response(self):
        self.assertEqual(self.presence, self.ok_200)

    def test_int_response_200(self):
        self.assertIsInstance(self.presence[RESPONSE], int)

    def test_int_response_400(self):
        self.assertIsInstance(self.presence_no_action[RESPONSE], int)

    def test_no_time(self):
        self.assertEqual(self.presence_no_time, self.err_400)

    def test_wrong_action(self):
        self.assertEqual(self.presence_wrong_action, self.err_400)

    def test_no_action(self):
        self.assertEqual(self.presence_wrong_action, self.err_400)

    def test_auth(self):
        self.assertTrue(self.auth)

    def test_bad_auth(self):
        self.assertFalse(self.bad_auth)

    def test_bad_reg(self):
        self.assertFalse(self.bad_reg)

    def test_normal_reg(self):
        self.assertTrue(self.reg)


if __name__ == '__main__':
    unittest.main()
