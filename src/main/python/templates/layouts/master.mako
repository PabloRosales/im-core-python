<!DOCTYPE html>
<html lang="es">
<head>
    <!-- META -->
    <meta charset="utf-8">
    <meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1' />
    <meta name='viewport' content="width=device-width,initial-scale=1.0" />
    <!-- /META -->

    <!-- STYLES -->
    <%block name="styles">
    </%block>
    <style type="text/css">\
    <%block name="css">
    </%block>
    </style>
    <!-- /STYLES -->
    
    <!-- SCRIPTS -->
    <script type=text/javascript> \
    <%block name="js_defaults">
    </%block>
    </script>
        
    <%block name="scripts">
    </%block>
    <!-- head js -->
    <script type=text/javascript> \
    <%block name="js_head">
    </%block>
    </script>
    <!-- /head js -->        

    <!-- /SCRIPTS -->

    <title>
    % if not title is UNDEFINED:
        ${title}
    %else:
        ${controller}
    % endif
    </title>

</head>
<body class="${body_class if not body_class is UNDEFINED else controller}">
    <!-- bodystart js -->
    <script type=text/javascript> \
    <%block name="js_bodystart">
    </%block>
    </script>
    <!-- /bodystart js -->

    <!-- CONTENT -->
    ${next.body()}
    <!-- /CONTENT -->

    <!-- bodyend js -->
    <script type=text/javascript> \
    <%block name="js_bodyend">
    </%block>
    </script>
    <!-- bodyend js -->

    <!-- ready js -->
    <script type=text/javascript> 
     $(function() { \
    <%block name="js_ready"> \
    </%block>
    });
    </script>
    <!-- /ready js -->
    
    ${helpers.custom.footer()}
    <%block name="footer">
    </%block>
</body>
</html>
