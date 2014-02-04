<%inherit file="/core/crud/html/base.mako" />
	  
 <font color=#B8B8B8>Desea borrar ${category_name} </font>
 <br>
 <br>
 <form name = "confirmDel" action = "${base_url}delete_category/delete">
   <input type = "hidden" name="category_id" value="${category_id}" >
  <inpyt type="submit"  value="Eliminar" class="btn" />
  
