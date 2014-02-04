<%namespace file="form.mako" import="form" />

<div class="btn-toolbar">
    <div class="btn-group">
        <a class="btn" href="../list"><i class="icon-th-list"></i> Listado</a>
    </div>
    % if toolbar:
        <%include file="${toolbar + '.mako'}" />
    % endif
</div>
<h2>Agregar ${subtitle}</h2>
<br />
<form class="form-horizontal" action="." method="post">
    ${form(columns, item, crud_type='add')}
    <div class="form-actions form-actions-no-background">
        <a style="color: #333; text-decoration: underline;" href="../list" tabindex="100">Cancelar</a>
        &nbsp;
        <input class="btn btn-primary" type="submit" name="submit" value="Guardar" tabindex="101" />
    </div>
</form>


% if templateDecorator :
	<%include file="${templateDecorator + '.mako'}" />
% endif
