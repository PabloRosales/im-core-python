## Simple base template for html5 with boostrap
<!doctype html>
<html>
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
    <link rel='stylesheet' id='style-bootstrap-css' href="${CDN}/css/bootstrap-2.min.css" type='text/css' media='all' />
    <link rel='stylesheet' id='style-bootwstrap-responsive-css' href="${CDN}/css/bootstrap-responsive-2.min.css" type='text/css' media='all' />
    <link rel='stylesheet' id='style-style-css' href="${STATIC}/css/application.css" type='text/css' media='all' />
    <%block name="css" />
</head>
<body class="${body_class or ''}">
    ${next.body()}
    <script type='text/javascript' src="${CDN}/js/jquery-1.7.2.min.js"></script>
    <script type='text/javascript' src="${CDN}/js/bootstrap-2.min.js"></script>
    <%block name="javascript" />
    <%include file="/core/analytics.mako" />
</body>
</html>
