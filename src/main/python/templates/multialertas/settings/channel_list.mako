% if categories: 
     <font color=#B8B8B8>Seleccione la categoria que desea eliminar</font>	
     <br> <br>
     <form name="formCarrierData" id="frmCarrier" action="${base_url}delete_category/confirm" > 
     <select name = "category" >
     % for category in categories: 
           <option value = "${category.id}_${category.name}"> ${category.name} </option>
     % endfor
     </select>
      <input type="submit" value="Eliminar" class="btn" /> 

% endif 