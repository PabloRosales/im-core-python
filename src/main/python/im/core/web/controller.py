
from __future__ import absolute_import

import inspect
import json

from werkzeug.utils import redirect, import_string

from im.core.config import conf
from im.core.web.routes import Routing
from im.core.web.exceptions import Error400, Error401, Error403, Error404, Error500, Error501
from mako.lookup import TemplateLookup
from im.core.templates.mako import Template
from im.core.web.flash import get_flash_messages

class Controller(object):

    def __init__(self, request=None):
        if not conf('layouts'):
            raise Error400("Layouts configuration was not defined.")

        self.request = request
        
        self.base = '%s%s' % (normalize(conf('web.host')), normalize(conf('web.mount')))
        
        if not conf('web.cdn_url', '/').startswith("http"):
            self.cdn = '%s%s' % (self.base, normalize(conf('web.cdn_url', '/')))
        else:
            self.cdn = normalize(conf('web.cdn_url'))
        if not conf('web.static_url', '/').startswith("http"):            
            self.static = '%s%s' % (self.base, normalize(conf('web.static_url', '/')))
        else:
            self.static = normalize(conf('web.static_url'))

        self.host = normalize(conf('web.host', 'http://127.0.0.1'))
        self.mount = normalize(conf('web.mount', '/'))        

        self.master = conf('layouts.default.master')
        self.layout = conf('layouts.default.layout')
        self.format = conf('layouts.default.format')
        ext = '.' + self.format
        self.custom_helpers = conf('layouts.default.custom-helpers') + ext if not conf('layouts.default.custom-helpers').endswith(ext) else ''
        self.login_template = conf('layouts.default.login-template')
        
        self.template_config = conf('layouts.template_config')
        self.assets = Assets(self.cdn, self.static)
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
        # controller = self.__class__.__name__.lower()
        controller = self.__module__.split('.')[-1]
        template_params["controller"] = controller
        template_params["this"] = self
        template_params["t"] = self.t
        template_params["helpers"] = Helper()
        template_params["assets"] = self.assets
        layout = {"master": self.master,
                  "layout": self.layout,
                  "format": self.format
                  }

        template_params["BASE"] = self.base
        template_params["CDN"] = self.cdn
        template_params["STATIC"] = self.static
        template_params["HOST"] = self.host
        template_params["MOUNT"] = self.mount

        template_params["get_flash_messages"] = get_flash_messages

        if not template.startswith("/"):
            template = controller + "/" + template

        return Template(template, template_params, config=self.template_config,
            _format='html', template_lookup_class=TemplateLookup, layout=layout).render()

class Assets(object):
    HEAD = "head"
    BODYSTART = "bodystart"
    BODYEND = "bodyend"

    def __init__(self, cdn="/", static="/"):
        self.styles = []
        self.scripts = []
        self.cdn = cdn
        self.static = static
        self.registerAllStaticScripts()
        self.registerAllStaticStyles()

    def registerStyle(self, id, path):
        self.styles.append({"id": id, "path": self.static + path})

    def registerScript(self, id, path, pos):
        self.scripts.append({"id": id, "pos": pos, "path": self.static + path})

    def registerStaticScript(self, id):
        scripts = conf('layouts.scripts')
        if scripts.get(id):
            script = scripts.get(id)
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

def normalize(url):
    if not url.endswith("/"):
        url = url + "/"
    if url.startswith("/"):
        url = url[1:]
    return url
