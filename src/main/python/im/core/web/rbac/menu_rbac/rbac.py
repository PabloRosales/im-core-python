from im.core.config import YamlLocalConfig

def has_access(request, conf):
    path = request.environ.get('PATH_INFO')
    controller = '.'.join(filter(None, path.split('/')))
    roles = request.user_roles
    if controller == 'home' \
        or controller == '' \
        or path == conf('werkzeug.login_url') \
        or path == conf('werkzeug.logout_url'):
        return True
    else:
        found_something = False

        for menu in conf('menu').get('menu'):
            menu_conf = YamlLocalConfig('menus/%s' % menu)
            if menu_conf and submenu(controller, roles, menu_conf, found_something):
                return True # si tenia permiso en la config
                
        if not found_something: # el controlador no esta en ningun menu
            found_something = False
            return True 
            
    return False

def submenu(controller, user_roles, config, found_something):
    if config.get('controller') and controller == config.get('controller'):
        found_something = True
        if config.get('roles'):
            return any (a in user_roles for a in config.get('roles'))
        else:
            return True # permite acceso si el controllador no tiene roles configurados

    if config.get('roles'):
        if not any (a in user_roles for a in config.get('roles')):
            return False
    
    items = []
    if config.get('order'):
        for order in config.get('order'):
            if not "-" in order:
                items.append(submenu(controller, user_roles, config[order], found_something))
    else:
        for _key, value in config.iteritems():
            if _key not in ('title', 'controller', 'roles', 'disabled', 'icon', 'help'):
                items.append(submenu(controller, user_roles, value, found_something))
    return any(items)
