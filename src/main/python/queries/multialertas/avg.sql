SELECT cc.name , ROUND(AVG(TO_DAYS(IFNULL(us.deleted, NOW()))- TO_DAYS(us.created))) as prom
FROM user_suscriptions us
JOIN channel_category cc USING ( channel_category_id)
JOIN channel_category_conf ccc ON (cc.channel_category_id = ccc.channel_category_id)
JOIN carrier_configuration cconf ON ( cconf.carrier_configuration_id = ccc.carrier_configuration_id)
JOIN short_code_group scg ON ( cconf.short_code_group_id = scg.short_code_group_id)
WHERE scg.carrier_id = :carrier_id
AND us.created >= DATE(:start_date)
group by cc.name ; 