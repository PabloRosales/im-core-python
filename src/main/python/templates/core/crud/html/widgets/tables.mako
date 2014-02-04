<%def name="simple(headers, data, mapping)">
    <table class="table table-bordered table-striped table-condensed">
        <thead>
            <tr>
                % for header in headers:
                    <th>${header}</th>
                % endfor
            </tr>
        </thead>
        <tbody>
            % for item in data:
                <tr>
                    % for i, attribute in enumerate(mapping):
                        <td>${getattr(item, attribute)}</td>
                    % endfor
                </tr>
            % endfor
        </tbody>
    </table>
</%def>