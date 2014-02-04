<%def name="crud(model, pk, current='show', buttons=['add','update','list','show', 'delete'])">
    <%
        value = getattr(model, pk)
    %>
    <div class="btn-toolbar">
        % if 'add' in buttons:
            <div class="btn-group">
                % if 'add' == current:
                    <a href="../../add" class="btn"><i class="icon-refresh"></i> Limpiar</a>
                % else:
                    <a href="../../add" class="btn"><i class="icon-plus"></i> Nuevo</a>
                % endif
            </div>
        % endif
        <div class="btn-group">
            % if 'update' in buttons:
                % if 'update' == current:
                    <a href="../../update/${value}" class="btn"><i class="icon-refresh"></i> Recargar</a>
                % else:
                    <a href="../../update/${value}" class="btn"><i class="icon-wrench"></i> Editar</a>
                % endif
            % endif
            % if 'list' in buttons:
                % if 'list' == current:
                    <a href="../../list" class="btn"><i class="icon-refresh"></i> Recargar</a>
                % else:    
                    <a href="../../list" class="btn"><i class="icon-th-list"></i> Listado</a>
                % endif
            % endif
            % if 'show' in buttons:
                % if 'show' == current:
                    <a href="../../show/${value}" class="btn"><i class="icon-refresh"></i> Recargar</a>
                % else:
                    <a href="../../show/${value}" class="btn"><i class="icon-ok"></i> Ver</a>
                % endif
            % endif
            % if 'delete' in buttons:
                % if 'delete' == current:
                    <a href="../../delete/${value}" class="btn btn-danger"><i class="icon-remove"></i> Eliminar</a>
                % else:
                    <a href="../../delete/${value}" class="btn btn-danger"><i class="icon-remove"></i> Eliminar</a>
                % endif
            % endif
        </div>
    </div>
</%def>
