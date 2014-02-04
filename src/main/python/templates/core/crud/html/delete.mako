<div class="btn-toolbar">
    <div class="btn-group">
        <a class="btn" href="../../list"><i class="icon-th-list"></i> Listado</a>
        <a class="btn" href="../../update/${id}"><i class="icon-wrench"></i> Editar</a>
    </div>
</div>
<br />
<div class="alert alert-error">
    <h3>¿Esta seguro de que desea eliminar el ${item.__verbose_name__} ${item}?</h3>
    <p><span class="label label-important">¡Si se borra este elemento no se podrá recuperar!</span></p>
</div>
<form action="." method="post">
    <a style="color: #333;font-weight: bold;text-decoration: underline;" href="../../list">Cancelar</a> &nbsp;
    <input class="btn btn-danger" type="submit" name="submit" value="Eliminar" />
</form>

