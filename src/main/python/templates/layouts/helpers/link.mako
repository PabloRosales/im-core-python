## -*- coding: utf-8 -*-

<%def name="format_params(params={})">
<%  
    num = len(params.keys()) 
    r = ""
    for i in xrange(num):
        if i == 0:
            r += "?"
        r += str(params.keys()[i]) + "=" + str(params.values()[i])
        if i != num-1:
            r += "&"
    return r
%>
</%def>

<%def name="format_options(htmlOptions={})">
<%  
    r = ""
    for key, value in htmlOptions.iteritems():
        r += str(key) + "=\"" + str(value).replace('"', "'") + "\" "
    return r
%>
</%def>

<%def name="btn(text, path, params={}, icon='', **kwargs)">
<%
    if path.startswith("/"):
        path = path[1:]
    if isinstance(params, dict):    
        formatted_params = format_params(params)
    else:
        params = "" + params
        if not path.startswith("/"):
            params = "/" + params
        formatted_params = params 
%>\
<a href="${BASE}${path}${formatted_params}" class="btn" ${format_options(kwargs)}>\
% if icon:
    <i class="icon-${icon}"></i> \
% endif
 ${text}</a>
</%def>

<%def name="a(text, path, params={}, icon='', **kwargs)">
<%
    if path.startswith("/"):
        path = path[1:]
    if isinstance(params, dict):    
        formatted_params = format_params(params)
    else:
        params = str(params)
        if not path.startswith("/"):
            params = "/" + params
        formatted_params = params         
%>\
<a href="${BASE}${path}${formatted_params}" ${format_options(kwargs)}>\
% if icon:
    <i class="icon-${icon}"></i> \
% endif
 ${text}</a>
</%def>
