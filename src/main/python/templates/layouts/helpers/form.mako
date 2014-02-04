<%def name="begin(model, method='post', action='.')">
    <%
        classname = str(model.__class__.__name__)
    %>
    <form method="${method}" action="${action}" class="form-horizontal" name="${classname}-form">
</%def>

<%def name="input(model, field, icon='align-left', disabled=False)">
    <%
        classname = str(model.__class__.__name__)
        column = type(model).__mapper__.columns.get(field)
        column_name = column.info.get('verbose_name') if column.info.get('verbose_name') else column.name
        length =  column.type.length if hasattr(column.type, 'length') else -1
        value = getattr(model, field) if getattr(model, field) else ''
    %>
    <div class="control-group">
        <label for="${field}-verbose" class="control-label">${column_name}</label>
        <div class="controls">
            <div class="input-prepend">
                <span class="add-on"><i class="icon-${icon}"></i></span>
                <input type="text" 
                    % if disabled:
                        disabled="disabled"
                    % endif
                    % if length > -1:
                        maxlength=${length}
                    % endif
                tabindex="1" value="${value}" name="${classname}[${field}]" id="${field}-id">
            </div>
        </div>
    </div>
</%def>

<%def name="password(model, field, icon='align-left')">
    <%
        classname = str(model.__class__.__name__)
        column = type(model).__mapper__.columns.get(field)
        column_name = column.info.get('verbose_name') if column.info.get('verbose_name') else column.name
    %>
    <div class="control-group">
        <label for="${field}-verbose" class="control-label">${column_name}</label>
        <div class="controls">
            <div class="input-prepend">
                <span class="add-on"><i class="icon-${icon}"></i></span>
                <input type="password" tabindex="1" value="" name="${classname}[${field}]" id="${field}-id">
            </div>
        </div>
    </div>
    <div class="control-group">
        <label for="${field}-validate-verbose" class="control-label">Validar ${column_name.lower()}</label>
        <div class="controls">
            <div class="input-prepend">
                <span class="add-on"><i class="icon-${icon}"></i></span>
                <input type="password" tabindex="1" value="" name="${classname}[${field}-validate]" id="${field}-validate-id">
            </div>
        </div>
    </div>
</%def>

<%def name="textarea(model, field, rows=5, disabled=False)">
    <%
        classname = str(model.__class__.__name__)
        column = type(model).__mapper__.columns.get(field)
        column_name = column.info.get('verbose_name') if column.info.get('verbose_name') else column.name
        length =  column.type.length if hasattr(column.type, 'length') else 512
        value = getattr(model, field) if getattr(model, field) else ''
    %>
    <div class="control-group">
        <label for="${field}-verbose" class="control-label">${column_name}</label>
        <div class="controls">
            <span id="counter-${field}" class="counter">${length}⇓</span>
            
            <textarea tabindex="7" name="${classname}[${field}]" id="${field}-id" rows="${rows}" class="count" data-max="${length}">${value}</textarea>


        </div>
    </div>
</%def> 


<%def name="select(model, field, id, options)">
    <%
        classname = str(model.__class__.__name__)
        column = type(model).__mapper__.columns.get(field)
        if column is None:
            column = type(model).__mapper__.columns.get(field + '_id')
        if column is None:
            column_name = field.capitalize()
        else:
            column_name = column.info.get('verbose_name') if column.info.get('verbose_name') else column.name
            
        fk = getattr(model, field) if getattr(model, field) else None
        value = getattr(fk, id) if fk else None
    %>
    <div class="control-group">
        <label for="${field}-verbose" class="control-label">${column_name}</label>
        <div class="controls">
            <div class="input-prepend">
                <select name="${classname}[${field}]" id="${field}-id">
                    % if not value:
                        <option value="" selected="selected"></option>
                    % endif
                    % for option in options:
                        % if value and option[0] == value: 
                            <option value="${option[0]}" selected="selected">${option[1]}</option>
                        % else:
                            <option value="${option[0]}">${option[1]}</option>
                        % endif 
                    % endfor
                </select>
                <script type="text/javascript">$('#${field}-id').chosen()</script>
            </div>
        </div>
    </div>
</%def>

<%def name="multiselect(model, field, id, options)">
    <%
        classname = str(model.__class__.__name__)
        column = type(model).__mapper__.columns.get(field)
        if column is None:
            column = type(model).__mapper__.columns.get(field + '_id')
        if column is None:
            column_name = field.capitalize()
        else:
            column_name = column.info.get('verbose_name') if column.info.get('verbose_name') else column.name
            
        fk = getattr(model, field) if getattr(model, field) else None
        values = []
        for f in fk:
            if getattr(f, id):
                values.append(getattr(f, id))
        print "VALUES", values
    %>
    <div class="control-group">
        <label for="${field}-verbose" class="control-label">${column_name}</label>
        <div class="controls">
            <div class="input-prepend">
                <select multiple name="${classname}[${field}]" id="${field}-id">
                    % for option in options:
                        % if option[0] in values: 
                            <option value="${option[0]}" selected="selected">${option[1]}</option>
                        % else:
                            <option value="${option[0]}">${option[1]}</option>
                        % endif 
                    % endfor
                </select>
                <script type="text/javascript">$('#${field}-id').chosen()</script>
            </div>
        </div>
    </div>
</%def>

<%def name="end(model, submit_value='Guardar', cancel_url='../../list')">
    <%
        classname = str(model.__class__.__name__)
    %>
    <div class="form-actions form-actions-no-background">
        <a tabindex="100" href="${cancel_url}" style="color: #333; text-decoration: underline;">Cancelar</a>
        &nbsp;
        <input type="submit" tabindex="101" value="${submit_value}" name="${classname}-submit" id="${classname}-submit-id" class="btn btn-primary">
    </div>
</form>
</%def>

