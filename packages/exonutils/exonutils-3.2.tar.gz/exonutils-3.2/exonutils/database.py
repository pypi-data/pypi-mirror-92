# -*- coding: utf-8 -*-
"""
    :copyright: 2020, ExonLabs. All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import logging
import uuid
import sqlalchemy as sa
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from traceback import format_exc

__all__ = ['BaseModel', 'DatabaseHandler']

# supported DB backends
DB_BACKENDS = ['sqlite', 'pgsql', 'mysql', 'mariadb']


def init_db_logging(debug=0):
    # adjust logging for sqlalchemy and alembic
    sqlalchemy_logger = logging.getLogger('sqlalchemy')
    alembic_logger = logging.getLogger('alembic')
    if debug >= 5:
        sqlalchemy_logger.setLevel(logging.DEBUG)
        alembic_logger.setLevel(logging.DEBUG)
    elif debug >= 4:
        sqlalchemy_logger.setLevel(logging.INFO)
        alembic_logger.setLevel(logging.INFO)
    else:
        sqlalchemy_logger.setLevel(logging.ERROR)
        alembic_logger.setLevel(logging.ERROR)


@as_declarative()
class BaseModel(object):

    and_ = sa.and_
    or_ = sa.or_

    guid = sa.Column(
        sa.String(32), primary_key=True, index=True, unique=True,
        autoincrement=False, nullable=False)

    @declared_attr
    def __tablename__(cls):  # noqa
        return cls.__name__.lower()

    def __repr__(self):
        attrs = self.__mapper__.columns.keys()[1:]
        return "%s(%s)" % (
            self.__class__.__name__,
            ', '.join(['%s=%s' % (a, getattr(self, a)) for a in attrs]))

    @classmethod
    def default_orders(cls):
        # Usage:
        # return (cls.COLUMN.asc(), ...)
        return (cls.__mapper__.columns.values()[1].asc(),)

    def modify(self, dbs, data, commit=True):
        for attr, value in data.items():
            if attr != 'guid':
                setattr(self, attr, value)
        dbs.add(self)
        if commit:
            dbs.commit()

    def remove(self, dbs, commit=True):
        dbs.delete(self)
        if commit:
            dbs.commit()

    @classmethod
    def create(cls, dbs, data, commit=True):
        obj = cls()
        obj.guid = uuid.uuid5(uuid.uuid1(), uuid.uuid4().hex).hex
        for attr, value in data.items():
            if attr != 'guid':
                setattr(obj, attr, value)
        dbs.add(obj)
        if commit:
            dbs.commit()
        return obj

    @classmethod
    def update(cls, dbs, filters, data, commit=True):
        q = dbs.query(cls)
        if filters:
            q = q.filter(*filters)
        q.update(data, synchronize_session=False)
        if commit:
            dbs.commit()

    @classmethod
    def delete(cls, dbs, filters, commit=True):
        q = dbs.query(cls)
        if filters:
            q = q.filter(*filters)
        q.delete(synchronize_session=False)
        if commit:
            dbs.commit()

    @classmethod
    def get(cls, dbs, guid):
        return dbs.query(cls).get(guid)

    @classmethod
    def find(cls, dbs, filters, orders=None, offset=0, limit=-1):
        q = dbs.query(cls)
        if filters:
            q = q.filter(*filters)
        orders = orders or cls.default_orders()
        if orders:
            q = q.order_by(*orders)
        return q.offset(offset).limit(limit).all() or []

    @classmethod
    def find_one(cls, dbs, filters):
        q = dbs.query(cls)
        if filters:
            q = q.filter(*filters)
        return q.one_or_none()

    @classmethod
    def count(cls, dbs, filters):
        q = dbs.query(cls)
        if filters:
            q = q.filter(*filters)
        return q.count()

    @classmethod
    def migrate(cls, op, dbs):
        # Usage:
        # op.drop_table(...)
        pass

    @classmethod
    def initial_data(cls, dbs):
        # Usage:
        # cls.create(dbs, ...)
        pass


class DatabaseSessionContext(object):

    def __init__(self, session_factory):
        self._factory = session_factory
        self._session = None

    def __enter__(self):
        self._session = self._factory()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            self._session.close()


class DatabaseHandler(object):

    def __init__(self, backend, database, host=None, port=None,
                 username=None, password=None, debug=0):
        if backend not in DB_BACKENDS:
            raise RuntimeError("invalid backend: %s" % backend)
        if not database:
            raise RuntimeError("no database specified")

        self.debug = debug
        self.engine = None
        self.session_factory = None

        if backend == 'sqlite':
            driver = 'sqlite'
            query = {}
        elif backend == 'pgsql':
            driver = 'postgresql+psycopg2'
            query = {'client_encoding': 'utf8'}
        elif backend in ['mysql', 'mariadb']:
            driver = 'mysql+mysqldb'
            query = {'charset': 'utf8mb4'}

        self.url = sa.engine.url.URL(
            driver, database=database, host=host, port=port,
            username=username, password=password, query=query)

    def init_engine(self, pool=None, connect_timeout=0, query_timeout=0):
        backend = self.url.get_backend_name()
        if backend == 'sqlite':
            self.engine = sa.create_engine(
                self.url, poolclass=sa.pool.NullPool)
        else:
            connect_args = {'connect_timeout': connect_timeout}
            if backend == 'pgsql':
                connect_args.update({
                    'options': "-c statement_timeout=%s" % query_timeout,
                })
            elif backend in ['mysql', 'mariadb']:
                connect_args.update({
                    'read_timeout': query_timeout,
                    'write_timeout': query_timeout,
                })

            if pool and pool.get('size', 0) > 0:
                self.engine = sa.create_engine(
                    self.url,
                    pool_size=pool['size'],
                    max_overflow=pool.get('overflow', 8),
                    pool_timeout=pool.get('timeout', 10),
                    pool_recycle=pool.get('recycle', 1800),
                    connect_args=connect_args)
            else:
                self.engine = sa.create_engine(
                    self.url,
                    poolclass=sa.pool.NullPool,
                    connect_args=connect_args)

    def init_session_factory(self):
        # initialize engine
        if not self.engine:
            self.init_engine()

        # create session factory
        self.session_factory = sa.orm.scoped_session(
            sa.orm.sessionmaker(bind=self.engine))

    def create_session(self):
        # initialize session factory
        if not self.session_factory:
            self.init_session_factory()

        return self.session_factory()

    def session_context(self):
        # initialize session factory
        if not self.session_factory:
            self.init_session_factory()

        return DatabaseSessionContext(self.session_factory)

    def destroy(self):
        if self.session_factory:
            self.session_factory.remove()


def init_database(dbh, models):
    from alembic.operations import Operations
    from alembic.migration import MigrationContext

    err = ''
    try:
        # disable pooling and create db session
        dbh.init_engine(pool=None)
        dbs = dbh.create_session()

        # create database structure
        BaseModel.metadata.create_all(dbh.engine)

        # execute migrations
        conn = dbh.engine.connect()
        op = Operations(MigrationContext.configure(conn))
        for Model in models:
            Model.migrate(op, dbs)
            dbs.commit()

        # load initial models data
        for Model in models:
            Model.initial_data(dbs)
            dbs.commit()

    except Exception:
        err = format_exc().strip()
    finally:
        dbh.destroy()

    if err:
        raise RuntimeError(err)
    return True


def interactive_db_config(backends=None, defaults={}):
    from .console import ConsoleInput as Input

    default_backend = defaults.get('backend', None)
    default_database = defaults.get('database', None)
    default_host = defaults.get('host', 'localhost')
    default_port = defaults.get('port', None)
    default_username = defaults.get('username', None)
    default_password = defaults.get('password', None)

    cfg = {}
    cfg['backend'] = Input.select(
        "Select db backend", backends or DB_BACKENDS,
        default=default_backend, required=True)

    if cfg['backend'] == 'sqlite':
        cfg['database'] = Input.get(
            "Enter db path", default=default_database, required=True)
    else:
        if not default_port:
            if cfg['backend'] in ['pgsql']:
                default_port = 5432
            elif cfg['backend'] in ['mysql', 'mariadb']:
                default_port = 3306

        cfg['database'] = Input.get(
            "Enter db name", default=default_database, required=True)
        cfg['host'] = Input.get(
            "Enter db host", default=default_host, required=True)
        cfg['port'] = Input.number(
            "Enter db port", default=default_port, required=True)
        cfg['username'] = Input.get(
            "Enter db username", default=default_username)
        cfg['password'] = Input.passwd(
            "Enter db password", default=default_password)
        if cfg['password']:
            Input.confirm_passwd(
                "Confirm db password", cfg['password'])

    return cfg


def interactive_db_setup(cfg=None, defaults={}, quiet=False):
    if not cfg:
        cfg = interactive_db_config(defaults=defaults)

    backend = cfg.get('backend', '')
    if backend not in DB_BACKENDS:
        raise RuntimeError("invalid backend: %s" % backend)

    database = cfg.get('database', '')
    if not database:
        raise RuntimeError("empty database name")

    if backend == 'sqlite':
        # create db file
        open(database, 'a').close()
    else:
        fn_setup = eval('interactive_%s_setup' % backend)
        fn_setup(cfg, quiet=quiet)


# pgsql backend setup
def interactive_pgsql_setup(cfg, quiet=False):
    from .console import ConsoleInput as Input
    err = ''
    try:
        from psycopg2 import connect
    except ImportError:
        err = "[psycopg2] backend package not installed"
    if err:
        raise RuntimeError(err)

    host = cfg.get('host', None) or 'localhost'
    port = int(cfg.get('port', '0') or 5432)

    database = cfg.get('database', None)
    if not database:
        raise RuntimeError("invalid empty database name")
    username = cfg.get('username', None)
    if not username:
        raise RuntimeError("invalid empty database username")
    password = cfg.get('password', None)
    if not password:
        raise RuntimeError("invalid empty database password")

    # get superuser access for database setup
    adm_user = Input.get(
        "Enter DB server admin user", default='postgres')
    adm_pass = Input.get(
        "Enter DB server admin password", hidden=True, default='')

    def info(msg):
        if not quiet:
            print(msg)

    # create connection
    conn = connect(host=host, port=port, user=adm_user, password=adm_pass,
                   database='postgres', client_encoding='utf8')
    conn.set_session(autocommit=True)

    # create role
    cur = conn.cursor()
    cur.execute("SELECT * FROM pg_roles WHERE rolname='%s';"
                % (username))
    if not cur.fetchall():
        cur.execute("CREATE ROLE %s LOGIN PASSWORD '%s';"
                    % (username, password))
    else:
        cur.execute("ALTER ROLE %s WITH PASSWORD '%s';"
                    % (username, password))
    cur.close()
    info("-- role created --")

    # create database
    cur = conn.cursor()
    cur.execute("SELECT * FROM pg_database WHERE datname='%s';"
                % (database))
    if not cur.fetchall():
        cur.execute("CREATE DATABASE %s OWNER %s ENCODING 'UTF8'"
                    % (database, username) +
                    " LC_COLLATE 'en_US.UTF-8' LC_CTYPE 'en_US.UTF-8';")
    cur.close()
    info("-- database created --")

    # grant privileges
    cur = conn.cursor()
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s;"
                % (database, username))
    cur.close()
    info("-- privileges added --")

    conn.close()


# mysql backend setup
def interactive_mysql_setup(cfg, quiet=False):
    from .console import ConsoleInput as Input
    err = ''
    try:
        from MySQLdb import connect
    except ImportError:
        err = "[mysqlclient] backend package not installed"
    if err:
        raise RuntimeError(err)

    def info(msg):
        if not quiet:
            print(msg)

    host = cfg.get('host', None) or 'localhost'
    port = int(cfg.get('port', None) or 3306)

    database = cfg.get('database', None)
    if not database:
        raise RuntimeError("invalid empty database name")
    username = cfg.get('username', None)
    if not username:
        raise RuntimeError("invalid empty database username")
    password = cfg.get('password', None)
    if not password:
        raise RuntimeError("invalid empty database password")

    # get superuser access for database setup
    adm_user = Input.get(
        "Enter DB server admin user", default='root')
    adm_pass = Input.get(
        "Enter DB server admin password", hidden=True, default='')

    # create connection
    conn = connect(host=host, port=port, user=adm_user, passwd=adm_pass,
                   charset='utf8mb4')

    # create database
    cur = conn.cursor()
    cur.execute("SHOW DATABASES LIKE '%s';" % database)
    if not cur.fetchall():
        cur.execute("CREATE DATABASE %s" % database +
                    " CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    cur.close()
    info("-- database created --")

    # create user and grant privileges
    cur = conn.cursor()
    cur.execute("SELECT * FROM mysql.user " +
                "WHERE user='%s' AND host='%%';" % username)
    if not cur.fetchall():
        cur.execute("CREATE USER '%s'@'%%' IDENTIFIED BY '%s';"
                    % (username, password))
    else:
        cur.execute("ALTER USER '%s'@'%%' IDENTIFIED BY '%s';"
                    % (username, password))
    cur.execute("GRANT ALL ON %s.* TO %s@'%%';" % (database, username))
    cur.execute("FLUSH PRIVILEGES;")
    cur.close()
    info("-- user created --")
    info("-- privileges added --")

    conn.close()


# mariadb backend setup
def interactive_mariadb_setup(cfg, quiet=False):
    interactive_mysql_setup(cfg, quiet=quiet)
