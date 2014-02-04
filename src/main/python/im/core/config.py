
import os
import logging
import logging.handlers
import platform
import collections

from im.core.utils.args import Args
from im.core.utils.yaml import load_yaml, YAML_EXTENSION
from im.core.utils.imports import import_string
from im.core.utils.path import get_project_path, \
    set_project_path as _set_project_path

_local_paths = None

FEATURES_LIST = [
    'templates',
    'logging',
    'bottle',
    'werkzeug',
    'mongodb',
    'mysql',
    'activemq',
    'esmes',
    'routes',
    'args',
]

logger = logging.getLogger('im.core.config')


class RecursiveDict(dict):
    """Allows a dict to be updated with another dict recursively
    using update_recursive.

    >>> r = RecursiveDict({'data': {'one': 1, 'two': 2}})
    >>> r.update_recursive({'data': {'three': 3}})
    >>> r.get('data').get('three')
    3
    """

    def __init__(self, defaults=None):
        """
        :param defaults: Dictionary to pre-populate, defaults to None
        """
        dict.__init__(self, defaults or {})

    def update_recursive(self, other):
        """Recursively update

        :param other: Dictionary to update with
        """
        try:
            iterator = other.iteritems()
        except AttributeError:
            iterator = other
        self._update_recursive(iterator)

    def _update_recursive(self, iterator):
        for (key, value) in iterator:
            if key in self and isinstance(self[key], collections.Mapping) \
                and isinstance(value, collections.Mapping):
                self[key] = RecursiveDict(self[key])
                self[key].update_recursive(value)
            else:
                self[key] = value


class YamlConfig(RecursiveDict):
    """A :class:`RecursiveDict` that loads a YAML configuration file,
    allowing to use a list of paths for configuration override.

    :param key: The key to identify this YAML config, also used as the \
    filename of the YAML file.

    :param defaults: Dictionary to pre-populate, defaults to None.

    :param loader: A callable to use for loading the YAML file, defaults to \
    :func:`im.core.utils.yaml.load_yaml`

    :param paths: A list of paths to search for the YAML configuration \
    file. Will recursively update with every file found in paths.
    """

    def __init__(self, key, defaults=None, loader=load_yaml, paths=None):
        super(YamlConfig, self).__init__(defaults or {})
        self.key = key

        if isinstance(paths, basestring):
            paths = [paths]

        for path in paths:
            if not isinstance(path, basestring):
                raise TypeError('Invalid path: %s' % repr(path))
            yaml = os.path.join(path, '%s.%s' % (self.key, YAML_EXTENSION))
            self.update_recursive(loader(yaml, {}))


class YamlLocalConfig(RecursiveDict):
    """A :class:`RecursiveDict` that loads local YAML configuration files.

    Uses this convention order for searching the files:

    1.  First search on the defaults configs directory
    2.  Then on the globals configs directory
    3.  Then on the application configs directory.

    For every one of those files it checks for a version for the current node
    python is running.

    Does a recursive update on every config file found, allowing for
    configuration files override.

    :param key: The key to identify this YAML config, also used as the \
    filename of the YAML file.

    :param defaults: Dictionary to pre-populate, defaults to None.

    :param config_type: Used for feature config files named differently than \
    the feature, for example a logging config file could be called log, this \
    allows the :func:`configure` function to call the feature configuration \
    callable if available.

    :param loader: A callable to use for loading the YAML file, defaults to \
    :func:`im.core.utils.yaml.load_yaml`
    """
    def __init__(self, key, defaults=None, loader=load_yaml, config_type=None):
        super(YamlLocalConfig, self).__init__(defaults or {})
        self.key = key

        for path in _local_paths:

            key = self.key
            key_split = key.split('.')

            if '/\\' in path[-1]:
                path = path[:-1]

            if os.path.basename(path) == 'defaults' and key_split > 1:
                if key_split in FEATURES_LIST:
                    key = self.key.split('.')[-1]
                elif key not in FEATURES_LIST and config_type in FEATURES_LIST:
                    key = config_type

            yaml = os.path.join(path, '%s.%s' % (key, YAML_EXTENSION))
            logger.debug('Loading YAML %s', yaml)
            self.update_recursive(loader(yaml, {}))

            local_key = '%s.%s' % (key, platform.node())
            local_yaml = os.path.join(path, '%s.%s' % (local_key, YAML_EXTENSION))
            logger.debug('Loading local YAML %s', yaml)
            self.update_recursive(loader(local_yaml, {}))


class ObjectConfig(dict):
    """A dict that loads all uppercase attributes from a module or an object, all
    configuration keys are set to lowercase.

    :param key: Used to identify this object config

    :param obj: the object or module to load the configuration items

    :param defaults: Dictionary to pre-populate, defaults to None.

    >>> class MyConfig(): pass
    >>> obj = MyConfig()
    >>> obj.ONE, obj.TWO = 1, 2
    >>> config1 = ObjectConfig('my_config', obj)
    >>> config2 = {'three': 3}
    >>> config1.update(config2)
    >>> config1.get('two')
    2
    >>> config1.get('three')
    3
    """
    def __init__(self, key, obj, defaults=None):
        dict.__init__(self, defaults or {})
        self.key = key

        if isinstance(obj, basestring):
            obj = import_string(obj)

        for key in dir(obj):
            if key.isupper():
                self[key.lower()] = getattr(obj, key)


class DatabaseConfig(dict):
    pass


class ConfigStore(dict):
    """A dict used to load and store configuration files/objects.

    :param defaults: Dictionary to pre-populate, defaults to None.

    >>> store = ConfigStore()
    >>> class MyConfig(): pass
    >>> obj = MyConfig()
    >>> obj.ONE, obj.TWO = 1, 2
    >>> store.load_config('my_config', obj=obj, config_class=ObjectConfig)
    {'two': 2, 'one': 1}
    >>> store.get('my_config').get('two')
    2
    >>> store['my_config']['one']
    1
    """
    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def load_config(self, key, defaults=None, config_class=YamlLocalConfig,
            override='NONE', **kwargs):
        """Loads a configuration.

        :param key: Key to identify the configuration, used also as filename on \
        YAML file configs.

        :param defaults: Dictionary to pre-populate, defaults to None.

        :param config_class: Callable used to load the configuration. By default \
        uses the :class:`YamlLocalConfig` class for loading YAML files.

        :param override: 'NONE' means no replacement, 'FULL' means replacing the file completely,
        'PARTIAL' means replacing the explicit keys

        :param config_type: Used for :class:`YamlLocalConfig` when the key is \
        named differently than the feature it represents.
        """
        name = kwargs['config_type'] if 'config_type' in kwargs else key
        tmp = None
        if name in self and override == 'NONE':
            return self[name]

        if name in self and override == 'PARTIAL':
            tmp = self[name]

        if isinstance(key, list):
            self[name] = RecursiveDict(defaults)
            for item in key:
                self[name].update_recursive(
                    config_class(item, **kwargs)
                )
        else:
            self[name] = config_class(key, defaults=defaults, **kwargs)

        if tmp:
            for key, value in self[name].iteritems():
                if tmp.get(key) and not self[name].get(key):
                    self[name][key] = tmp[key]
        return self[name]

    def conf(self, config, default=None):
        search = config.split('.')

        try:
            self[search[0]]
        except KeyError:
            logger.debug('Could not get key %s from config', config)
            return default

        if len(search) == 1:
            return self[config]

        d = self
        for item in search:
            d = d.get(item)

        if not d:
            d = default

        return d


configs = ConfigStore()
conf = configs.conf
msg = None


def _get_features_config(key='features', override='NONE'):
    return configs.load_config(
        key,
        config_class=YamlConfig,
        # paths=os.path.join(get_project_path(), 'configs')
        paths=_local_paths,
        override=override
    )


def _configure_logging(directory=None):
    logging_config = configs['logging']

    formatter = logging.Formatter(
        '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')

    root_logger = logging.getLogger('')
    
    if len(root_logger.handlers) > 0:
        return
    
    root_logger.setLevel(logging.getLevelName(
        logging_config.get('default_level', logging.WARNING).upper()))

    if logging_config.get('console_level') is not None:

        consoleLogger = logging.StreamHandler()
        consoleLogger.setLevel(logging.getLevelName(
            logging_config.get('console_level').upper()))
        consoleLogger.setFormatter(formatter)
        root_logger.addHandler(consoleLogger)

    if logging_config.get('file_path') is not None:

        fileLogger = logging.handlers.TimedRotatingFileHandler(
            filename=logging_config.get('file_path'),
            when=logging_config.get('rotation_when'),
            interval=logging_config.get('rotation_interval')
        )
        fileLogger.setLevel(logging.getLevelName(
            logging_config.get('file_level', logging.WARNING).upper()))
        fileLogger.setFormatter(formatter)
        root_logger.addHandler(fileLogger)

    loggers = logging_config['loggers']
    for logger_name in loggers:
        logger_config = loggers[logger_name]
        if logger_config:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.getLevelName(
                logger_config.get('level', logging.WARNING).upper()))


def _configure_werkzeug(directory=None):
    global configs

    if not directory:
        directory = ''

    configs['werkzeug']['routes'] = YamlConfig(
        'routes',
        paths=os.path.join(get_project_path(), 'configs', directory)
    )


def _configure_args(directory=None):
    global configs
    configs['args']['parsed'] = Args(configs.get('args')).args


def _configure_messages(directory=None):
    global msg
    msg = configs['messages'].get


configure_functions = {
    'logging': _configure_logging,
    'werkzeug': _configure_werkzeug,
    'args': _configure_args,
    'messages': _configure_messages,
}


def configure(config_dict='features', set_project_path=None,
              configure_functions=configure_functions,
              directory=None, local_paths=None, override='NONE'):
    """Allows easy configuration of core features. Format is
    feature => key (for use when loading the YAML file when the config file
    is not named after the feature). If the key is None then will load the
    config file with the feature name.

    If a callable is available in ``configure_functions`` for the feature will
    call it with the config loaded.

    Automatically loads the global config file.

    :param config_dict: A string or dict with the features to configure. If a \
    string then will search for a YAML file in configs directory with that \
    key.

    :param configure_functions: A dict with features and their callable, if \
    a callable for the feature is available it will be called with the config \
    loaded.

    :param local_paths: The paths to use for local configuration files loading,\
    if local_paths is None will use the default config paths.
    """
    global _local_paths
    
    if set_project_path is not None:
        _set_project_path(set_project_path)

    configs.load_config('global_config', config_class=YamlConfig, paths='/etc/im/')

    if local_paths is None:
        if _local_paths is None:
            _local_paths = [
                os.path.join(configs['global_config']['configs_path'], 'defaults'),
                os.path.join(configs['global_config']['configs_path'], 'globals'),
                os.path.join(get_project_path(), 'configs'),
            ]
        else:
            _local_paths.append(os.path.join(get_project_path(), 'configs'))
    else:
        _local_paths = local_paths

    if isinstance(config_dict, basestring):
        if directory:
            config_dict = os.path.join(directory, config_dict)
        config_dict = _get_features_config(config_dict, override=override)
        
    for key, value in config_dict.iteritems():
        if value is None:
            configs.load_config(key, override=override)
        else:
            configs.load_config(value, config_type=key, override=override)

        if key in configure_functions:
            configure_functions[key](directory)

    configs['project_path'] = get_project_path()

