
from __future__ import absolute_import

import logging

from im.core.security.simple.user import User
from im.core.database.mysql import Query
from werkzeug.contrib.sessions import SessionStore, Session

logger = logging.getLogger('im.core.web.session')


class DatabaseSessionStore(SessionStore):

    def save(self, session):
        if 'user' in session and hasattr(session['user'], 'serialize'):
            return Query('core/web/sessions/save', {
                'session_id': session.sid,
                'data': session['user'].serialize(),
                'expires_on': None,
                'user_id': session['user'].user_id
            }).execute()
        logger.error('Error serializing user in session, maybe empty user or no serialization method implemented')
        return False

    def delete(self, session):
        return Query('core/web/sessions/delete', {
            'session_id': session.sid
        }).execute()

    def close(self, session):
        return Query('core/web/sessions/close', {
            'session_id': session.sid
        }).execute()

    def get(self, sid):
        data = {}
        user = Query('core/web/sessions/get', {
            'session_id': sid
        }).one()
        if user:
            data['user'] = User.unserialize(user.data)
        return Session(data, sid=sid)
