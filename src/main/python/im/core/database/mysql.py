# TODO sqlalchemy.exc.ProgrammingError catch ? fatal?
# TODO use bind_arguments from werkzeug to generate cache key

import os, sys
import logging

if sys.version_info < (2, 7, 0):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

import hashlib

from sqlalchemy import orm
from sqlalchemy.schema import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Column as BaseColumn
from werkzeug.contrib.cache import MemcachedCache
# from ordereddict import OrderedDict

from im.core.web.bootstrap import icons
from im.core.utils.path import get_project_path
from im.core.config import configs, RecursiveDict, conf




logger = logging.getLogger('im.core.database.mysql')

databases = {}
file_queries = {}

class QueryFileNotFound(Exception):
    pass


class DatabaseSessionStore(object):

    default_configuration = RecursiveDict({
        'autocommit': True,
        'autoflush': True,
        'pool_size': 8,
        'pool_recycle': 300,
        'host': '127.0.0.1',
        'port': 3306,
        })

    def __init__(self, config=None):
        self.config = self.default_configuration
        self.config.update_recursive(configs.get('mysql', {}))
        if config:
            self.config.update_recursive(config)
        self.metadatas = {}
        self.engines = {}
        self.sessions = {}
        self.models = {}

    def _get_metadata(self, database, engine):
        if database in self.metadatas:
            return self.metadatas[database]
        metadata = MetaData(bind=engine)
        self.metadatas[database] = metadata
        return metadata

    def _get_engine(self, database):
        if database in self.engines:
            return self.engines[database]
        connection_string = self._connection_string(database)
        engine = create_engine(connection_string, logging_name=database,
            pool_logging_name=database, pool_size=self.config.get('pool_size'),
            pool_recycle=self.config.get('pool_recycle'))
        self.engines[database] = engine
        return engine

    def _get_session(self, database):
        if database in self.sessions:
            logger.info('Existing session for database: %s' % database)
            return self.sessions[database]()
        logger.info('Getting session for database: %s' % database)
        engine = self._get_engine(database)
        self._get_metadata(database, engine)
        self.sessions[database] = orm.scoped_session(orm.sessionmaker(
            bind=engine,
            autoflush=self.config.get('autoflush'),
            autocommit=self.config.get('autocommit')
        ))
        return self.sessions[database]()

    def _connection_string(self, database):
        databases = self.config['databases']
        d = databases.get(database, None)
        database_name = database

        # check if config is a string and not a dict
        # then its pointing to another db config
        if isinstance(d, basestring):
            database_name = d
            try:
                d = databases[database_name]
            except KeyError:
                d = None

        # if the config for the database exists but is empty use defaults
        if d is None:
            self.config['databases'][database] = {
                'host': self.config.get('host'),
                'port': self.config.get('port'),
                'username': self.config.get('default_username'),
                'password': self.config.get('default_password'),
                }
            d = self.config['databases'][database]

        if 'name' in d:
            database_name = d['name']

        conn = 'mysql://%(username)s:%(password)s@%(host)s:%(port)s/%(db)s'
        parameters = {
            'host': d.get('host', self.config.get('host')),
            'port': d.get('port', self.config.get('port')),
            'username': d.get('username', self.config.get('default_username')),
            'password': d.get('password', self.config.get('default_password')),
            'db': database_name
        }
        to_use = conn % parameters
        parameters.update({'password': '******'})
        to_debug = conn % parameters
        logger.info('Connection: %s' % to_debug)
        return to_use

    def remove_all(self):
        logger.debug('Removing all database sessions')
        for (key, session) in self.sessions.iteritems():
            session.remove()

    def close_all(self):
        logger.debug('Closing all database sessions')
        for (key, session) in self.sessions.iteritems():
            session.close()

    def get(self, database):
        return self._get_session(database)

    def get_model_reflected(self, table, database='default', **kwargs):
        class_name = '%s%s' % (
            table.capitalize(),
            ''.join([i.capitalize() for i in database.split('_')])
            )
        if class_name in self.models:
            _class = self.models[class_name]
        else:
            engine = self._get_engine(database)
            metadata = self._get_metadata(database, engine)
            _class = type(str(class_name), (object,), {})
            table = Table(table, metadata, autoload=True, autoload_with=engine)
            orm.mapper(_class, table, **kwargs)
            self.models[class_name] = _class
        return _class

    def query_reflected(self, table, database='default'):
        _class = self.get_model_reflected(table, database)
        session = self._get_session(database)
        return session.query(_class)


sessions = DatabaseSessionStore()


class Query(object):

    default_configuration = RecursiveDict({
        'query_directories': [],
        'cached': False,
        'execute_queries': True,
        })

    def __init__(self, query, params=None, from_file=True, model_class=None,
                 database='default', sessions=sessions, cached=False,
                 replace=None, config=None, cache_timeout=3600*12):

        self.config = self.default_configuration
        self.config.update_recursive(configs.get('mysql', {}))
        if config:
            self.config.update_recursive(config)

        # add project path queries directory if not already configured
        project_queries = os.path.join(get_project_path(), 'queries')
        if not project_queries in self.config['query_directories']:
            self.config['query_directories'].append(project_queries)

        if from_file:
            if query in file_queries:
                logger.debug('Getting query file from query files cache %s' %
                             query)
                self.query = file_queries[query]
            else:
                logger.debug('Getting query file %s' % query)
                file_queries[query] = self._get_from_file(query)
                self.query = file_queries[query]
        else:
            self.query = query

        if replace:
            self.query = self.query % replace

        self.params = params
        self.session = sessions.get(database)
        self.result = None
        self.model_class = model_class
        self.cached = cached
        self.query_cache = MemcachedCache(['127.0.0.1:11211'])
        self.cache_timeout = cache_timeout
        self.database = database

    def _gen_mem_key(self):
        params_string=''
        if self.params:
            ordered_values =  OrderedDict(sorted(self.params.items(),
                key=lambda t: t[0]))
            for value in ordered_values:
                params_string = params_string +'_'+ value
            return str(hash(self.database+'_'+self.query+params_string))

    def _get_from_file(self, query):
        for query_directory in self.config.get('query_directories'):
            for dirpath, dirnames, filenames in os.walk(query_directory,
                                                        followlinks=True):
                for name in filenames:
                    if '%s.sql' % query in os.path.join(dirpath, name):
                        f = file(os.path.join(dirpath, name))
                        query = f.read()
                        f.close()
                        return query
        raise QueryFileNotFound('%s.sql not found in any of %s' %
                                (query, self.config.get('query_directories')))

    def _raw_query(self):
        if self.config.get('execute_queries'):
            self.result = self.session.execute(self.query, self.params)
        else:
            self.result = None

    def _raw_query_with_model(self):
        if self.config.get('execute_queries'):
            self.result = self.session.query(self.model_class).from_statement(self.query).params(**self.params)
        else:
            self.result = None

    def _query(self):
        if self.model_class:
            self._raw_query_with_model()
        else:
            self._raw_query()

    def execute(self):
        self._query()
        return self.result

    def one(self):
        cache_key = ''
        if self.cached:
            cache_key = self._gen_mem_key()
            cached_query = self.query_cache.get(cache_key)
            if cached_query:
                return cached_query
        self._query()
        if self.result:
            if self.model_class:
                _one = self.result.one()
                if self.cached:
                    self.query_cache.set(cache_key,
                                         _one,self.cache_timeout)
                return _one
            else:
                fetch_one = self.result.fetchone()
                if self.cached:
                    self.query_cache.set(cache_key,
                                         fetch_one, self.cache_timeout)
                return fetch_one
        if self.cached:
            self.query_cache.set(cache_key, self.result, self.cache_timeout)
        return self.result

    def all(self):
        cache_key = ''

        if self.cached:
            cache_key = self._gen_mem_key()
            cached_query = self.query_cache.get(cache_key)
            if cached_query:
                return cached_query
        self._query()
        if self.result:
            if self.model_class:
                _all = self.result.all()
                if self.cached:
                    query_cache.set(cache_key, _all, self.cache_timeout)
                return _all
            else:
                fetch_all = self.result.fetchall()
                if self.cached:
                    self.query_cache.set(cache_key, fetch_all,
                                         self.cache_timeout)
                return fetch_all
        if self.cached:
            self.query_cache.set(cache_key, self.result, self.cache_timeout)
        return self.result




    @staticmethod
    def last_insert_id():
        return Query('last_insert_id').one()[0]


class Column(BaseColumn):

    _constructor = BaseColumn

    def __add_property__(self, name, kwargs):
        if not name in self.__dict__:
            self.__dict__[name] = None
            if name in kwargs:
                self.__dict__[name] = kwargs[name]
                del kwargs[name]

    @property
    def __icon__(self):

        column_name = self
        if hasattr(self, 'name'):
            column_name = self.name

        if column_name in icons:
            icon = icons[column_name]
        elif column_name.endswith('_id'):
            icon = icons['id']
        elif column_name.startswith('is_') or column_name.startswith('has_') or column_name.startswith('allows_'):
            icon = icons['is_active']
        elif 'message' in column_name:
            icon = icons['message']
        elif hasattr(self, 'type'):
            type_icon = {
                'DATETIME': 'icon-calendar',
                'DATE': 'icon-calendar',
                'TEXT': 'icon-align-left',
                'STRING': 'icon-align-left',
                'VARCHAR': 'icon-align-left',
                }
            icon = str(self.type).split('(')[0]
            if icon in type_icon:
                icon = type_icon[icon]
        else:
            icon = ''

        return icon

    def __init__(self, *args, **kwargs):

        self.__add_property__('read_only', kwargs)
        self.__add_property__('max_length', kwargs)
        self.__add_property__('help', kwargs)
        self.__add_property__('icon', kwargs)

        verbose_name = None
        if 'verbose_name' in kwargs:
            verbose_name = kwargs['verbose_name']
            del kwargs['verbose_name']

        super(Column, self).__init__(*args, **kwargs)

        if self.name and not verbose_name:
            verbose_name = ' '.join([i.capitalize for i in self.name.split('_')])

        verbose_name = {'verbose_name': verbose_name}
        if self.info:
            self.info.update(verbose_name)
        else:
            self.info = verbose_name

class BaseModel(object):
    __columns_renderers_on_list__ = {}
    __columns_renderers_on_show__ = {}
    __columns_renderers_on_update__ = {}
    __columns_extra_on_list__ = {}
    __columns_exclude_on_list__ = []
    __load_relations_on_add__ = {}
    __extra_filters__ = {}

    def __str__(self):
        return self.__unicode__()


Model = declarative_base(cls=BaseModel)
