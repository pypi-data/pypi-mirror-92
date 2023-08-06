import sys
import os
from Cryptodome.PublicKey import RSA
from argparse import ArgumentParser
from PyQt5.QtWidgets import QApplication, QMessageBox

import log.client_log_config
from common.settings import *
from logging import getLogger
from common.decos import log
from common.errors import ServerError
from client.client_database import ClientDatabase
from client.client_transport import Client
from client.main_window import ClientMainWindow
from client.start_dialog import UserNameDialog

CLI_LOGGER = getLogger('client_logger')


@log
def cln_arguments_parser():
    """
    Разбор аргументов, переданных в командной строке.
    Пример вызова:
    client.py 192.168.100.120 8888 -n user -p pass
    """
    parser = ArgumentParser()
    parser.add_argument('addr', default=DEF_IP, nargs='?')
    parser.add_argument('port', default=DEF_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    args_list = parser.parse_args(sys.argv[1:])
    server_address = args_list.addr
    server_port = args_list.port
    client_name = args_list.name
    client_passwd = args_list.password

    if not 1023 < server_port < 65536:
        CLI_LOGGER.critical(f'Попытка запуска клиента. '
                            f'Недопустимый номер порта: {server_port}.')
        sys.exit(1)

    return server_address, server_port, client_name, client_passwd


if __name__ == '__main__':

    server_address, server_port, client_name, client_passwd = \
        cln_arguments_parser()
    CLI_LOGGER.debug('Аргументы загружены.')

    # создаем приложение
    client_app = QApplication(sys.argv)

    # если клиент не указал имя в аргументах командной строки
    start_dialog = UserNameDialog()
    if not client_name or not client_passwd:
        client_app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и
        # удаляем объект, иначе выходим
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
            CLI_LOGGER.debug(f'Using USERNAME = {client_name}, PASSWD = '
                             f'{client_passwd}.')
        else:
            sys.exit(0)

    CLI_LOGGER.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}, '
        f'имя пользователя: {client_name}')

    # Загружаем ключи с файла, если же файла нет, то генерируем новую пару.
    dir_path = os.getcwd()
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    # !!!keys.publickey().export_key()
    CLI_LOGGER.debug("Ключи успешно загружены.")

    # объект БД
    database = ClientDatabase(client_name)

    # объект для соединения с сервером
    try:
        transport = Client(server_port, server_address, database, client_name,
                           client_passwd, keys)
        CLI_LOGGER.debug('Клиентское подключение готово.')
    except ServerError as e:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', e.text)
        sys.exit(1)
    transport.setDaemon(True)
    transport.start()

    # Удалим объект диалога за ненадобностью
    del start_dialog

    # GUI
    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат - {client_name}')
    client_app.exec_()

    # закрываем соединение
    transport.client_shutdown()
    transport.join()
