
from __future__ import absolute_import

import json

from werkzeug.wrappers import BaseRequest
from werkzeug.utils import cached_property

from im.core.config import conf
from im.core.web.sessions import DatabaseSessionStore
from im.core.database.mysql import sessions as sa_sessions

session_store = DatabaseSessionStore()


class Request(BaseRequest):

    session = None
    website_id = None

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
        session_store.close(self.session)
        if self.session.has_key('user'):
            self.session.pop('user') 

    def login(self, user):
        session_store.save(self.session)
        self.session['user'] = user

    @property
    def logged_in(self):
        return self.session.has_key('user') or False

    #~ def logout(self):
        #~ self.session.pop('user_id', None)
        #~ self.session.pop('account_id', None)

    #~ def login(self, account_id, user_id):
        #~ self.session['account_id'] = account_id
        #~ self.session['user_id'] = user_id

    #~ @property
    #~ def logged_in(self):
        #~ return self.user_id or False

    #~ @property
    #~ def user_id(self):
        #~ return self.session.get('user_id')

    #~ @property
    #~ def account_id(self):
        #~ return self.session.get('account_id')

    @cached_property
    def json(self):
        if self.headers.get('content-type') == 'application/json':
            return json.loads(self.data)
