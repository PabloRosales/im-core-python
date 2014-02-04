
from __future__ import absolute_import

from werkzeug.routing import Map, Rule

from im.core.config import conf
from im.core.database.mysql import Query


class Routing(object):

    website = None
    controller = None
    action = None

    def __init__(self, environ, request):
        self.environ = environ
        self.request = request
        self.current_url = self.request.environ.get('PATH_INFO') or '/'
        self._get_website()
        if self.website:
            self._get_controller()
            if self.controller:
                self._get_action()

    def _get_website(self):
        self.website = Query('core/web/website/by_url_and_mount_point', {
            'mount_point': conf('web.mount'),
            'url': conf('web.host'),
        }).one()

    def _get_controller(self):
        path = self.current_url.replace(self.website.mount_point, '', 1) or '/'
        if path != '/' and path.endswith('/'):
            path = path[:-1]
        self.controller = Query('core/web/controllers/by_route_url_and_website_id', {
            'path': path,
            'website_id': self.website.website_id,
        }).one()

    def _get_action(self):
        self.action = Query('core/web/action/by_id', {
            'action_id': self.controller.action_id
        }).one()

    def get_controller(self):

        if not self.website or not self.controller:
            return None, None, None, None

        url_map = Map([Rule(self.current_url)])
        urls = url_map.bind_to_environ(self.request.environ)
        endpoint, args = urls.match()

        return self.website, self.controller, self.action, args
