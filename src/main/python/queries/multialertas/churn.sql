SELECT cc.name , IFNULL(DATE(deleted), DATE(created)) AS fecha,
 SUM(not us.is_deleted) AS altas, SUM(us.is_deleted) AS bajas, SUM(not us.is_deleted)-SUM(us.is_deleted) AS netos
FROM user_suscriptions us
JOIN channel_category_conf ccc USING(channel_category_conf_id)
JOIN carrier_configuration cc ON ( cc.carrier_configuration_id = ccc.carrier_configuration_id)
JOIN short_code_group scg ON  (cc.short_code_group_id = scg.short_code_group_id)
WHERE scg.carrier_id = :carrier
AND (DATE(created) BETWEEN DATE(:date_start) AND DATE(:date_end))
OR (DATE(deleted) BETWEEN DATE(:date_start) AND DATE(:date_end))
GROUP BY fecha;
