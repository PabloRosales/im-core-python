select cc.name , ccc.channel_category_conf_id as id
FROM channel_category cc
JOIN channel_category_conf ccc ON (cc.channel_category_id = ccc.channel_category_id)
WHERE ccc.carrier_configuration_id = :carrier_conf_id ;