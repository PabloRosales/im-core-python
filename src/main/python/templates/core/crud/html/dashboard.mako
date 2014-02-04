% if menu and app:
    <%
        from im.core.config import YamlLocalConfig
        _menu = YamlLocalConfig('menus/%s' % conf('crud.dashboard_menu', app))
    %>
    <div class="dashboard">
        <div class="row">
            % for order in _menu.get('order'):
                % if order == 'home' or order == '-':
                    <% continue %>
                % endif
                % if order.startswith('-'):
                    <div class="span12">
                        <h2 style="margin:0;padding:0;font-weight:bold;">${order[1:]}</h2>
                    </div>
                % else:
                    <div>
                        ${subitems(order, _menu[order])}
                    </div>
                % endif
            % endfor
        </div>
    </div>
% endif

<%def name="subitems(key, config, heading=4)">
    <%
        if config.get('roles'):
            if user_role not in config.get('roles'):
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
        icon = 'icon-arrow-right'
        if key in icons:
            icon = icons[key]
        if config.get('icon'):
            icon = config.get('icon')

        href = '#' if config.get('disabled') else menu_url(config.get('controller'))
        _title = config.get('title')
        _help = config.get('help')

        subs = []
        if config.get('order'):
            for _order in config.get('order'):
                subs.append(capture(subitems, _order, config[_order], heading+1))
    %>
    % if subs:
        <div class="span3">
            <h${heading} style="border-bottom: 1px solid #ddd;">${_title}</h${heading}>
            % if _help:
                <p>${_help}</p>
            % endif
            % for sub in subs:
                ${sub}
            % endfor
        </div>
    % else:
        <a class="" href="${href}">
            % if icon:
                <i class="icon ${icon}"></i>
            % endif
            ${_title}
        </a>
    % endif
</%def>

