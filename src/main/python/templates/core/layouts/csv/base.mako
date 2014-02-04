% if __sections__:
% for section in __sections__:
${recursive_render(section)}\
% endfor
% endif
<%def name="recursive_render(section, item=None, override=None)">\
% if isinstance(section, list):
% for _item in section:
${recursive_render(_item, item)}\
% endfor
% elif isinstance(section, dict):
% if 'type' in section:
<%
    _type = section['type']
%>
% elif 'template' in section:
<% template = section['template'] % {'format': __format__} %>\
<%include file="${template}.mako" />\
% elif 'sections' in section:
${recursive_render(section['sections'])}\
% endif
% else:
${section}\
% endif
</%def>