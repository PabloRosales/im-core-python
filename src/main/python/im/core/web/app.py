
from __future__ import absolute_import

import os
import json
import logging
import inspect

from werkzeug.utils import append_slash_redirect
from werkzeug.wrappers import Response, BaseResponse
from werkzeug.exceptions import HTTPException, NotFound

from im.core.web.request import Request
from im.core.utils.path import get_project_path
from im.core.config import configs, RecursiveDict
from im.core.web.controller import ControllerLoader, TemplateDefaults

logger = logging.getLogger('im.core.web.werkzeug')


class App(object):

    request_class = Request
    response_class = Response
    controller_loader_class = ControllerLoader
    template_defaults_class = TemplateDefaults

    default_configuration = RecursiveDict({
        'debug': False,
        'reloader': True,
        'evalex': True,
        'host': '127.0.0.1',
        'port': 80,
        'mount_point': '/',
        'url_scheme': 'http',
        'static_url': '/static',
        'static_path': os.path.join(get_project_path(), 'static'),
        'cdn_url': 'http://static.interactuamovil.com',
        'sessions': False,
        'sa_remove_sessions': True,
        'append_slash': False,
        'security_manager': None,
    })

    def __init__(self, config=None):
        self.config = self.default_configuration
        self.config.update_recursive(configs.get('werkzeug', {}))
        if config:
            self.config.update_recursive(config)

    def __call__(self, environ, start_response):
        self.environ = environ
        self.request = self.request_class(environ)
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):

        request_method = self.request.environ.get('REQUEST_METHOD')
        last_character_in_path = self.request.environ.get('PATH_INFO', '')[-1:]

        if self.config.get('append_slash') and last_character_in_path != '/' and request_method != 'POST':
            response = append_slash_redirect(self.request.environ)
        else:
            response = self.dispatch_request()

        self.request.end(response)

        return response(environ, start_response)

    def dispatch_request(self):

        controller, arguments = self.controller_loader_class(self.environ, self.request).get()

        if not controller:
            raise NotFound()

        if isinstance(controller, BaseResponse):
            return controller

        template_defaults = self.template_defaults_class(self.request, self.environ)

        try:

            if inspect.ismethod(controller):
                if isinstance(arguments, dict):
                    response = controller(**arguments)
                else:
                    response = controller(*arguments)
            else:
                if isinstance(arguments, dict):
                    response = controller(self.request, **arguments)
                else:
                    response = controller(self.request, *arguments)

            if isinstance(response, basestring):
                return self.response_class(response, mimetype='text/html')
            elif hasattr(response, 'render') and callable(response.render):
                return self.response_class(
                    response.render(template_defaults),
                    mimetype='text/html'
                )
            elif isinstance(response, dict) or isinstance(response, list):
                response = json.dumps(response)
                return self.response_class(response, mimetype='application/json')
            else:
                return response

        #~ except _ProxyException, e:
            #~ response = e.get_response(self.environ)
            #~ template = response.response
            #~ if hasattr(template, 'render') and callable(template.render):
                #~ return self.response_class(
                    #~ template.render(template_defaults),
                    #~ mimetype=response.mimetype
                #~ )
            #~ return response

        except HTTPException, e:

            return e
