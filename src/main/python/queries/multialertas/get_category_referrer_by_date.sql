SELECT c.name, c.keyword, us.source, us.referrer ,  count(*) as total
FROM user_suscriptions us
JOIN channel_category c on (us.channel_category_id = c.channel_category_id)
JOIN channel_category_conf ccf on (c.channel_category_id = ccf.channel_category_id)
JOIN carrier_configuration cc on (cc.carrier_configuration_id = ccf.carrier_configuration_id)
JOIN short_code_group scg on (scg.short_code_group_id = cc.short_code_group_id)
WHERE scg.carrier_id= :carrier_id
AND us.created BETWEEN DATE(:date_start) AND DATE(:date_end)
GROUP BY c.channel_category_id, us.source, us.referrer
ORDER BY c.channel_category_id, us.source, us.referrer;
