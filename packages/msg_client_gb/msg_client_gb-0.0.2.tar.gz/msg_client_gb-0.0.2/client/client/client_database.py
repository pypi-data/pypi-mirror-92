import datetime
import sys
import os

from sqlalchemy import create_engine, Table, Column, Integer, String, \
    Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator

sys.path.append('../')


class ClientDatabase:
    """
    Класс для работы с базой данных клиентской части программы.
    База данных SQLite. Реализована с помощью SQLAlchemy ORM.
    """

    # запись в таблице known_users
    class KnownUsers:
        """
        Класс отображение для таблицы всех пользователей.
        """
        def __init__(self, user):
            self.id = None
            self.username = user

    # запись в таблице message_history
    class MessageHistory:
        """
        Класс отображение для таблицы статистики переданных сообщений.
        """
        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    # запись в таблице contacts
    class Contacts:
        """
        Класс - отображение для таблицы контактов.
        """
        def __init__(self, contact):
            self.id = None
            self.name = contact

    def __init__(self, name):
        path = os.path.dirname(os.getcwd())
        filename = f'client_{name}.db3'

        self.database_engine = create_engine(
            f'sqlite:///{os.path.join(path, filename)}', echo=False,
            pool_recycle=7200,
            connect_args={'check_same_thread': False})
        self.metadata = MetaData()

        # таблица известных пользователей
        known_users = Table('known_users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('username', String)
                            )

        # таблица истории сообщений
        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('contact', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime)
                        )

        # таблица контактов
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )

        self.metadata.create_all(self.database_engine)

        mapper(self.KnownUsers, known_users)
        mapper(self.MessageHistory, history)
        mapper(self.Contacts, contacts)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # очищаем таблицу контактов, т.к. при новом запуске она
        # загружается с сервера
        self.session.query(self.Contacts).delete()
        self.session.commit()

    # добавление контакта
    def add_contact(self, contact):
        """Метод добавляющий контакт в базу данных."""
        if not self.session.query(self.Contacts).filter_by(
                name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    # очищение таблицы со списком контактов
    def contacts_clear(self):
        """Метод очищающий таблицу со списком контактов."""
        self.session.query(self.Contacts).delete()

    # удаление контакта
    def del_contact(self, contact):
        """Метод удаляющий определённый контакт."""
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    # добавление известных пользователей из серверной БД
    def add_users(self, users_list):
        """Метод заполняющий таблицу известных пользователей."""
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    # сохранение сообщений в БД
    def save_message(self, contact, direction, message):
        """
        Метод сохраняющий сообщение в базе данных. Принимает контакт,
        с которым происходит взаимодействие, направление сообщения (in/out),
        само сообщение.
        """
        message_row = self.MessageHistory(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    # выдает список контактов
    def get_contacts(self):
        """Метод возвращающий список всех контактов."""
        return [contact[0] for contact in
                self.session.query(self.Contacts.name).all()]

    # выдает список известных пользователей
    def get_users(self):
        """Метод возвращающий список всех известных пользователей."""
        return [user[0] for user in
                self.session.query(self.KnownUsers.username).all()]

    # проверяет наличие текущего пользователя среди известных
    def check_user(self, user):
        """Метод проверяющий существует ли пользователь."""
        if self.session.query(self.KnownUsers).filter_by(
                username=user).count():
            return True
        else:
            return False

    # проверяет наличие пользователя в контактах
    def check_contact(self, contact):
        """Метод проверяющий существует ли контакт."""
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    # возвращает историю переписки
    def get_history(self, contact):
        """
        Метод возвращающий историю сообщений с определённым пользователем.
        """
        query = self.session.query(self.MessageHistory).filter_by(
            contact=contact)
        return [(history_row.contact, history_row.direction,
                 history_row.message, history_row.date)
                for history_row in query.all()]


if __name__ == '__main__':
    test1 = ClientDatabase('test1')
    print(test1.get_contacts())
    print(test1.get_users())
    print(test1.check_user('test2'))
    print(test1.check_user('test111'))
    print(test1.get_history('test2'))
    print(test1.get_history('test2'))
    print(test1.get_history('test3'))
    # test1.del_contact('test3')
    # print(test1.get_contacts())
