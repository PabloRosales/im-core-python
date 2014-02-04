<%inherit file="${context.get('__inherit__')}"/>
<%namespace name="custom" file="/layouts/helpers/custom.mako" inheritable="True"/>
<%namespace name="form" file="/layouts/helpers/form.mako" inheritable="True"/>
<%namespace name="link" file="/layouts/helpers/link.mako" inheritable="True"/>
<%namespace name="form_" file="/layouts/helpers/form_.mako" inheritable="True"/>
<%namespace name="toolbar" file="/layouts/helpers/toolbar.mako" inheritable="True"/>
<%namespace name="toolbar_" file="/layouts/helpers/toolbar_.mako" inheritable="True"/>
<%namespace name="detailview" file="/layouts/helpers/detailview.mako" inheritable="True"/>
<%namespace name="detailview_" file="/layouts/helpers/detailview_.mako" inheritable="True"/>

<%def name="content(index=0)">
    <%
        sections = context.get('__sections__')
        template = context.lookup.get_template(sections[index])
        helpers.custom = custom
        helpers.form = form
        helpers.link = link
        helpers.form_ = form_
        helpers.toolbar = toolbar
        helpers.toolbar_ = toolbar_
        helpers.detailview = detailview
        helpers.detailview_ = detailview_
        template.render_context(context)
    %>
</%def>


${next.body()}
