import logging

# Порт по умолчанию
DEF_PORT = 9090
# Дефолтный IP адрес
DEF_IP = '127.0.0.1'
# Максимальное количество подключений
MAX_CONN = 5
# Максимальная длина сообщения в байтах
MAX_PACK_LENGTH = 10240
# Кодировка сообщений
ENCODING = 'utf-8'
# Уровень логгирования
LOGGING_LEVEL = logging.DEBUG
# База данных для хранения данных сервера:
SERVER_DATABASE = 'sqlite:///server_base.db3'
# настройки сервера
SERVER_CONFIG = 'server_config.ini'

# ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'

# статусы action
PROBE = 'probe'
MSG = 'msg'
QUIT = 'quit'
AUTHENTICATE = 'authenticate'
JOIN = 'join'
LEAVE = 'leave'

# другие ключи
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
GUEST = 'Guest'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'
SERVER = 'server'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
GET_CONTACTS = 'get_contacts'
PUBLIC_KEY_REQUEST = 'pubkey_need'

# ответы сервера
RESPONSE_GOOD = {RESPONSE: 200}

RESPONSE_202 = {RESPONSE: 202,
                LIST_INFO: None
                }
RESPONSE_BAD = {
    RESPONSE: 400,
    ERROR: None
}
RESPONSE_205 = {
    RESPONSE: 205
}
RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}
