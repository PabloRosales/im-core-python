<div class="btn-toolbar">
    <div class="btn-group">
        <a class="btn" href="${current_url()}"><i class="icon-refresh"></i> Refrescar</a>
        % if download_csv:
            <a class="btn btn-primary" href="${current_url(format='csv')}">Descargar CSV</a>
        % endif
    </div>
    % if search_type:
        <form style="float: right;" class="form-search" method="get" action="${current_url()}">
            % if 'datetime' in search_type or 'timestamp' in search_type:
                <a class="btn datetime-now" href="#" data-content="search">Ahorita</a>
            % elif 'date' in search_type:
                <a class="btn date-today" href="#" data-content="search">Hoy</a>
            % endif
            <input type="text" id="search" class="${search_type}" name="search" value="${search_term if search_term else ''}" />
            % if search_type in ('datetime', 'date', 'timestamp'):
                <input type="text" id="search-end" class="${search_type}-end" name="search2" value="${search_term_end if search_term_end else ''}" />
            % endif
            <button type="submit" class="btn">Buscar</button>
        </form>
    % endif
</div>

% if items:
    <table class=" table table-bordered table-striped">
        <thead>
            <tr>
                % for verbose in headers:
                    <th>${verbose}</th>
                % endfor
            </tr>
        </thead>
        <tbody>
            % for item in items:
                <tr>
                % for column in columns:
                    <td>
                        ${getattr(item, column)}
                    </td>
                % endfor
            </tr>
            % endfor
        </tbody>
    </table>
% else:
    <p class="alert alert-notice">No se encontró nada</p>
% endif
