"""Server database"""
import datetime

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, \
    DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class ServerDataBase:
    """
    Класс - оболочка для работы с базой данных сервера.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется классический подход.
    """

    class AllUsers:
        """Класс - отображение таблицы всех пользователей."""

        def __init__(self, username, passwd_hash):
            self.id = None
            self.name = username
            self.last_login = datetime.datetime.now()
            self.passwd_hash = passwd_hash
            self.pubkey = None

    class ActiveUsers:
        """Класс - отображение таблицы активных пользователей."""

        def __init__(self, user_id, ip_address, port, login_time):
            self.id = None
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time

    class LoginHistory:
        """Класс - отображение таблицы истории входов."""

        def __init__(self, user_id, date, ip_address, port):
            self.id = None
            self.user = user_id
            self.date = date
            self.ip_address = ip_address
            self.port = port

    class UsersContacts:
        """Класс - отображение таблицы контактов пользователей."""

        def __init__(self, user_id, contact_name):
            self.id = None
            self.user = user_id
            self.contact = contact_name

    class UsersMessageStats:
        """Класс - отображение таблицы статистики действий."""

        def __init__(self, user_id):
            self.id = None
            self.user = user_id
            self.sent = 0
            self.received = 0

    def __init__(self, path):
        # Создаём движок базы данных
        self.database_engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})

        # Создаём объект MetaData
        self.metadata = MetaData()

        # Создаём таблицу пользователей
        users_table = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime),
                            Column('passwd_hash', String),
                            Column('pubkey', Text)
                            )

        # Создаём таблицу активных пользователей
        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id'), unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime)
                                   )

        # Создаём таблицу истории входов
        user_login_history = Table('login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id')),
                                   Column('date', DateTime),
                                   Column('ip_address', String),
                                   Column('port', Integer)
                                   )

        # Создаём таблицу контактов пользователей
        contacts = Table('Contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('user', ForeignKey('Users.id')),
                         Column('contact', ForeignKey('Users.id'))
                         )

        # Создаём таблицу статистики пользователей
        users_message_stats = Table('Message_stats', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('user', ForeignKey('Users.id')),
                                    Column('sent', Integer),
                                    Column('received', Integer)
                                    )

        # Создаём таблицы
        self.metadata.create_all(self.database_engine)

        # Создаём отображения
        mapper(self.AllUsers, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.LoginHistory, user_login_history)
        mapper(self.UsersContacts, contacts)
        mapper(self.UsersMessageStats, users_message_stats)

        # Создаём сессию
        session = sessionmaker(bind=self.database_engine)
        self.session = session()

        # Если в таблице активных пользователей есть записи, то их необходимо удалить
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port, key):
        """
        Метод выполняющийся при входе пользователя, записывает в базу факт входа
        Обновляет открытый ключ пользователя при его изменении.
        """

        # Запрос в таблицу пользователей на наличие там пользователя с таким именем
        user_in_base = self.session.query(self.AllUsers).filter_by(name=username)

        # Если имя пользователя уже присутствует в таблице, обновляем время последнего входа
        # и проверяем корректность ключа. Если клиент прислал новый ключ, сохраняем его.
        if user_in_base.count():
            user = user_in_base.first()
            user.last_login = datetime.datetime.now()
            if user.pubkey != key:
                user.pubkey = key

        # Если нету, то генерируем исключение
        else:
            raise ValueError('Пользователь не зарегистрирован.')

        # Теперь можно создать запись в таблицу активных пользователей о факте входа.
        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(new_active_user)

        # и сохранить в историю входов
        new_history_user = self.LoginHistory(user.id, datetime.datetime.now(), ip_address, port)
        self.session.add(new_history_user)

        # Сохрраняем изменения
        self.session.commit()

    def add_user(self, name, passwd_hash):
        """
        Метод регистрации пользователя.
        Принимает имя и хэш пароля, создаёт запись в таблице статистики.
        """

        user_row = self.AllUsers(name, passwd_hash)
        self.session.add(user_row)
        self.session.commit()

        stats_row = self.UsersMessageStats(user_row.id)
        self.session.add(stats_row)
        self.session.commit()

    def remove_user(self, name):
        """Метод удаляющий пользователя из базы."""
        user = self.session.query(self.AllUsers).filter_by(name=name).first()

        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.query(self.LoginHistory).filter_by(user=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(user=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(contact=user.id).delete()
        self.session.query(self.UsersMessageStats).filter_by(user=user.id).delete()
        self.session.query(self.AllUsers).filter_by(name=name).delete()

        self.session.commit()

    def get_hash(self, name):
        """Метод получения хэша пароля пользователя."""

        user = self.session.query(self.AllUsers).filter_by(name=name).first()

        return user.passwd_hash

    def get_pubkey(self, name):
        """Метод получения публичного ключа пользователя."""

        user = self.session.query(self.AllUsers).filter_by(name=name).first()

        return user.pubkey

    def check_user(self, name):
        """Метод проверяющий существование пользователя."""

        if self.session.query(self.AllUsers).filter_by(name=name).count():
            return True
        else:
            return False

    def user_logout(self, username):
        """Метод фиксирующий отключения пользователя."""

        # Запрашиваем пользователя, что покидает нас
        user = self.session.query(self.AllUsers).filter_by(name=username).first()

        # Удаляем его из таблицы активных пользователей.
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()

        # Применяем изменения
        self.session.commit()

    def process_message(self, sender, recipient):
        """Метод записывающий в таблицу статистики факт передачи сообщения."""

        # Получаем ID отправителя и получателя
        sender = self.session.query(self.AllUsers).filter_by(name=sender).first().id
        recipient = self.session.query(self.AllUsers).filter_by(name=recipient).first().id

        # Запрашиваем строки из статистики и увеличиваем счётчики
        sender_row = self.session.query(self.UsersMessageStats).filter_by(user=sender).first()
        sender_row.sent += 1

        recipient_row = self.session.query(self.UsersMessageStats).filter_by(user=recipient).first()
        recipient_row.received += 1

        self.session.commit()

    def add_contact(self, user, contact):
        """Метод добавления контакта для пользователя."""

        # Получаем ID пользователя
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(name=contact).first()

        # Проверяем что не дубль и что контакт может существовать (полю
        # пользователь мы доверяем)
        if not contact or self.session.query(self.UsersContacts).filter_by(
                user=user.id, contact=contact.id).count():
            return

        # Создаём объект и заносим его в базу
        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def remove_contact(self, user, contact):
        """Метод удаления контакта пользователя."""

        # Получаем ID пользователя
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(name=contact).first()

        # Проверяем что контакт может существовать (полю пользователь мы
        # доверяем)
        if not contact:
            return

        # Удаляем требуемое
        self.session.query(self.UsersContacts).filter_by(user=user.id, contact=contact.id).delete()

        self.session.commit()

    def users_list(self):
        """Метод возвращающий список известных пользователей со временем последнего входа."""

        # Запрос строк таблицы пользователей.
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login,
        )

        return query.all()

    def active_users_list(self):
        """Метод возвращающий список активных пользователей."""

        # Запрашиваем соединение таблиц и собираем кортежи имя, адрес, порт, время.
        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time,
        ).join(self.AllUsers)

        return query.all()

    def login_history(self, username=None):
        """Метод возвращающий историю входов."""

        # Запрашиваем историю входа
        query = self.session.query(
            self.AllUsers.name,
            self.LoginHistory.date,
            self.LoginHistory.ip_address,
            self.LoginHistory.port
        ).join(self.AllUsers)

        # Если было указано имя пользователя, то фильтруем по нему
        if username:
            query = query.filter(self.AllUsers.name == username)

        return query.all()

    def get_contacts(self, username):
        """Метод возвращающий список контактов пользователя."""

        # Запрашивааем указанного пользователя
        user = self.session.query(self.AllUsers).filter_by(name=username).one()

        # Запрашиваем его список контактов
        query = self.session.query(
            self.UsersContacts,
            self.AllUsers.name,
        ).filter_by(user=user.id).join(self.AllUsers,
                                       self.UsersContacts.contact == self.AllUsers.id)

        # выбираем только имена пользователей и возвращаем их.
        return [contact[1] for contact in query.all()]

    def message_stats(self):
        """Метод возвращающий статистику сообщений."""

        query = self.session.query(
            self.AllUsers.name,
            self.UsersMessageStats.sent,
            self.UsersMessageStats.received,
            self.AllUsers.last_login,
        ).join(self.AllUsers)

        return query.all()
