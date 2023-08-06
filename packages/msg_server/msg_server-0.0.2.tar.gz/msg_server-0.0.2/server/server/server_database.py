import datetime

from sqlalchemy import create_engine, Table, Column, Integer, String, \
    ForeignKey, DateTime, MetaData, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class ServerStorage:
    """
    Класс для работы с базой данных серверной части программы.
    База данных SQLite. Реализована с помощью SQLAlchemy ORM.
    """

    # запись в таблице AllUsers
    class AllUsers:
        """Класс отображения таблицы всех пользователей."""

        def __init__(self, username, passwd_hash):
            self.id = None
            self.name = username
            self.last_login = datetime.datetime.now()
            self.passwd_hash = passwd_hash
            self.pubkey = None

    # запись в таблице ActiveUsers
    class ActiveUsers:
        """Класс отображения таблицы активных пользователей."""

        def __init__(self, user_id, ip_address, port, login_time):
            self.id = None
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time

    # запись в таблице LoginHistory
    class LoginHistory:
        """Класс отображения таблицы истории входов."""

        def __init__(self, user, date, ip, port):
            self.id = None
            self.name = user
            self.date_time = date
            self.ip = ip
            self.port = port

    # контакты пользователя
    class UsersContacts:
        """Класс отображения контактов между пользователями."""

        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact

    # история отправки сообщений
    class UsersHistory:
        """Класс отображения истории действий пользователя."""

        def __init__(self, user):
            self.id = None
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, path):
        self.database_engine = create_engine(
            f'sqlite:///{path}', echo=False, pool_recycle=7200,
            connect_args={'check_same_thread': False})
        self.metadata = MetaData()

        # таблица пользователей Users
        users_table = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime),
                            Column('passwd_hash', String),
                            Column('pubkey', Text)
                            )

        # таблица активных пользователей Active_users
        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id'),
                                          unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime),
                                   )

        # таблица истории входов Login_history
        login_history_table = Table('Login_history', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('name', ForeignKey('Users.id')),
                                    Column('date_time', DateTime),
                                    Column('ip', String),
                                    Column('port', Integer),
                                    )

        # таблица контактов пользователей
        contacts_table = Table('Contacts', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('user', ForeignKey('Users.id')),
                               Column('contact', ForeignKey('Users.id'))
                               )

        # таблица истории пользователей
        users_history_table = Table('History', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('user', ForeignKey('Users.id')),
                                    Column('sent', Integer),
                                    Column('accepted', Integer)
                                    )

        self.metadata.create_all(self.database_engine)

        mapper(self.AllUsers, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.LoginHistory, login_history_table)
        mapper(self.UsersContacts, contacts_table)
        mapper(self.UsersHistory, users_history_table)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    # записывает пользователя в БД при логине
    def user_login(self, username, ip_address, port, key):
        """
        Метод вполняется при фходе пользователя, записывает в базу факт входа,
        обновляет открытый ключ при его изменении.
        """
        # ищем в БД пользователя
        query = self.session.query(self.AllUsers).filter_by(name=username)
        # проверка пользователя - новый или нет
        if query.count():
            user = query.first()
            user.last_login = datetime.datetime.now()
            if user.pubkey != key:
                user.pubkey = key
        else:
            raise ValueError('Пользователь не зарегистрирован.')

        # делаем запись в таблице активный пользователь
        new_active_user = self.ActiveUsers(user.id, ip_address, port,
                                           datetime.datetime.now())
        self.session.add(new_active_user)

        # делаем запись в таблицу с журналирование пользовательских входов
        log = self.LoginHistory(user.id, datetime.datetime.now(), ip_address,
                                port)
        self.session.add(log)

        self.session.commit()

    # регистрация пользователя
    def add_user(self, name, passwd_hash):
        """
        Метод реализует регистрацию пользователя. Делает запись в БД.
        Принимает имя и хеш пароля.
        """
        user_row = self.AllUsers(name, passwd_hash)
        self.session.add(user_row)
        self.session.commit()
        history_row = self.UsersHistory(user_row.id)
        self.session.add(history_row)
        self.session.commit()

    # удаляет пользователя
    def del_user(self, name):
        """
        Метод реализует удаление пользователя из БД.
        """
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.query(self.LoginHistory).filter_by(name=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(user=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(
            contact=user.id).delete()
        self.session.query(self.UsersHistory).filter_by(user=user.id).delete()
        self.session.query(self.AllUsers).filter_by(name=name).delete()
        self.session.commit()

    # получить хеш пароль пользователя
    def get_hash(self, name):
        """Метод получения хеш пароля пользователя."""
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        return user.passwd_hash

    # получить публичный ключ пользователя
    def get_pubkey(self, name):
        """Метод получения публичного ключа пользователя."""
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        return user.pubkey

    # проверяем, существует ли пользователь
    def check_user(self, name):
        """Метод проверяет существование пользователя"""
        if self.session.query(self.AllUsers).filter_by(name=name).count():
            return True
        else:
            return False

    # удаляет пользователя из таблицы активных пользователей при логауте
    def user_logout(self, username):
        """Метод реализует отключение пользователя от сервера."""
        # выбираем нужного пользователя
        user = self.session.query(self.AllUsers).filter_by(
            name=username).first()
        # удаляем его из списка активных
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.commit()

    # ведет подсчет статистики передачи сообщений и записывает в History
    def count_message(self, sender, recipient):
        """Метод ведет подсчет полученных/отправленных сообщений."""
        # Получаем ID отправителя и получателя
        sender = self.session.query(self.AllUsers).filter_by(
            name=sender).first().id
        recipient = self.session.query(self.AllUsers).filter_by(
            name=recipient).first().id
        # Запрашиваем строки из истории и увеличиваем счётчики
        sender_row = self.session.query(self.UsersHistory).filter_by(
            user=sender).first()
        sender_row.sent += 1
        recipient_row = self.session.query(self.UsersHistory).filter_by(
            user=recipient).first()
        recipient_row.accepted += 1
        self.session.commit()

    # добавляет новый контакт для пользователя
    def add_contact(self, user, contact):
        """Метод добаления нового контакта пользователю."""
        # получаем id пользователя и контакта
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(
            name=contact).first()

        # проверяем, что существует и это не дубль
        if not contact or self.session.query(self.UsersContacts).filter_by(
                user=user.id, contact=contact.id).count():
            return

        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    # удаляет контакт из базы
    def del_contact(self, user, contact):
        """Метод удаления контакта пользователя"""
        # получаем id пользователя и контакта
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(
            name=contact).first()

        # проверяем, что существует
        if not contact:
            return

        self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user == user.id,
            self.UsersContacts.contact == contact.id).delete()
        self.session.commit()

    # выводит список всех пользователей
    def users_list(self):
        """
        Метод возвращает список кортежей известных пользователей со временем
        последнего входа. Возвращает кортеж.
        """
        # список всех пользователей - список кортежей (имя, последний логин)
        query = self.session.query(self.AllUsers.name,
                                   self.AllUsers.last_login)
        return query.all()

    # выводит список активных пользователей
    def active_users_list(self):
        """
        Метод возвращает список кортежей активных пользователей. Кортеж
        состоит из имени, IP адреса, порта подключения и времени входа.
        """
        # список активных пользователей -
        # список кортежей - (имя, ip, порт, время)
        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time,
        ).join(self.AllUsers)
        return query.all()

    # выводит пользователя и его последний логин
    def login_history(self, username=None):
        """Метод возвращает список кортежей с историей входа пользователя."""
        # история входов пользователя/пользователей
        query = self.session.query(self.AllUsers.name,
                                   self.LoginHistory.date_time,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port).join(self.AllUsers)
        if username:
            query = query.filter(self.AllUsers.name == username)
        return query.all()

    # список контактов пользователя
    def get_contacts(self, username):
        """Метод возвращает список контактов пользователя."""
        # сам пользователь
        user = self.session.query(self.AllUsers).filter_by(
            name=username).first()

        # его список контактов
        query = self.session.query(self.UsersContacts, self.AllUsers.name). \
            filter_by(user=user.id).join(self.AllUsers,
                                         self.UsersContacts.contact == self.AllUsers.id)

        return [contact[1] for contact in query.all()]

    # выводит количество переданных и полученных сообщений
    def message_history(self):
        """Метод возвращает статистику сообщений пользователя."""
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login,
            self.UsersHistory.sent,
            self.UsersHistory.accepted
        ).join(self.AllUsers)
        # список кортежей
        return query.all()


if __name__ == '__main__':
    test_db = ServerStorage('server_database.db3')
    test_db.add_user('t1', 'asvcbcbvbvbv')
    test_db.user_login('t1', '4.4.1.1', 7777, 'asdasdasdasdasd')
    # test_db.user_login('t2', '7.7.8.8', 6666)
    # test_db.user_login('t3', '7.7.6.6', 5555)
    # test_db.user_logout('t2')
    # test_db.add_contact('t1', 't2')
    # test_db.add_contact('t1', 't3')
    # print(test_db.users_list())
    # print(test_db.active_users_list())
    # print(test_db.get_contacts('t1'))
    # print(test_db.login_history())
    # print(test_db.login_history('test3'))
