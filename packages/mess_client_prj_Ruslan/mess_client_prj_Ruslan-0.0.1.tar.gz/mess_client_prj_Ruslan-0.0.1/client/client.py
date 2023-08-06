"""Main client app"""

import sys
import logging
import argparse
import os

from PyQt5.QtWidgets import QApplication, QMessageBox

from Cryptodome.PublicKey import RSA

from common.vars import DEFAULT_PORT, DEFAULT_IP

from common.errors import ServerError

from common.decos import Log
from client_utils.client_gui import UserNameDialog, ClientMainWindow

from client_utils.client_database import ClientDatabase

from client_utils.transport import ClientTransport

# pip install pycryptodome
# pip install pycryptodomex

CLIENT_LOGGER = logging.getLogger('client_log')


@Log()
def arg_parser():
    """Парсер аргументов коммандной строки"""

    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    username = namespace.name
    user_passwd = namespace.password

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    return server_address, server_port, username, user_passwd


def main():
    """Сообщаем о запуске"""

    print('Консольный месседжер. Клиентский модуль.')

    # Загружаем параметы коммандной строки
    server_address, server_port, username, user_passwd = arg_parser()

    client_app = QApplication(sys.argv)

    start_dialog = UserNameDialog()
    if not username or not user_passwd:
        client_app.exec_()

        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и
        # удаляем объект, инааче выходим
        if start_dialog.ok_pressed:
            username = start_dialog.client_name.text()
            user_passwd = start_dialog.client_passwd.text()
            CLIENT_LOGGER.debug(f'Using USERNAME = {username}, PASSWD = {user_passwd}.')
        else:
            sys.exit(0)

    CLIENT_LOGGER.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}, имя пользователя: {username}')

    # Загружаем ключи с файла, если же файла нет, то генерируем новую пару.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    key_file = os.path.join(dir_path, f'{username}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    CLIENT_LOGGER.debug("Keys sucsessfully loaded.")
    database = ClientDatabase(username)

    # Создаём объект - транспорт и запускаем транспортный поток
    try:
        transport = ClientTransport(server_port, server_address, database, username, user_passwd,
                                    keys)
        CLIENT_LOGGER.debug("Transport ready.")
    except ServerError as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', error.text)
        sys.exit(1)
    transport.setDaemon(True)
    transport.start()

    # Создаём GUI
    main_window = ClientMainWindow(database, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {username}')
    client_app.exec_()

    # Раз графическая оболочка закрылась, закрываем транспорт
    transport.transport_shutdown()
    transport.join()


if __name__ == '__main__':
    main()
