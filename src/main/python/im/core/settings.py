# Django settings for mysite project.
import os,sys,hashlib
from im.core.config import conf

sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)))

import warnings
import MySQLdb
warnings.filterwarnings('ignore', category=MySQLdb.Warning)

DEBUG = conf('web.debug')
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {}

for key, c in conf('mysql.databases', {}).iteritems():
    database = {}
    if type(c) is str:
        database['NAME'] = c
        c = {}
    else:
        database['NAME'] = c['name'] if c.get('name') else key

    database['ENGINE'] = c['engine'] if c.get('engine') else "django.db.backends.mysql"
    database['USER'] = c['username'] if c.get('username') else conf('mysql.default_username')
    database['PASSWORD'] = c['password'] if c.get('password') else conf('mysql.default_password')
    database['HOST'] = c['host'] if c.get('host') else conf('mysql.host', '127.0.0.1')
    database['PORT'] = c['port'] if c.get('port') else conf('mysql.port', '3306')

    DATABASES[key] = database

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts

MOUNT_POINT = conf('web.mount')
ALLOWED_HOSTS = [conf('web.host', None)]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Guatemala'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"

STATIC_URL = conf('web.static_url', '/static/')


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    conf('project_path') + '/static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = hashlib.md5(conf('config.artifact', 'default')).hexdigest()

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.doc.XViewMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'cms.middleware.page.CurrentPageMiddleware',
    # 'cms.middleware.user.CurrentUserMiddleware',
    # 'cms.middleware.toolbar.ToolbarMiddleware',
    # 'cms.middleware.language.LanguageCookieMiddleware',    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    # 'cms.context_processors.media',
    # 'sekizai.context_processors.sekizai',
)

ROOT_URLCONF = 'routes'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'


if conf('templates'):
    TEMPLATE_DIRS = conf('templates.directories') + [conf('project_path') + '/templates']
else:
    TEMPLATE_DIRS = ()

INSTALLED_APPS = conf('config.apps')

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db': {
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
#~ 
#~ CACHES = {
    #~ 'default': {
        #~ 'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #~ 'LOCATION': 'unix:/tmp/memcached.sock',
    #~ }
#~ }

if conf('config.apps_params'):
    for key, value in conf('config.apps_params').iteritems():
        vars()[key] = value

