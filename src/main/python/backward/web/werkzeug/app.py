
from __future__ import absolute_import

import json
import copy
import urllib
import urlparse

from werkzeug.exceptions import abort
from werkzeug.routing import Rule, Map
from werkzeug.wsgi import get_current_url
from werkzeug.contrib.sessions import FilesystemSessionStore
from werkzeug.wrappers import BaseRequest, Response, BaseResponse
from werkzeug.utils import cached_property, redirect, import_string

from im.core.config import conf
from im.core.web.app import App as CoreApp
from im.core.web.flash import get_flash_messages
from im.core.database.mysql import sessions as sa_sessions

session_store = FilesystemSessionStore(
    path=conf('werkzeug.sessions_path', None),
    renew_missing=conf('werkzeug.sessions_renew_missing', False),
    filename_template=conf('werkzeug.sessions_filename_template', 'im_%s.sess')
)


class Request(BaseRequest):

    session = None
    charset = 'utf-8'
    encoding_errors = 'utf-8'

    def __init__(self, environ, populate_request=True, shallow=False):

        super(Request, self).__init__(environ, populate_request=True, shallow=False)

        if conf('werkzeug.sessions'):
            sid = self.cookies.get(conf('werkzeug.cookie_name'))
            if sid is None:
                self.session = session_store.new()
            else:
                self.session = session_store.get(sid)
        else:
            self.session = None

    def end(self, response):

        if conf('werkzeug.sessions'):
            if self.session.should_save:
                session_store.save(self.session)
                response.set_cookie(conf('werkzeug.cookie_name'), self.session.sid)

        if conf('werkzeug.sa_remove_sessions'):
            if sa_sessions:
                sa_sessions.remove_all()

    def logout(self):
        self.session.pop('username', None)
        self.session.pop('user_roles', None)

    def login(self, username, roles=None):
        self.session['username'] = username
        self.session['user_roles'] = roles

    @property
    def logged_in(self):
        if not conf('werkzeug.use_auth'):
            return True
        return self.session.get('username', False)

    @property
    def user_roles(self):
        if not conf('werkzeug.use_auth'):
            return None
        return self.session.get('user_roles')

    @cached_property
    def json(self):
        if self.headers.get('content-type') == 'application/json':
            return json.loads(self.data)


class Routing(object):

    def __init__(self, environ, request):
        self.config = conf('werkzeug')
        self.endpoints = {}
        self.load()

    def load(self):
        rules = []
        routes = self.config.get('routes', False)
        subdomain = routes.get('subdomain', '')
        if routes:
            module = routes.get('module', '')
            endpoints = routes.get('endpoints', [])
            for url in endpoints:
                args = {}
                config = copy.copy(endpoints[url])
                if isinstance(config, dict):
                    controller = config['controller']
                    del config['controller']
                    args = config
                else:
                    controller = config
                if url[-1:] != '/':
                    url = '%s/' % url
                rules.append(Rule(url, endpoint='%s.%s' % (module, controller),
                    **args))

        self.routes = Map(rules, default_subdomain=subdomain)
        port = self.config.get('port')
        self.urls_mapper = self.routes.bind(
            self.config.get('host') + ':%s' % (port if port and port != '80' else ''),
            self.config.get('mount_point'),
            url_scheme=self.config.get('url_scheme'),
        )

    def __automatic_routing(self, request):
        module_parts = filter(None, request.environ.get('PATH_INFO').split('/'))
        controller = controller_module = function = None
        counter = len(module_parts)
        endpoint = '.'.join(module_parts)
        values = {}

        routes = self.config.get('routes', False)
        if routes:
            controllers_module_base = routes.get('module')
        else:
            controllers_module_base = 'controllers'

        while counter > 0:
            module = module_parts[:counter]

            if len(module) == 1:
                module = controllers_module_base
            else:
                module = '%s.%s' % (controllers_module_base, '.'.join(module[:counter - 1]))


            try:
                controller_module = import_string(module)
            except AttributeError:
                controller_module = False

            if controller_module and not callable(controller_module):
                function = module_parts[counter - 1:counter][0]
                values = module_parts[counter:]
                break

            counter -= 1

        if controller_module and function:
            expose = hasattr(controller_module, 'expose')
            exposed = expose and function in getattr(controller_module, 'expose')
            public = not expose and not function.startswith('_')\
            and getattr(controller_module, function)
            if exposed or public:
                endpoint = request.environ.get('PATH_INFO')
                controller = getattr(controller_module, function)
                if callable(controller):
                    if endpoint in self.endpoints:
                        controller = self.endpoints[endpoint]
                    else:
                        self.endpoints[endpoint] = controller

        return controller, endpoint, values

    def controller_from_request(self, request):
        controller = None
        values = {}

        if self.config.get('allow_automatic_routing'):
            controller, endpoint, values = self.__automatic_routing(request)

        if not controller:
            adapter = self.routes.bind_to_environ(request.environ)
            endpoint, values = adapter.match()
            if endpoint in self.endpoints:
                controller = self.endpoints[endpoint]
            else:
                if len(endpoint.split('.')) == 1:
                    module = endpoint
                else:
                    module = ".".join(endpoint.split('.')[:-1])
                function = endpoint.split('.')[-1]
                controller_module = import_string(module)
                controller = getattr(controller_module, function)
                self.endpoints[endpoint] = controller

        return controller, values


class ControllerLoader(object):

    response_class = Response

    def __init__(self, environ, request):
        self.environ = environ
        self.request = request
        self.routing = Routing(environ, request)

    def get(self):

        if conf('werkzeug.mount_point') and \
           not conf('werkzeug.multiple_mount_points', False):
            current_path = '/%s%s' % (
                conf('werkzeug.mount_point', ''),
                self.request.path
            )
        else:
            current_path = self.request.path

        if conf('werkzeug.use_auth')\
           and hasattr(self.request, 'logged_in')\
           and not self.request.logged_in\
           and current_path != conf('werkzeug.login_url'):
            return redirect(conf('werkzeug.login_url')), None

        return self.routing.controller_from_request(self.request)


class TemplateDefaults(dict):

    def _get_current_url(self, root_only=False, strip_querystring=False,
                         host_only=False, **kwargs):

        current_url = get_current_url(self.environ,
            root_only, strip_querystring, host_only)

        if (root_only or host_only) and not kwargs:
            return current_url

        qs = {}
        querystring = ''

        if not strip_querystring:
            qs = urlparse.parse_qs(''.join(current_url.split('?')[1:]))
            for arg in qs:
                qs[arg] = qs[arg][0]

        if kwargs:

            for arg in kwargs:
                qs[arg] = kwargs[arg]

            querystring = '?' + urllib.urlencode(qs)

        url = '%s' % get_current_url(self.environ, strip_querystring=True)

        if url[-1] != '/':
            url += '/'

        url += querystring

        return url


    def __init__(self, request, environ):

        self.environ = environ

        config = conf('werkzeug')

        logged_in = None
        if hasattr(request, 'logged_in'):
            logged_in = request.logged_in

        user_role = None
        if hasattr(request, 'user_role'):
            user_role = request.user_role

        mount_point = config.get('mount_point', '/')
        if mount_point != '/':
            mount_point = '/%s/' % mount_point
        port = config.get('port')
        host = config.get('host') + ':%s' % port if port and port != '80' else ''
        base_url = '%s://%s%s' % (
            config.get('url_scheme'),
            host,
            mount_point
        )

        super(TemplateDefaults, self).__init__({
            'request': request,
            'current_url': self._get_current_url,
            'base_url': base_url,
            'get_flash_messages': get_flash_messages,
            'logged_in': logged_in,
            'user_role': user_role,
            #'url_for': url_for,
            'BASE': base_url,
            'STATIC': config.get('static_url'),
            'CDN': config.get('cdn_url'),
            'user_roles': request.user_roles
        })


class App(CoreApp):

    request_class = Request
    controller_loader_class = ControllerLoader
    template_defaults_class = TemplateDefaults
