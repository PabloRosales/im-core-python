<%namespace file="form.mako" import="form" />

% if item:
    <div class="btn-toolbar">
        <div class="btn-group">
            <a class="btn" href="../../add"><i class="icon-plus"></i> Nuevo</a>
        </div>
        <div class="btn-group">
            <a class="btn" href="${current_url()}"><i class="icon-refresh"></i> Recargar</a>
            <a class="btn" href="../../list"><i class="icon-th-list"></i> Listado</a>
            <a class="btn" href="../../show/${item_id}"><i class="icon-wrench"></i> Ver</a>
            <a class="btn btn-danger" href="../../delete/${item_id}"><i class="icon-remove"></i> Eliminar</a>
        </div>
        % if toolbar:
            <%include file="${toolbar + '.mako'}" />
        % endif
    </div>
    <br />
    <form class="form-horizontal" action="." method="post">
        ${form(columns, item)}
        <div class="form-actions form-actions-no-background">
            <a style="color: #333; text-decoration: underline;" href="../../list" tabindex="100">Cancelar</a>
            &nbsp;
            <input class="btn btn-primary" type="submit" name="submit" value="Guardar" tabindex="101" />
        </div>
    </form>
% else:
    <p class="alert alert-notice">No se encontró nada</p>
% endif

% if templateDecorator :
	<%include file="${templateDecorator + '.mako'}" />
% endif
