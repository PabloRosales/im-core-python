<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>${title}</title>
    <meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1' />
    <meta name='viewport' content="width=device-width,initial-scale=1.0" />
    <link rel='stylesheet' id='style-style-css' href="${STATIC}/css/style.css" type='text/css' media='all' />
    <%block name="css" />
</head>
<body>
    ${next.body()}
    <%block name="javascript" />
</body>
</html>
