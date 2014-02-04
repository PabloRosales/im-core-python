<% columns_count = len(columns) - 1 %>\
% for verbose in headers:
${verbose}${'\n' if loop.index == columns_count else ','}\
% endfor
% for item in items:
% for column in columns:
"${getattr(item, column)}"${'' if loop.index == columns_count else ','}\
% endfor
${'' if loop.index == len(items)-1 else '\n'}\
% endfor