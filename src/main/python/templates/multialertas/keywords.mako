<%inherit file="/core/crud/html/base.mako" />

<%
    from datetime import date
    from im.core.web.bootstrap import get_icon

    def column_icon(name):
        return '<i class="%s"></i>' % get_icon(name)

%>

% if not custom_keyword:
    <p class="alert notice">El reporte se generará del día del envío hasta hoy ${date.today()}</p>
% endif

<div class="btn-toolbar">
    <form class="form-search" action="" method="post">
        <a class="btn date-today" data-content="search" href="#">Hoy</a>
        <input id="search" class="date" type="text" value="" name="date_start">
        <input id="search-end" class="date-end" type="text" value="" name="date_end">
        <input class="input-medium search-query" type="text" value="" name="keyword" placeholder="Keyword">
        <button class="btn" type="submit">Buscar</button>
    </form>
</div>

% if ad_messages:
    <table class=" table table-bordered table-striped">
        <thead>
            <tr>
                <th>${column_icon('ad_message_id')} ID</th>
                <th>${column_icon('message')} Mensaje</th>
                <th>${column_icon('keyword')} Keyword</th>
                <th>${column_icon('send_on')} Envio</th>
                <th>${column_icon('actions')} Acciones</th>
            </tr>
        </thead>
        <tbody>
            % for ad_message in ad_messages:
                <tr>
                    <td>${ad_message.ad_message_id}</td>
                    <td>${ad_message.message}</td>
                    <td>${ad_message.keyword}</td>
                    <td>${ad_message.send_on.strftime('%Y-%m-%d')}</td>
                    <td>
                        <a class="btn btn-primary" href="${current_url(strip_querystring=True, keyword=ad_message.keyword, csv=1, ad_message_id=ad_message.ad_message_id)}" rel="popover" data-content="Esto puede tardar un rato" data-original-title="Cuidado!">CSV</a>
                    </td>
                </tr>
            % endfor
        </tbody>
    </table>
% endif