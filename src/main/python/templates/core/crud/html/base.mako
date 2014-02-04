## Base template for use on admins
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>${title}</title>
    <link rel='dns-prefetch' href='//www.google-analytics.com' />
    <link rel='dns-prefetch' href='//static.interactuamovil.com' />
    <link rel="prefetch" href="${CDN}/js/jquery-1.7.2.min.js" />
    <link rel="prefetch" href="${CDN}/js/bootstrap-2.min.js" />
    <link rel="prefetch" href="http://www.google-analytics.com/ga.js" />
    <meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1' />
    <meta name='viewport' content="width=device-width,initial-scale=1.0" />
    <link rel='stylesheet' id='style-bootstrap-css' href="${CDN}/css/bootstrap-2.1.1.min.css" type='text/css' media='all' />
    <link rel='stylesheet' id='style-bootwstrap-responsive-css' href="${CDN}/css/bootstrap-responsive-2.1.1.min.css" type='text/css' media='all' />
    <link rel='stylesheet' id='style-bootwstrap-addon-css' href="${CDN}/css/rickshaw.min.css" type='text/css' media='all' />
    <link rel='stylesheet' id='style-bootstrap-css' href="${CDN}/css/jquery-ui/jquery-ui-1.8.22.custom.css" type='text/css' media='all' />
    <link rel='stylesheet' id='style-style-css' href="${CDN}/css/anytime.css" type='text/css' media='all' />
    <link rel='stylesheet' id='style-style-css' href="${CDN}/css/d3.css" type='text/css' media='all' />
    <link rel='stylesheet' id='style-style-css' href="${CDN}/css/crud.css" type='text/css' media='all' />
    <link rel='stylesheet' id='style-style-css' href="${STATIC}/css/application.css" type='text/css' media='all' />
    <%block name="css" />
    <script type="text/javascript">
        window.base_url = '${'%s://%s' % (conf('werkzeug.url_scheme'), conf('werkzeug.host'))}';
    </script>
    <script type='text/javascript' src="${CDN}/js/jquery-1.7.2.min.js"></script>
    <script type='text/javascript' src="${CDN}/js/jquery-ui-1.8.22.custom.min.js"></script>
    <script type='text/javascript' src="${CDN}/js/date.js"></script>
    <script type='text/javascript' src="${CDN}/js/anytime.js"></script>
    <script type='text/javascript' src="${CDN}/js/bootstrap-2.1.1.js"></script>
    <script type='text/javascript' src="${CDN}/js/crossfilter.min.js"></script>
    <script type='text/javascript' src="${CDN}/js/crud.js"></script>
    <script type='text/javascript' src="${CDN}/js/crud-dates.js"></script>
    <script type='text/javascript' src="${CDN}/js/url.js"></script>
    <script type='text/javascript' src="${CDN}/js/jquery.cookies.2.2.0.min.js"></script>
    <%block name="javascript" />
</head>
<body class="${body_class or ''}">
    <%include file="menu.mako" />
    <div class="container" id="main">
        % if logged_in and conf('crud.show_instance_toolbar', False):
            <div class="btn-toolbar">
                <div class="btn-group">
                    <a class="btn btn-mini" href="${base_url}"><i class="icon-th-large"></i> Dashboard</a>
                    % if not 'admin' in body_class and not 'home' in body_class:
                        <a class="btn btn-mini" href="${current_url(change_instance=1)}"><i class="icon-wrench"></i> Cambiar de instancia</a>
                    % endif
                    <a class="btn btn-mini disabled" href="${menu_url('admin.logs.list')}"><i class="icon-eye-open"></i> Log</a>
                </div>
            </div>
        % endif
        <div class="page-header">
            <h1>
                ${title}
                <small>${subtitle}</small>
            </h1>
        </div>
        % for level, flashes in get_flash_messages(request, clear=True).iteritems():
            % for flash in flashes:
                    <div class="alert ${'alert-%s' % level if level != 'notice' else ''}">
                        <a class="close" data-dismiss="alert" href="#">×</a>
                        <strong>${flash}</strong>
                    </div>
            % endfor
        % endfor
        ${next.body()}
    </div>
    <%include file="/core/analytics.mako" />
</body>
</html>
