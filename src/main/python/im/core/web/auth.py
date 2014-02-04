
from __future__ import absolute_import

from werkzeug.utils import redirect

from im.core.config import conf
from im.core.web.controller import Controller
from im.core.templates.mako import Template
from im.core.security.security import Security

class Auth(Controller):


    def login(self):        
        username = self.request.form.get('username')
        password = self.request.form.get('password')
        return_url = self.request.form.get('return_url') or ""
        
        login_flag = self.request.form.get('login')

        logged_in = self.request.logged_in
        
        if username and password:
            logged_in = self._process_login(username, password)

        if not logged_in:
            return self.render(self.login_template, {
                    'body_class':'login',
                    'title': 'Ingreso',
                    'subtitle': '',
                    'failed_attempt': not logged_in and password or False
                    })
        else:
            if return_url:
                return redirect(return_url)
            else:
                return redirect(self.base)


    def logout(self):
        self.request.logout()
        
        return_url = self.request.form.get('return_url') or ""
        if return_url:
            return redirect(return_url)
        else:
            return redirect(self.base)



    def _process_login(self, username, password):

        user = None
        self.security = Security(conf('werkzeug.security_manager', 'simple'))
        website_id = self.request.website_id
        if website_id is not None:
            user = self.security.authenticate(username=username,
                                              password=password,
                                              website_id=website_id)
            if user:
                self.request.login(user)
                return True
            else:
                return False
        else:
            return False
