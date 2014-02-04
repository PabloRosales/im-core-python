<%
    from im.core.web.werkzeug import get_column_data
%>

% if item:
    <div class="btn-toolbar">
        <div class="btn-group">
            <a class="btn" href="${current_url()}"><i class="icon-refresh"></i> Recargar</a>
            <a class="btn" href="../../list"><i class="icon-th-list"></i> Listado</a>
            % if not read_only:
                <a class="btn" href="../../update/${id}"><i class="icon-wrench"></i> Editar</a>
                <a class="btn btn-danger" href="../../delete/${id}"><i class="icon-remove"></i> Eliminar</a>
            % endif
        </div>
        % if toolbar:
            <%include file="${toolbar + '.mako'}" />
        % endif
    </div>
    <br />
    <table class="table table-bordered table-striped table-condensed">
        <thead>
            <tr>
                <th style="width:230px;">Atributo</th>
                <th>Valor</th>
            </tr>
        </thead>
        <tbody>
            % for column in columns:
                <%
                    column_icon = column.__icon__
                    if item.__columns_renderers_on_show__ and column.name in item.__columns_renderers_on_show__:
                        item_data = item.__columns_renderers_on_show__[column.name](item.__dict__[column.name])
                        icon = link = None
                    if item.__columns_renderers_on_list__ and column.name in item.__columns_renderers_on_list__:
                        item_data = item.__columns_renderers_on_list__[column.name](item.__dict__[column.name])
                        icon = link = None
                    else:
                        item_data, icon, link = get_column_data(item, column, crud_type='show')
                %>
                <tr>
                    <td style="text-align: right;background: #f9f9f9;"><strong>${column.info['verbose_name']}</strong> <i class="${column_icon}"></i></td>
                    <td>
                        <i class="${icon}"></i>
                        % if link:
                            <a href="${link}">${item_data}</a>
                        % else:
                            ${item_data}
                        % endif
                    </td>
                </tr>
            % endfor
        </tbody>
    </table>
% else:
    <p class="alert alert-notice">No se encontró nada</p>
% endif

