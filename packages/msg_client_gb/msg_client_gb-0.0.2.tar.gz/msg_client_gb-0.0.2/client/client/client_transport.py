import hashlib
import socket
import sys
import json
import binascii
from time import time, sleep
from threading import Thread, Lock
from logging import getLogger

import hmac
from PyQt5.QtCore import pyqtSignal, QObject

from common.settings import *
from common.utils import receive_message, send_message
from common.errors import ServerError

sys.path.append('../')
CLI_LOGGER = getLogger('client_logger')
sock_lock = Lock()


class Client(Thread, QObject):
    """
    Класс реализующий транспортную подсистему клиентского
    модуля. Отвечает за взаимодействие с сервером.
    """
    new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, port, ip_address, database, username, passwd, keys):
        # конструктор предка
        Thread.__init__(self)
        QObject.__init__(self)

        self.database = database
        self.username = username
        self.password = passwd
        self.sock = None
        self.keys = keys
        self.connection_init(port, ip_address)
        try:
            self.user_list_update()
            self.contacts_list_update()
        except OSError as e:
            if e.errno:
                CLI_LOGGER.critical(f'Потеряно соединение с сервером')
                raise ServerError('Потеряно соединение с сервером')
            CLI_LOGGER.error(
                'Timeout соединения при обновлении списка пользователей.')
        except json.JSONDecodeError:
            CLI_LOGGER.critical(f'Потеряно соединение с сервером')
            raise ServerError('Потеряно соединение с сервером')
        # флаг продолжения работы
        self.running = True

    # инициализация соединения с сервером
    def connection_init(self, port, ip_address):
        """Метод устанавливает соединение с сервером."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ожидаем освобождения сокета
        self.sock.settimeout(5)

        # флаг успеха подключения
        connected = False
        # 5 попыток соединения, если соединились, то флаг меняем на True
        for i in range(5):
            CLI_LOGGER.info(f'Попытка подключения №{i + 1}')
            try:
                self.sock.connect((ip_address, port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                CLI_LOGGER.debug('Установлено соединение с сервером')
                break
            sleep(1)

        # так и не удалось подключиться
        if not connected:
            CLI_LOGGER.critical('Не удалось подключиться к серверу')
            raise ServerError('Не удалось подключиться к серверу')

        CLI_LOGGER.debug('Начат процесс аутентификации.')

        # Запускаем процедуру авторизации
        # Получаем хэш пароля
        passwd_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        passwd_hash_string = binascii.hexlify(passwd_hash)

        CLI_LOGGER.debug(f'Хеш пароля готов: {passwd_hash_string}')

        # Получаем публичный ключ и декодируем его из байтов
        pubkey = self.keys.publickey().export_key().decode('ascii')

        # Авторизируемся на сервере
        with sock_lock:
            # {'action': 'presence', 'time': 2341254553.234234,
            # 'user': {'account_name': 'Guest'}}
            presense = {
                ACTION: PRESENCE,
                TIME: time(),
                USER: {
                    ACCOUNT_NAME: self.username,
                    PUBLIC_KEY: pubkey
                }
            }
            CLI_LOGGER.debug(f"Сообщение приветствия = {presense}")
            # Отправляем серверу приветственное сообщение.
            try:
                send_message(self.sock, presense)
                answer = receive_message(self.sock)
                CLI_LOGGER.debug(f'Ответ сервера = {answer}.')
                # Если сервер вернул ошибку, бросаем исключение.
                if RESPONSE in answer:
                    if answer[RESPONSE] == 400:
                        raise ServerError(answer[ERROR])
                    elif answer[RESPONSE] == 511:
                        # Если всё нормально, то продолжаем процедуру
                        # авторизации.
                        ans_data = answer[DATA]
                        hash = hmac.new(passwd_hash_string,
                                        ans_data.encode('utf-8'), 'MD5')
                        digest = hash.digest()
                        my_answer = RESPONSE_511
                        my_answer[DATA] = binascii.b2a_base64(digest).decode(
                            'ascii')
                        send_message(self.sock, my_answer)
                        self.server_message_handler(receive_message(self.sock))
            except (OSError, json.JSONDecodeError) as err:
                CLI_LOGGER.debug(f'Connection error.', exc_info=err)
                raise ServerError('Сбой соединения в процессе авторизации.')

        # если все хорошо, то соответствующее сообщение
        # CLI_LOGGER.info('Соединение с сервером установлено.')

    # обрабатывает сообщения от сервера
    def server_message_handler(self, message):
        """Метод обрабатывает поступающие сообщения с сервера."""
        CLI_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
        if RESPONSE in message:
            print(f'Получил {message}')
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ServerError(f'{message[ERROR]}')
            elif message[RESPONSE] == 205:
                print('я тут')
                self.user_list_update()
                self.contacts_list_update()
                self.message_205.emit()
            else:
                CLI_LOGGER.error(
                    f'Принят неизвестный код подтверждения {message[RESPONSE]}')

        # если сообщение от пользователя, то добавляем в базу и
        # даем сигнал о новом сообщениии
        elif ACTION in message and message[
            ACTION] == MESSAGE and SENDER in message and \
                DESTINATION in message \
                and MESSAGE_TEXT in message and message[
            DESTINATION] == self.username:
            CLI_LOGGER.debug(
                f'Получено сообщение от пользователя {message[SENDER]}:'
                f'{message[MESSAGE_TEXT]}')
            self.new_message.emit(message)

    # обновляет список контактов с сервера
    def contacts_list_update(self):
        """Метод обновляющий с сервера список контактов."""
        self.database.contacts_clear()
        CLI_LOGGER.debug(
            f'Запрос контакт листа для пользователя {self.username}')
        request = {
            ACTION: GET_CONTACTS,
            TIME: time(),
            USER: self.username
        }
        CLI_LOGGER.debug(f'Сформирован запрос {request}')
        with sock_lock:
            send_message(self.sock, request)
            answer = receive_message(self.sock)
        CLI_LOGGER.debug(f'Получен ответ {answer}')
        if RESPONSE in answer and answer[RESPONSE] == 202:
            for contact in answer[LIST_INFO]:
                # print(contact)
                self.database.add_contact(contact)
        else:
            CLI_LOGGER.error('Не удалось обновить список контактов.')

    # обновляет список известных пользователей
    def user_list_update(self):
        """Метод обновляющий с сервера список пользователей."""
        CLI_LOGGER.debug(
            f'Запрос списка известных пользователей {self.username}')
        request = {
            ACTION: USERS_REQUEST,
            TIME: time(),
            ACCOUNT_NAME: self.username
        }
        with sock_lock:
            send_message(self.sock, request)
            answer = receive_message(self.sock)
        if RESPONSE in answer and answer[RESPONSE] == 202:
            self.database.add_users(answer[LIST_INFO])
        else:
            CLI_LOGGER.error(
                'Не удалось обновить список известных пользователей.')

    # запрашиваем с сервера публичный ключь пользователя
    def key_request(self, user):
        """Метод запрашивающий с сервера публичный ключ пользователя."""
        CLI_LOGGER.debug(f'Запрос публичного ключа для {user}')
        request = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time(),
            ACCOUNT_NAME: user
        }
        with sock_lock:
            send_message(self.sock, request)
            answer = receive_message(self.sock)
        if RESPONSE in answer and answer[RESPONSE] == 511:
            return answer[DATA]
        else:
            CLI_LOGGER.error(f'Не удалось получить ключ собеседника{user}.')

    # добавление пользователя на сервере в список контактов
    def add_contact(self, contact):
        """Метод отправляющий на сервер сведения о добавлении контакта."""
        CLI_LOGGER.debug(f'Создание контакта {contact}')
        request = {
            ACTION: ADD_CONTACT,
            TIME: time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with sock_lock:
            send_message(self.sock, request)
            self.server_message_handler(receive_message(self.sock))

    # удаление пользователя из списка контактов на сервере
    def remove_contact(self, contact):
        """Метод отправляющий на сервер сведения о удалении контакта."""
        CLI_LOGGER.debug(f'Удаление контакта {contact}')
        request = {
            ACTION: REMOVE_CONTACT,
            TIME: time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with sock_lock:
            send_message(self.sock, request)
            self.server_message_handler(receive_message(self.sock))

    # отправляет сообщение о выходе из клиента.
    def client_shutdown(self):
        """Метод уведомляющий сервер о завершении работы клиента."""
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: time(),
            ACCOUNT_NAME: self.username
        }
        with sock_lock:
            try:
                send_message(self.sock, message)
            except OSError:
                pass
        CLI_LOGGER.debug('Транспорт завершает работу.')
        sleep(0.5)

    # отправка сообщения на сервер
    def send_message(self, to, message):
        """Метод отправляющий на сервер сообщения для пользователя."""
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.username,
            DESTINATION: to,
            TIME: time(),
            MESSAGE_TEXT: message
        }
        CLI_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')

        # Необходимо дождаться освобождения сокета для отправки сообщения
        with sock_lock:
            send_message(self.sock, message_dict)
            self.server_message_handler(receive_message(self.sock))
            CLI_LOGGER.info(f'Отправлено сообщение пользователю {to}')

    def run(self):
        """Метод содержащий основной цикл работы транспортного потока."""
        CLI_LOGGER.debug('Запущен поток - приёмник собщений с сервера.')
        while self.running:
            # Отдыхаем секунду и снова пробуем захватить сокет.
            # если не сделать тут задержку, то отправка может
            # достаточно долго ждать освобождения сокета.
            sleep(1)
            message = None
            with sock_lock:
                try:
                    self.sock.settimeout(0.5)
                    message = receive_message(self.sock)
                except OSError as e:
                    if e.errno:
                        CLI_LOGGER.critical(f'Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                # Проблемы с соединением
                except (
                        ConnectionError, ConnectionAbortedError,
                        ConnectionResetError,
                        json.JSONDecodeError, TypeError):
                    CLI_LOGGER.debug(f'Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                finally:
                    self.sock.settimeout(5)

            # Если сообщение получено, то вызываем функцию обработчик:
            if message:
                CLI_LOGGER.debug(f'Принято сообщение с сервера: {message}')
                self.server_message_handler(message)
