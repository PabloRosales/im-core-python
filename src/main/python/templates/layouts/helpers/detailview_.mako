<%def name="makerow(model, field, kind='text', icon='align-left')">
    <%
        column = type(model).__mapper__.columns.get(field)
        if column is None:
            column = type(model).__mapper__.columns.get(field + '_id')
        
        if column is None:
            column_name = field.capitalize()
        else:
            column_name = column.info.get('verbose_name') if column.info.get('verbose_name') else column.name
        value = getattr(model, field) if getattr(model, field) else ''
        if not icon:
            icon='align-left'
    %>
    % if kind == 'text':
    <tr>
        <td style="text-align: right;background: #f9f9f9;"><strong>${column_name}</strong> <i class="icon-${icon}"></i></td>
        <td>
            % if value:
                ${value}
            % else:
                &mdash;
            % endif
        </td>
    </tr>
    % elif kind == 'list':
    <tr>
        <td style="text-align: right;background: #f9f9f9;"><strong>${column_name}</strong> <i class="icon-${icon}"></i></td>
        <td>
            % if value and len(value) > 0:
                % for val in value:
                    % if val:
                        &nbsp;<code>${val}</code>&nbsp;
                    % endif
                % endfor
            % else:
                &mdash;
            % endif
        </td>
    </tr>
    % endif
</%def>

<%def name="table(model, properties)">

<table class="table table-bordered table-striped table-condensed">
    <thead>
        <tr>
            <th style="width:230px;">Atributo</th>
            <th>Valor</th>
        </tr>
    </thead>
    <tbody>
        % for property in properties:
            ${makerow(model, property.get('field'), property.get('kind'), property.get('icon'))}
        % endfor
    </tbody>
</table>

</%def>

