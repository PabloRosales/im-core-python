
from __future__ import absolute_import

import inspect
import json

from werkzeug.utils import redirect, import_string

from im.core.config import conf
from im.core.security import Security
from im.core.web.routes import Routing
from im.core.web.exceptions import Error400, Error401, Error403, Error404, Error500, Error501
from mako.lookup import TemplateLookup
from im.core.templates.mako import Template
from im.core.web.flash import get_flash_messages

class ControllerLoader(object):

    routing_class = Routing
    security_class = Security

    def __init__(self, environ, request):
        self.request = request
        self.environ = environ
        self.routing = self.routing_class(environ, request)
        self.security = self.security_class(conf('werkzeug.security_manager', 'simple'))

    def get(self):

        website, controller, action, values = self.routing.get_controller()

        if controller:
            self.request.website_id = website.website_id

            user = self.request.session.get('user')

            authorized = not conf('werkzeug.use_auth', False) or self.security.authorize(
                user=user,
                action=action,
                website_id=self.request.website_id,
            ) or action.key == 'auth.login' or action.key == 'auth.logout'
            
            
            if user is None and not authorized:
                return redirect('%s%s' % (website.mount_point, conf('web.login_url'))), None
            elif user is not None and not authorized:
                raise Error501()

            _controller = import_string(controller.python_module)
            if inspect.isclass(_controller):
                controller_instance = _controller(self.request)
                if hasattr(controller_instance, action.python_callable):
                    controller = getattr(controller_instance, action.python_callable)
            elif inspect.ismodule(_controller):
                if hasattr(_controller, action.python_callable):
                    controller = getattr(_controller, action.python_callable)

        return controller, values


class Controller(object):

    def __init__(self, request=None):
        if not conf('layouts'):
            raise Error400("Layouts configuration was not defined.")

        self.request = request
        self.base = conf('web.mount') or '/'
        self.master = conf('layouts.default.master')
        self.layout = conf('layouts.default.layout')
        self.format = conf('layouts.default.format')
        ext = '.' + self.format
        self.custom_helpers = conf('layouts.default.custom-helpers') + ext if not conf('layouts.default.custom-helpers').endswith(ext) else ''
        self.login_template = conf('layouts.default.login-template')
        
        self.template_config = conf('layouts.template_config')
        self.assets = Assets()
        self.languages = conf('lang')
        self.lang = None

    def get_languages(self):
        return json.dumps(self.languages);

    def t(self, key, params=(), lang='default'):
        
        
        if self.languages.get('debug'):
            default = "====='" + key + "'====="
        else:
            default = key.lower().replace("_"," ")
        
        if not self.languages:
            return default
                
        if lang == 'default':
            lang = self.lang or self.languages.get('language') or lang
        
        language = self.languages.get(lang)

        if not language:
            return default
        
        text = language.get(key) or default
        
        try:
            return text % params
        except TypeError:
            return text

    def render(self, template, template_params={}, config=None,
            _format='html', template_lookup_class=TemplateLookup):
        controller = self.__class__.__name__.lower()

        template_params["controller"] = controller
        template_params["this"] = self
        template_params["t"] = self.t
        template_params["helpers"] = Helper()
        template_params["assets"] = self.assets
        layout = {"master": self.master,
                  "layout": self.layout,
                  "format": self.format
                  }

        if not template.startswith("/"):
            template = controller + "/" + template

        return Template(template, template_params, config=self.template_config,
            _format='html', template_lookup_class=TemplateLookup, layout=layout)

class Assets(object):
    HEAD = "head"
    BODYSTART = "bodystart"
    BODYEND = "bodyend"

    def __init__(self):
        self.styles = []
        self.scripts = []
        self.cdn = conf('werkzeug.cdn_url')
        self.static = conf('werkzeug.static_url')
        self.registerAllStaticScripts()
        self.registerAllStaticStyles()

    def registerStyle(self, id, path):
        #self.styles[self.static + path] = {"id": id}
        self.styles.append({"id": id, "path": self.static + path})

    def registerScript(self, id, path, pos):
        #self.scripts[self.static + path] = {"id": id, "pos": pos}
        self.scripts.append({"id": id, "pos": pos, "path": self.static + path})

    def registerStaticScript(self, id):
        scripts = conf('layouts.scripts')
        if scripts.get(id):
            script = scripts.get(id)
            #script["id"] = id
            #self.scripts[self.cdn + script.get("path")] = script
            self.scripts.append({"id": id, "pos": "HEAD", "path": self.cdn + script.get("path")})

    def registerAllStaticScripts(self):
        for id, script in conf('layouts.scripts').iteritems():
            if script.get("autoload"):
                self.registerStaticScript(id)

    def registerAllStaticStyles(self):
        for id, style in conf('layouts.styles').iteritems():
            if style.get("autoload"):
                self.registerStaticStyle(id)

    def registerStaticStyle(self, id):
        styles = conf('layouts.styles')
        if styles.get(id):
            style = styles.get(id)
            style["id"] = id
            #self.styles[self.cdn + style.get("path")] = style
            self.styles.append({"id": id, "path": self.cdn + style.get("path"), "style": style})

    def unRegisterStaticScript(self, id):
        scripts = conf('layouts.scripts')
        if scripts.get(id):
            script = scripts.get(id)
            self.scripts[self.cdn + script.get("path")] = None

    def unRegisterStaticStyle(self, id):
        styles = conf('layouts.styles')
        if styles.get(id):
            style = styles.get(id)
            self.styles[self.cdn + style.get("path")] = None


class Helper(dict):
    def __init__(self):
        self._dict = {}

    def __getitem__(self, key):
        val = self._dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):
        self._dict.__setitem__(self, key, val)

    def add(self, id, val):
        self._dict[id] = val


class TemplateDefaults(dict):
    
    def normalize(self, url):
        if not url.endswith("/"):
            url = url + "/"
        if url.startswith("/"):
            url = url[1:]
        return url
    
    def __init__(self, request, environ):
        config = conf('werkzeug')
        super(TemplateDefaults, self).__init__({
            'request': request,
            'BASE': '%s%s' % (self.normalize(request.path_info), self.normalize(conf('web.mount'))),
            'CDN': self.normalize(config.get('cdn_url')),
            'STATIC': conf('werkzeug.static_url'),
            'MOUNT': self.normalize(request.environ.get('SCRIPT_NAME') or '/'),
            'get_flash_messages': get_flash_messages,
        })
