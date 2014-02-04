<%def name="form(columns, item=None, crud_type='update')">
    <%
        from im.core.web.werkzeug import get_column_data
        from im.core.web.bootstrap import icons
        tabindex = 0
    %>
    % for column in columns:
        <%

            tabindex += 1
            type = repr(column.type).lower()

            if crud_type == 'add' and column.primary_key:
                if 'integer' in type:
                    continue

            link, relation_column, value, value_verbose = None, None, '', ''
            if item:
                value = getattr(item, str(column.key))
                if value is None:
                    value = ''
            elif column.default:
                if hasattr(column.default.arg, 'compile'):
                    value = column.default.arg.compile(bind=session.bind).execute().fetchone()
                    if isinstance(value, list):
                        value = value[0]
                    else:
                        value = ''
                else:
                    value = column.default.arg

            relation_column = None
            column_name = column.name
            relation_column_name = None

            if column.foreign_keys:
                relation_column_name = list(column.foreign_keys)[0].target_fullname.split('.')[1].replace('_id', '')
                relation = column_name.replace('_id', '')
                url = base_url if not base_url.endswith('/') else base_url.rstrip('/')
                if crud_type == 'update':
                    link = '../../../%s/list' % relation_column_name
                else:
                    link = '../../%s/list' % relation_column_name
                if hasattr(item, relation):
                    relation_column = getattr(item, relation)
                else:
                    try:
                        if crud_type == 'add' and column_name in relations:
                            relation_column = relations[column_name]
                    except NameError:
                        pass

            if relation_column:
                if hasattr(relation_column, str(column_name)):
                    value = getattr(relation_column, str(column_name))
                else:
                    try:
                        relation_columns = relation_column.__table__.columns
                    except AttributeError:
                        value = relation_column
                    else:
                        for col in relation_columns:
                            if col.primary_key:
                                value = getattr(relation_column, str(col.name))
                value_verbose = relation_column

            column_icon = column.__icon__
            if not column_icon or column_icon == str(column.type).split('(')[0]:
                    column_icon = 'icon-pencil'

        %>

        % if model.__columns_renderers_on_update__ and column.name in model.__columns_renderers_on_update__:
            ${model.__columns_renderers_on_update__[column.name][0](column.name, model.__columns_renderers_on_update__[column.name][1], column, item)}
	    % elif column.foreign_keys:
            <div class="control-group">
                <label class="control-label" for="${column_name}-verbose">${column.info['verbose_name']}</label>
                <div class="controls">
                    <div class="input-append">
                        <input class="span2" size="16" id="${column_name}-verbose" type="text" value="${value_verbose}" disabled />
                        <input id="${column_name}" name="${column_name}" type="hidden" value="${value}" />
                        <a class="btn foreign" data-target="${link}?foreign_selection=1&id=${column_name}" data-title="${relation_column if relation_column else ''}" href="#" tabindex="${tabindex}">Buscar</a>
                    </div>
                    % if column.help:
                        <p class="help-block">${column.help}</p>
                    % endif
                </div>
            </div>
        % elif 'integer' in type :
            <div class="control-group">
                <label class="control-label" for="${column_name}-verbose">${column.info['verbose_name']}</label>
                <div class="controls">
                    <div class="input-prepend">
                        <span class="add-on"><i class="${column_icon}"></i></span>
                        <input id="${column_name}" name="${column_name}" type="text" value="${value}" tabindex="${tabindex}" ${'disabled' if column.primary_key else ''} ${'disabled' if column.read_only else ''}/>
                    </div>
                    % if column.help:
                        <p class="help-block">${column.help}</p>
                    % endif
                </div>
            </div>
        % elif 'string' in type or 'varchar' in type or 'date' in type or 'timestamp' in type:
            <% max_length = column.type.length if hasattr(column.type, 'length') else False %>
            % if max_length and max_length > 100:
                <div class="control-group">
                    <label class="control-label" for="${column_name}">${column.info['verbose_name']}</label>
                    <div class="controls">
                        <span class="counter" id="counter-${column_name}">${max_length if not value else (max_length - len(value.replace('\r\n', '\n')))}&dArr;</span>
                        <textarea ${'data-max="%s"' % max_length} class="count" rows="5" class="input-xxlarge" id="${column_name}" name="${column_name}" tabindex="${tabindex}" ${'disabled' if column.read_only else ''}>${value}</textarea>
                        % if column.help:
                            <p class="help-block">${column.help}</p>
                        % endif
                    </div>
                </div>
            % else:
                <div class="control-group">
                    <label class="control-label" for="${column_name}">${column.info['verbose_name']}</label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="${column_icon}"></i></span>
                            <%
                                def get_date_type(t):
                                    if 'datetime' in t or 'timestamp' in t:
                                        return 'datetime'
                                    elif 'date' in t:
                                        return 'date'
                                    return ''
                            %>
                            <input class="${get_date_type(type)}" id="${column_name}" name="${column_name}" type="text" value="${value}" tabindex="${tabindex}" ${'maxlength="%s"' % max_length if max_length else ''} ${'disabled' if column.primary_key or column.read_only else ''} />
                            % if 'datetime' in type or 'timestamp' in type:
                                <a class="btn datetime-now" href="#" data-content="${column_name}">Ahora</a>
                            % elif 'date' in type:
                                <a class="btn date-today" href="#" data-content="${column_name}">Hoy</a>
                            % endif
                        </div>
                        % if column.help:
                            <p class="help-block">${column.help}</p>
                        % endif
                    </div>
                </div>
            % endif
        % elif 'bool' in type:
            <div class="control-group">
                <label class="control-label" for="${column_name}">${column.info['verbose_name']}</label>
                <div class="controls">
                    <label class="radio">
                        <input id="${column_name}_true" name="${column_name}" type="radio" value="1" tabindex="${tabindex}" ${'checked' if value else ''}/>
                        Si
                    </label>
                    <label class="radio">
                        <input id="${column_name}_false" name="${column_name}" type="radio" value="0" ${'checked' if value is False else ''}/>
                        No
                    </label>
                    % if column.help:
                        <p class="help-block">${column.help}</p>
                    % endif
                </div>
            </div>
        % elif 'text' in type:
            <div class="control-group">
                <label class="control-label" for="${column_name}">${column.info['verbose_name']}</label>
                <div class="controls">
                    <% max_length = column.max_length if hasattr(column, 'max_length') else False %>
                    <textarea ${'data-max="%s"' % max_length if max_length else ''} class="${'count' if max_length else ''}" rows="5" class="input-xxlarge" id="${column_name}" name="${column_name}" tabindex="${tabindex}">${value}</textarea>
                    % if max_length:
                        <span class="counter" id="counter-${column_name}">${max_length if not value else (max_length - len(value.replace('\r\n', '\n')))}&dArr;</span>
                    % endif
                    % if column.help:
                        <p class="help-block">${column.help}</p>
                    % endif
                </div>
            </div>
        % elif 'enum' in type:
            <div class="control-group">
                <label class="control-label" for="${column_name}">${column.info['verbose_name']}</label>
                <div class="controls">
                    <select id="${column_name}" name="${column_name}" tabindex="${tabindex}">
                        % if column.nullable:
                            <option value="">Ninguno</option>
                        % endif
                        % for val in column.type.enums:
                            <option value="${val}" ${'selected' if val == value else ''}>${val}</option>
                        % endfor
                    </select>
                    % if column.help:
                        <p class="help-block">${column.help}</p>
                    % endif
                </div>
            </div>
        % else:
            <div class="control-group">
                <label class="control-label" for="${column_name}">${column.info['verbose_name']}</label>
                <div class="controls">
                    <div class="input-prepend">
                        <span class="add-on"><i class="${column_icon}"></i></span>
                        <input id="${column_name}" name="${column_name}" type="text" value="${value}" tabindex="${tabindex}" ${'disabled' if column.read_only else ''}/>
                    </div>
                    % if column.help:
                        <p class="help-block">${column.help}</p>
                    % endif
                </div>
            </div>
        % endif
    % endfor
</%def>
