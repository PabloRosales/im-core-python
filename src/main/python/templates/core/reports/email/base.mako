<%
    from datetime import date
%>
<div style="margin:0;padding:30px 0;width:100%;font-family:Arial,Verdana,sans-serif;background:#f6f6f6;">
    <table border="0" cellpadding="0" cellspacing="0" width="800" align="center" style="">
        <tr>
            <td style="font-size:22px;font-weight:bold;padding:5px 0 3px 0;font-family:Helvetica,sans-serif;">
                ${title}
            </td>
        </tr>
        <tr>
            <td style="padding-bottom:3px;">
                <span style="font-size:15px;font-weight:normal;color:#666;">${subtitle}</span>
            </td>
        </tr>
        ${hr()}
        ${next.body()}
        ${hr()}
        ${hr()}
        <tr>
            <td style="padding:13px 70px 0 70px;font-size:13px;text-align:center;border-top:1px solid #ccc;color:#444;">Este reporte fue generado autom&aacute;ticamente por ${brand} el d&iacute;a ${date.today().strftime('%Y-%m-%d')} y no representa resultados finales. Los datos pueden corregirse en base a revisiones posteriores.</td>
        </tr>
    </table>
</div>

<%def name="hr(border=False)">
    % if border:
        <tr><td style="border-top:1px solid #ccc;margin:3px 0;">&nbsp;</td></tr>
    % else:
        <tr><td>&nbsp;</td></tr>
    % endif
</%def>
