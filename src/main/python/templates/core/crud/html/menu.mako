% if menu:
	<%
        from im.core.config import YamlLocalConfig
        menu_items = menu.get('menu')
        _menu = {'order': menu_items}
        for item in menu_items:
            _menu[item] = YamlLocalConfig('menus/%s' % item)
    %>
	<%def name="submenu(key, config, items_count)">
        <%
            if config.get('roles') and user_roles is not None:
                if not any (a in user_roles for a in config.get('roles')):
                    if current_url(strip_querystring=True) == menu_url(config.get('controller')):
                        from im.core.web.werkzeug import abort
                        abort(404)
                    return ''
            icons = {
                'add': 'icon-plus-sign',
                'list': 'icon-th-list',
                'all': 'icon-th-list',
                'home': 'icon-th-large',
                'messages': 'icon-comment',
                'reports': 'icon-signal',
                'users': 'icon-user',
            }
            subs = []
            if config.get('order'):
                for order in config.get('order'):
                    if order == '-' :
                        subs.append("divider")
                    elif not order.find("-"):
                        subs.append(order)
                    else:
                        subs.append(capture(submenu, order, config[order], items_count + 1))
                        if order == 'home':
                            subs.append("divider")
            else:
                for _key, value in config.iteritems():
                    if _key not in ('title', 'controller', 'roles', 'disabled', 'icon', 'help'):
                        subs.append(capture(submenu, _key, value, items_count + 1))

            icon = 'icon-arrow-right'
            href = '#' if config.get('disabled') else menu_url(config.get('controller'))
            class_ = 'disabled' if config.get('disabled') else ''
            class_ += ' dropdown-toggle' if subs else ''
            other_props = "data-toggle='dropdown'" if subs else ''

            if key in icons:
                icon = icons[key]

            if config.get('icon'):
                icon = config.get('icon')

        %>
        % if subs and items_count == 0:
            <li class="dropdown">
        % elif subs and items_count > 0:
            <li class="dropdown-submenu">
        % else :
            <li>
        % endif
            <a class="${class_}" href="${href}" ${other_props}>
                % if icon and items_count > 0:
                    <i class="icon ${icon}"></i>
                % endif
                ${config.get('title')}
                % if subs:
                    <b class="caret"></b>
                % endif
            </a>
            % if subs:
                <ul class="dropdown-menu">
                    % for sub in subs:
                        % if sub == "divider" :
                            <li class="divider"></li>
                        % elif sub.find("-") == 0 :
                            <li class="nav-header">${sub[1:]}</li>
                        % else :
                            ${sub}
                        % endif
                    % endfor
                </ul>
            % endif
        </li>
    </%def>
    <div class="navbar navbar-fixed-top">
        <div class="navbar-inner">
            <div class="container">
                <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </a>
                <a class="brand" href="${menu.get('root_url')}">${menu.get('brand')}</a>
                <div class="nav-collapse collapse">
                    <ul class="nav">
                        % if logged_in:
                            % if _menu.get('order'):
                                % for order in _menu.get('order'):
                                    ${submenu(order, _menu[order], 0)}
                                % endfor
                            % else:
                                % for key, menu_item in _menu.iteritems():
                                    ${submenu(key, menu_item, 0)}
                                % endfor
                            % endif
                            % if conf('werkzeug.use_auth'):
                                <li><a href="${conf('werkzeug.logout_url')}">Salir</a></li>
                            % endif
                        % endif
                    </ul>
                </div>
            </div>
        </div>
    </div>
% endif
