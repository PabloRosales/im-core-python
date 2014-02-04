Telefono, Marcacion, Mensaje, Fecha
% if data:
    % for item in data:
${'"%s","%s","%s","%s"' % (item.phone_number, item.short_number, item.message.replace('\n', ''), item.message_datetime)}
    % endfor
%endif

