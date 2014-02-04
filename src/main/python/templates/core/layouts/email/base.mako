<%
    import locale
    locale.setlocale(locale.LC_ALL, conf('locale.locale'))
    _saved_values = {}
%>
<%inherit file="${context.get('__inherit__')}.mako" />

% if __sections__:
    % for section in __sections__:
        ${recursive_render(section)}
    % endfor
% endif

<%def name="recursive_render(section, item=None, override=None)">

    % if isinstance(section, list):

        % for _item in section:
            ${recursive_render(_item, item)}
        % endfor

    % else:

        % if isinstance(section, dict):

            % if 'template' in section:

                <% template = section['template'] % {'format': __format__} %>
                <%include file="${template}.mako" />

            % elif 'type' in section:

                <%
                    _type = section['type']
                    _id = section['id'] if 'id' in section else None
                %>

                % if _type == 'table':

                    <%
                        data = None
                        if 'data' in section:
                            data = context.get(section['data'])
                    %>

                    % if data:
                        <tr>
                            <td>
                                <table border="0" cellpadding="0" cellspacing="0" style="border:1px solid #ccc;background:white;width:100%;">
                                    % for _item in data:
                                        % if 'sections' in section:
                                            ${recursive_render(section['sections'], _item)}
                                        % endif
                                    % endfor
                                </table>
                            </td>
                        </tr>
                    % else:
                        <tr>
                            <td>
                                <table border="0" cellpadding="0" cellspacing="0" style="border:1px solid #ccc;background:white;width:100%;">
                                    % if 'sections' in section:
                                        ${recursive_render(section['sections'], item)}
                                    % endif
                                </table>
                            </td>
                        </tr>
                    % endif

                % elif _type == 'table-header':

                    % if 'sections' in section:
                        <thead>
                            <tr style="background:${'#3C657D' if not 'background' in section else section['background']};">
                                % for _section in section['sections']:
                                    <th style="border-bottom:1px solid #ccc;font-size:14px;color:white;font-weight:normal;padding:4px;text-align:${section['align'] if 'align' in section else 'left'};">${_section}</th>
                                % endfor
                            </tr>
                        </thead>
                    % endif

                % elif _type == 'table-data':

                    <%

                        if isinstance(override, dict):
                            section.update(override)

                        data = None
                        if 'data' in section:
                            data = context.get(section['data'])
                        elif item:
                            data = item

                    %>
                    % if data and 'sections' in section:
                        <tbody>
                            % for _item in data:
                                <tr style="background:${'#ffffff' if not 'background' in section else section['background']};">
                                    % for _section in section['sections']:
                                        <%
                                            _error = False

                                            if isinstance(_section['data'], list):
                                                _data = _section['data']
                                            else:
                                                _data = getattr(_item, _section['data'])

                                            if 'check' in _section:
                                                if _section['check'] == 'ascii':
                                                    try:
                                                        _data.decode('ascii')
                                                    except UnicodeDecodeError:
                                                        _error = True

                                            if _data is None:
                                                _data = '-'
                                            else:
                                                if 'calculate' in _section:
                                                    if _section['calculate'] == 'percentage':
                                                        first_value = getattr(_item, _data[0])
                                                        if isinstance(first_value, basestring) and ',' in first_value:
                                                            first_value = first_value.replace(',', '')
                                                        second_value = getattr(_item, _data[1])
                                                        if isinstance(second_value, basestring) and ',' in second_value:
                                                            second_value = second_value.replace(',', '')
                                                        if int(second_value) <= 0:
                                                            second_value = 1
                                                        _data = (float(first_value) / float(second_value)) * 100
                                                        _data = locale.format('%.2f', _data, grouping=True) + '%'

                                            _style = ''
                                            if 'style' in _section:
                                                _style = _section['style']
                                        %>
                                        <td style="border-bottom:1px solid #ccc;padding:3px;${_style};font-size:13px;color:${'#f00' if _error else '#000'};">${_data}</td>
                                    % endfor
                                </tr>
                            % endfor
                        </tbody>
                    % endif

                % elif _type == 'table-group-by':

                    <%
                        _items = context.get(section['data'])
                        _subitems = {}
                        latest_group_item = None
                        for _item in _items:
                            group_column = getattr(_item, section['column'])
                            if group_column != latest_group_item:
                                _subitems[group_column] = [_item]
                                latest_group_item = group_column
                            else:
                                _subitems[group_column].append(_item)
                    %>
                    % for _key, _value in _subitems.iteritems():
                        <%
                            _name = '%s_%s' % (section['column'], _key)
                            _sections = section['sections']
                            override = {'data': _name}
                        %>
                        ${recursive_render(_sections, _value, override)}
                    % endfor

                % elif _type == 'header':

                    <%
                        style = ''
                        if 'style' in section:
                            style = section['style']
                            if context.get(style, False):
                                style = context.get(style)
                                if callable(style):
                                    style = style(item)
                    %>

                    % if 'sections' in section:
                        <tr style="background:${'#3C657D' if not 'background' in section else section['background']};${style if style else ''}">
                            % for _section in section['sections']:

                                ${recursive_render(_section, item)}
                            % endfor
                        </tr>
                    % endif

                % elif _type == 'row':

                    <tr style="padding:5px;">
                        % if 'sections' in section:
                            ${recursive_render(section['sections'], item)}
                        % endif
                    </tr>

                % elif _type == 'title' or _type == 'subtitle':

                    <%
                        title = getattr(item, section['data'])
                    %>
                    <td colspan="${section['colspan'] if 'colspan' in section else '1'}" style="border-bottom:1px solid #ccc;font-size:14px;color:white;font-weight:normal;padding:10px 10px 8px 10px;text-align:${section['align'] if 'align' in section else 'left'};">
                        <strong>${title}</strong>
                    </td>

                % elif _type == 'label':

                    <td colspan="${section['colspan'] if 'colspan' in section else 1}" valign="bottom" style="font-size: 14px;font-weight:bold;border-bottom:1px solid #ccc;width:200px;padding:4px 0 4px 4px;color:#3C657D;text-align:${section['align'] if 'align' in section else 'left'}">
                        ${section['text']}
                    </td>

                % elif _type == 'info':

                    <%
                        content = '?'
                        if item and 'data' in section:
                            content = getattr(item, section['data'])
                            if content is None:
                                content = '-'
                                if 'default' in section:
                                    content = section['default']
                            else:
                                if item and 'text' in section:
                                    content = section['text'] % content
                    %>
                    <td style="padding:4px 0 4px 4px;font-size: 13px;border-bottom:1px solid #ccc;padding:4px 0px;">
                        <p style="text-align:center;margin:0 0 3px 0;">
                            <strong>${section['title']}</strong>
                        </p>
                        <p style="text-align:center;margin:0;">
                            <span style="text-align:center;">${content}</span>
                        </p>
                    </td>

                % elif _type == 'data':

                    <%
                        content = '?'
                        if item and 'data' in section:
                            content = getattr(item, section['data'])

                        if content is None:
                            content = '-'
                            if 'default' in section:
                                content = section['default']
                        else:
                            if item and 'text' in section:
                                content = section['text'] % content

                    %>
                    <td colspan="${section['colspan'] if 'colspan' in section else 1}" style="font-size: 13px;border-bottom:1px solid #ccc;padding:4px 0px;">
                        <p style="text-align:center;margin:0;">${content}</p>
                    </td>

                % elif _type == 'sum':

                    <%
                        total = 0

                        if item:
                            data = item
                        elif 'data' in section:
                            data = context.get(section['data'])

                        if 'column' in section:
                            column = section['column']
                            for _item in data:
                                _item_data = getattr(_item, column)
                                if isinstance(_item_data, basestring) and ',' in _item_data:
                                   _item_data = _item_data.replace(',', '')
                                total += int(_item_data)

                        if 'save' in section:
                            _saved_values[section['save']] = total
                %>
                    <td style="border-bottom:1px solid #ccc;">${locale.format('%d', total, grouping=True)}</td>

                % elif _type == 'percentage':

                    <%
                        _data = section['data']
                        first_value = _saved_values[_data[0]]
                        second_value = _saved_values[_data[1]]
                        if not second_value:
                            second_value = 1
                        total = (float(first_value) / float(second_value)) * 100
                    %>
                    <td style="border-bottom:1px solid #ccc;">${locale.format('%.2f', total, grouping=True)}%</td>

                % elif _type == 'empty':

                    <td colspan="${section['colspan'] if 'colspan' in section else '1'}" style="border-bottom:${'1' if ('border' in section and section['border']) else '0'}px solid #ccc;">&nbsp;</td>

                % endif

            % elif 'sections' in section:

                ${recursive_render(section['sections'])}

            % endif

        % else:

            ${section}

        % endif

    % endif

</%def>