<%
    # TODO add url query args for filter
    from im.core.web.werkzeug import get_column_data, get_item_primary_key
    dir_path = '../'
%>

<div class="btn-toolbar">
    % if not read_only:
        <div class="btn-group">
            <a class="btn" href="../add"><i class="icon-plus"></i> Nuevo</a>
        </div>
    % endif
    <div class="btn-group">
        <a class="btn" href="${current_url()}"><i class="icon-refresh"></i> Refrescar</a>
        % if not filtered:
            % if not 'list' in current_url() and not id:
                <a class="btn btn-primary" href="${dir_path}"><i class=""></i> Quitar filtros</a>
            % endif
            <a class="btn ${'btn-inverse' if per_page == '10' else ''}" href="${current_url(per_page=10)}"><i class="icon-list"></i> 10</a>
            <a class="btn ${'btn-inverse' if per_page == '30' else ''}" href="${current_url(per_page=30)}"><i class="icon-list"></i> 30</a>
            <a class="btn ${'btn-inverse' if per_page == '60' else ''}" href="${current_url(per_page=60)}"><i class="icon-list"></i> 60</a>
            <a class="btn ${'btn-inverse' if per_page == 'all' else ''}" href="${current_url(per_page='all')}" rel="popover" data-content="!Esto puede ser lento si hay demasiados datos que cargar!" data-original-title="Cuidado!"><i class="icon-exclamation-sign"></i> Todos</a>
        % endif
    </div>
    % if toolbar and not filtered:
        <%include file="${toolbar + '.mako'}" />
    % endif
    % if hasattr(model, 'search'):
        <form style="float: right;" class="form-search" method="post" action="${current_url()}">
            <input type="text" class="input-medium search-query" name="search" value="${search_term if search_term else ''}" />
            <button type="submit" class="btn">Buscar</button>
        </form>
    % endif
</div>

% if items:
    <table class=" table table-bordered table-striped">
        <thead>
            <tr>
                % for column in columns:
                    <%
                        if not hasattr(items[0], str(column.name)):
                            continue

                        if column.name in items[0].__columns_exclude_on_list__:
                            continue

                        column_type = str(column.type).lower()
                        if '(' in column_type:
                            column_type = column_type.split('(')[0]

                    %>
                    <th class="${column_type} ${column.name}" ${'width="200px"' if 'message' in column.name else ''}>
                        % if column.__icon__:
                            <i class="${column.__icon__}"></i>
                        % endif
                        ${column.info['verbose_name']}
                    </th>
                % endfor
                % if items[0].__columns_extra_on_list__:
                    % for column in items[0].__columns_extra_on_list__:
                        <th><i class="${column['icon'] if 'icon' in column else ''}"></i> ${column['name']}</th>
                    % endfor
                % endif
                % if not read_only:
                    <td style="width:80px !important;"><i class="icon-wrench"></i> <strong>Acciones</strong></td>
                % endif
            </tr>
        </thead>
        <tbody>
            % for item in items:
                <tr>
                    % for column in columns:
                        <%
                            if not hasattr(item, str(column.name)):
                                continue

                            if column.name in item.__columns_exclude_on_list__:
                                continue

                            column_type = str(column.type).lower()
                            if '(' in column_type:
                                column_type = column_type.split('(')[0]

                        %>
                        <td class='${column_type}_data'>
                            <%
                                if column.name in item.__columns_renderers_on_list__.keys():
                                    item_data = item.__columns_renderers_on_list__[column.name](item.__dict__[column.name])
                                    link = icon = None
                                else:
                                    item_data, icon, link = get_column_data(item, column)
                            %>
			                % if not icon is None:
                                <i class="${icon}"></i>
                            % endif
                            % if link:
                                <a href="${link}">${item_data}</a>
                            % else:
                                ${item_data}
                            % endif
                        </td>
                    % endfor
                    <% primary_key = get_item_primary_key(item, columns) %>
                    % if hasattr(item, '__extra_actions__') and item.__extra_actions__:
                        % for column in item.__columns_extra_on_list__:
                            <td>
                                <%
                                    data = column['data']
                                    if callable(column['data']):
                                        data = column['data'](column, item, primary_key)
                                %>
                                ${data}
                            </td>
                        % endfor
                    % endif
                    <td>
                        <div class="btn-group">
                            % if foreign_selection:
                                <a class="btn foreign-selection" data-content="${primary_key}" data-title="${item}" href="#">Seleccionar</a>
                            % else:
                                <a class="btn btn-primary" href="${dir_path}show/${primary_key}">Ver</a>
                                % if not read_only:
                                    <button class="btn btn-inverse dropdown-toggle" data-toggle="dropdown">
                                        <span class="caret"></span>
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><a class="" href="${dir_path}update/${primary_key}">Editar</a></li>
                                        <li><a class="" href="${dir_path}delete/${primary_key}">Borrar</a></li>
                                        % if hasattr(item, '__extra_actions__') and item.__extra_actions__:
                                            % for action in item.__extra_actions__:
                                                <%
                                                    if 'url' in action:
                                                        action_href = action['url'] + str(primary_key)
                                                    else:
                                                        action_href = dir_path + action['action'] + str(primary_key)
                                                %>
                                                <li><a class="${action['class'] if 'class' in action else ''}" href="${action_href}">${action['name']}</a></li>
                                            % endfor
                                        % endif
                                    </ul>
                                % endif
                            % endif
                        </div>
                    </td>
                </tr>
            % endfor
        </tbody>
    </table>
    % if pagination and pagination.pages > 1:
       <div class="pagination">
            <ul>
                % if pagination.has_prev:
                    <li><a href="${current_url(page=current_page - 1)}">Anterior</a></li>
                % endif
                % for page_number in pagination.iter_pages():
                    % if page_number:
                        <li class="${'active' if page_number == current_page else ''}"><a href="${current_url(page=page_number)}">${page_number}</a></li>
                    % else:
                        <li class="disabled"><a href="#">...</a></li>
                    % endif
                % endfor
                % if pagination.has_next:
                    <li><a href="${current_url(page=current_page + 1)}">Siguiente</a></li>
                % endif
            </ul>
        </div>
    % endif
% else:
    <p class="alert alert-notice">No se encontró nada</p>
% endif

