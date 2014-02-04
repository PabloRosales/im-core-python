<%inherit file="/core/crud/html/base.mako" />

<div class="row-fluid">
<div class="span4">

% if carriers: 
<font color=#B8B8B8>Seleccione el carrier para ver el reporte</font>
<br><br>
  <form name="formCarrierData" id="frmCarrier" action="${base_url}/multialertas/reports/list/" >
        <select name="slct" >
        % for carrier in carriers:
                <option value="${carrier.id}" > ${carrier.carrier_name} </option>
        % endfor
        </select>
        <input type="submit" value="Buscar" class="btn" />
  </form>
%endif

</div>
<div id="result" class="span8"> </div>
</div>
<script>
          $("#frmCarrier").submit(function(event){
                event.preventDefault();
                var $form = $(this),
                term=$form.find('select[name="slct"]').val(),
                url=$form.attr('action');
                $('#result').load(url+"?opt="+term);
                });
</script>

