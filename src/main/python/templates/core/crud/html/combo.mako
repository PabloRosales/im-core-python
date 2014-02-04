<div class="control-group">
    <label class="control-label" for="${name}">
        ${column.info['verbose_name'].encode('ascii', 'xmlcharrefreplace')}
    </label>
    <div class="controls">
        <div class="input-prepend">
            <span class="add-on"><i class="${column.__icon__}"></i></span>
            <select name="${name}" id="${name}">
                % for id, value in data.iteritems():
                    <option value="${id}">${value}</option>
                % endfor
            </select>
        </div>
    </div>
</div>