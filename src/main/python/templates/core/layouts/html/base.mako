<%inherit file="${context.get('__inherit__')}.mako" />
% if __sections__:
    % for section in __sections__:
        ${recursive_render(section)}
    % endfor
% endif

% if __layout__ and 'stylesheets' in __layout__:
    % for css in __layout__['stylesheets']:
        <link rel="stylesheet" type="text/css" href="${STATIC}/css/${css}.css" />
    % endfor
% endif

<%def name="recursive_render(section, item=None)">

    % if isinstance(section, list):

        % for _item in section:
            ${recursive_render(_item)}
        % endfor

    % elif isinstance(section, dict):

            % if 'template' in section:

                <% template = section['template'] % {'format': __format__} %>
                <%include file="${template}.mako" />

            % elif 'type' in section:

                <%
                    _type = section['type']
                    _id = section['id'] if 'id' in section else None
                %>

                % if _type == 'template':

                    <% template = section['file'] % {'format': __format__} %>
                    <%include file="${template}.mako" />

                % elif _type == 'row':

                    <div class="row">
                        % if 'sections' in section:
                            ${recursive_render(section['sections'])}
                        % endif
                    </div>

                % elif _type == 'span':

                    <div class="span${section['size']}">
                        % if 'sections' in section:
                            ${recursive_render(section['sections'])}
                        % endif
                    </div>

                % elif _type == 'html':

                    <%
                        if 'data' in section:
                            if context.get(section['data']) is not None:
                                data = context.get(section['data'])
                            else:
                                data = section['data']
                            html = section['html'] % data
                        else:
                            html = section['html']

                    %>

                    ${html}

                % elif _type == 'toolbar':

                    <div class="btn-toolbar">
                        % if 'sections' in section:
                            ${recursive_render(section['sections'])}
                        % endif
                    </div>

                % elif _type == 'button-group':

                    <div class="btn-group">
                        % if 'sections' in section:
                            ${recursive_render(section['sections'])}
                        % endif
                    </div>

                % elif _type == 'button':

                    ${button(section)}

                % elif _type == 'search':

                    <%
                        align = section.get('align', 'right')
                        method = section.get('method', 'get')
                        search_term = context.get(section.get('name', 'search_term'), False)

                        url = ''
                        if 'url' in section:
                            url = section['url']
                            if url.startswith('current+'):
                                _params = {}
                                for _param in url.replace('current+', '').split(','):
                                    if _param and '=' in _param:
                                        p = _param.split('=')
                                        _params[p[0]] = p[1]
                                url = current_url(**_params)
                    %>

                    <form style="float:${align};" class="form-search" method="${method}" action="${current_url()}">
                        <input type="text" class="input-medium search-query" name="search" value="${search_term if search_term else ''}" />
                        <button type="submit" class="btn">Buscar</button>
                    </form>

                % elif _type == 'form':

                    <form class="${section['class'] if 'class' in section else ''}" method="${section['method'] if 'method' in section else 'post'}" action="${section['action'] if 'action' in section else current_url()}" enctype="multipart/form-data">
                        % if 'sections' in section:
                            ${recursive_render(section['sections'])}
                        % endif
                    </form>

                % elif _type == 'form-input-hidden':

                    <input type="hidden" name="${section['name']}" id="${section['name']}" />

                % elif _type == 'form-input':

                    <div class="control-group">
                        % if 'label' in section:
                            <label class="control-label" for="${section['name']}">${section['label']}</label>
                        % endif
                        <div class="controls">
                            <input
                                class="${section['class'] if 'class' in section else ''} ${'disable' if 'readonly' in section and section['readonly'] else ''}"
                                type="${section['input-type'] if 'input-type' in section else 'text'}"
                                id="${section['name']}"
                                name="${section['name']}"
                                placeholder="${section['placeholder'] if 'placeholder' in section else ''}"
                                value="${context.get(section['name']) if context.get(section['name']) is not None else section['value'] if 'value' in section else ''}"
                                ${'readonly' if 'readonly' in section and section['readonly'] else ''}>
                            % if 'sections' in section:
                                ${recursive_render(section['sections'])}
                            % endif
                            % if 'help' in section:
                                <p class="help-block">${section['help']}</p>
                            % endif
                        </div>
                    </div>

                % elif _type == 'form-input-radio':

                    <div class="control-group">
                        <label class="control-label" for="${section['name']}">${section['label']}</label>
                        <div class="controls">
                            % for _item in section['data']:
                                <label class="radio">
                                    <input id="${section['name']}" name="${section['name']}" type="radio" value="${_item[0]}" ${'checked' if _item[2] else ''} />
                                    ${_item[1]}
                                </label>
                            % endfor
                        </div>
                    </div>

                % elif _type == 'form-select':

                    <%
                        data = None
                        if 'data' in section:
                            data = context.get(section['data'])

                    %>
                    <div class="control-group">
                        % if 'label' in section:
                            <label class="control-label" for="${section['name']}">${section['label']}</label>
                        % endif
                        <div class="controls">
                            <select
                                    class="${section['class'] if 'class' in section else ''}"
                                    id="${section['id'] if 'id' in section else section['name']}"
                                    name="${section['name']}">
                                % if 'nullable' in section and section['nullable']:
                                    <option value="">Ninguno</option>
                                % endif
                                % if isinstance(data, dict):
                                    % for key, _item in data.iteritems():
                                        <option value="${_item.get(section['value'])}">${_item.get(section['description'])}</option>
                                    % endfor
                                % else:
                                    % if data:
                                        % for _item in data:
                                            <option value="${getattr(_item, section['value'])}"
                                                <%
                                                    if context.get(section['name'], False) and context.get(section['name']) == getattr(_item, section['value']):
                                                        selected = 'selected="selected"'
                                                    elif 'default' in section and getattr(_item, section['value']) == section['default']:
                                                        selected = 'selected="selected"'
                                                    else:
                                                        selected = ''
                                                %>
                                                ${selected}
                                                >
                                                ${getattr(_item, section['description'])}
                                            </option>
                                        % endfor
                                    % endif
                                % endif
                            </select>
                            % if 'help' in section:
                                <p class="help-block">${section['help']}</p>
                            % endif
                        </div>
                    </div>

                % elif _type == 'form-textarea':

                    <div class="control-group">
                        % if 'label' in section:
                            <label class="control-label" for="${section['name']}">${section['label']}</label>
                        % endif
                        <div class="controls">
                            % if 'counter' in section:
                                <span class="counter" id="counter-${section['name']}">${section['counter']['max-length']}&dArr;</span>
                            % endif
                            <textarea ${'data-max="%s"' % section['counter']['max-length'] if 'counter' in section else ''} class="${'count' if 'counter' in section else ''}" id="${section['name']}" name="${section['name']}" rows="${section['rows'] if 'rows' in section else ''}" cols="${section['cols'] if 'cols' in section else ''}">${context.get(section['value']) if context.get(section['value']) is not None else section['value'] if 'value' in section else ''}</textarea>
                            % if 'sections' in section:
                                ${recursive_render(section['sections'])}
                            % endif
                            % if 'help' in section:
                                <p class="help-block">${section['help']}</p>
                            % endif
                        </div>
                    </div>

                % elif _type == 'form-actions':

                    <div class="form-actions form-actions-no-background">
                        % if 'sections' in section:
                            ${recursive_render(section['sections'])}
                        % endif
                    </div>

                % elif _type == 'form-submit':

                    <input class="${'btn btn-primary' if not 'class' in section else section['class']}" type="submit" name="${section['name'] if 'name' in section else 'submit'}" value="${section['value'] if 'value' in section else 'OK'}" />

                % elif _type == 'table':

                    <%
                        data = None
                        if 'data' in section:
                            data = context.get(section['data'])
                    %>

                    <table class="table ${section['class'] if 'class' in section else ''}">
                        % if data:
                            % for _item in data:
                                % if 'sections' in section:
                                    ${recursive_render(section['sections'], _item)}
                                % endif
                            % endfor
                        % else:
                            % if 'sections' in section:
                                ${recursive_render(section['sections'], item)}
                            % endif
                        % endif
                    </table>

                % elif _type == 'table-header':

                    % if 'sections' in section:
                        <thead style="${section['style'] if 'style' in section else ''}">
                            <tr>
                                % for _section in section['sections']:
                                    <th style="text-align:${section['align'] if 'align' in section else 'left'};">${_section}</th>
                                % endfor
                            </tr>
                        </thead>
                    % endif

                % elif _type == 'table-data':

                    <%
                        data = None
                        if 'data' in section:
                            data = context.get(section['data'])
                        elif item:
                            data = item
                    %>

                    <tbody>
                        % if data:
                            % for _item in data:
                                <tr style="${section['style'] if 'style' in section else ''}">
                                    % for _section in section['sections']:
                                        <%
                                            if isinstance(_section['data'], list):
                                                _data = _section['data']
                                            else:
                                                _data = getattr(_item, _section['data'])

                                            if _data is None:
                                                _data = '-'

                                            if 'html' in _section:
                                                try:
                                                    _data = _section['html'] % _data
                                                except TypeError:
                                                    _data = _section['html']
                                        %>
                                        <td>${_data}</td>
                                    % endfor
                                </tr>
                            % endfor
                        % else:
                            <tr>
                                <td>No hay datos.</td>
                            </tr>
                        % endif
                    </tbody>

                % elif _type == 'javascript':

                    <script type='text/javascript' src="${STATIC}/js/${section['file']}.js"></script>

                % elif 'sections' in section:

                    ${recursive_render(section['sections'])}

                % endif

            % endif

    % else:

        ${section}

    % endif

</%def>

<%def name="button(config)">

    <%

        url = '#'
        if 'url' in config:
            url = config['url']
            if url.startswith('current'):
                _params = {}
                for _param in url.replace('current+', '').replace('current', '').split(','):
                    if _param and '=' in _param:
                        p = _param.split('=')
                        _params[p[0]] = p[1]
                url = current_url(**_params)

        _class = config.get('class', '')
        _id = config.get('id', '')
        label = config.get('text', '')

        icon = ''
        if 'icon' in config:
            icon =  '<i class="%s"></i>' % config['icon']

        if 'inverse' in config:
            inverse = config['inverse']
            if '==' in inverse:
                d = inverse.split('==')
                if d[0] in dict(context) and context.get(d[0]) == str(d[1]):
                    _class += ' btn-inverse'
            elif '!=' in inverse:
                d = inverse.split('!=')
                if d[0] in dict(context) and context.get(d[0]) != str(d[1]):
                    _class += ' btn-inverse'

    %>

    <a ${config['extra'] if 'extra' in config else ''} id="${_id}" class="btn ${_class}" href="${url}"
       % if 'popover' in config:
           rel="popover"
           data-title="${config['popover']['title']}"
           data-content="${config['popover']['text']}"
       % endif
    >
        ${icon}
        ${label}
    </a>

</%def>

% if __layout__ and 'javascripts' in __layout__:
    % for js in __layout__['javascripts']:
        <script type='text/javascript' src="${STATIC}/js/${js}.js"></script>
    % endfor
% endif
