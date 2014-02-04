<%inherit file="${context.get('__layout__')}"/> \
<%namespace name="custom" file="${context.get('this').custom_helpers}" inheritable="True"/>\
<%namespace name="form" file="/layouts/helpers/form.mako" inheritable="True"/>\
<%namespace name="link" file="/layouts/helpers/link.mako" inheritable="True"/>\
<%namespace name="toolbar" file="/layouts/helpers/toolbar.mako" inheritable="True"/>\
<%namespace name="detailview" file="/layouts/helpers/detailview.mako" inheritable="True"/>\
<%
    helpers.custom = custom
    helpers.form = form
    helpers.link = link
    helpers.toolbar = toolbar
    helpers.detailview = detailview
    #assets.registerStyle = registerStyle
    #assets.registerScript = registerScript
    next.body(**context.kwargs)
%>
<%block name="styles">
<%include file="/layouts/assets/register_styles.mako" />
</%block>
<%block name="scripts">
<%include file="/layouts/assets/register_scripts.mako" />
</%block>
<%block name="js_defaults">
<%include file="/layouts/assets/default_scripts.mako" />
</%block>
