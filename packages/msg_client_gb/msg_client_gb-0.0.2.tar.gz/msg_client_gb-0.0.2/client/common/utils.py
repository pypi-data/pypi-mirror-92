import json

from common.settings import ENCODING, MAX_PACK_LENGTH
from common.decos import log


# @log
def receive_message(socket):
    """
    Функция принимает байт сообщение и декодирует его. Возвращает словарь.
    Если поступают не байты, то выдает ошибку.
    """
    encoded_message = socket.recv(MAX_PACK_LENGTH)
    json_message = encoded_message.decode(ENCODING)
    message = json.loads(json_message)
    if isinstance(message, dict):
        return message
    else:
        raise TypeError


# @log
def send_message(socket, message):
    """
    Функция принимает сокет адресата и словарь с данными,
    кодирует и отправлет его.
    """
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    socket.send(encoded_message)
