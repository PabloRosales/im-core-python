SELECT cc.name 'category', DATE(MAX(m.scheduled_for)) 'last_scheduled', IFNULL(DATEDIFF(DATE(MAX(m.scheduled_for)), CURDATE()), 0) 'days_left'
FROM carrier_configuration ca 
JOIN channel_category_conf ccc ON (ccc.carrier_configuration_id = ca.carrier_configuration_id)
JOIN channel_category cc ON (ccc.channel_category_id = cc.channel_category_id) 
LEFT JOIN channel_feed_message_conf mc ON (mc.channel_category_conf_id = ccc.channel_category_conf_id)
LEFT JOIN channel_feed_message m ON (m.channel_feed_message_id = mc.channel_feed_message_id)
JOIN short_code_group scg ON (ca.short_code_group_id = scg.short_code_group_id)
WHERE scg.carrier_id = :carrier_id 
    AND cc.is_active = 1 AND cc.is_deleted = 0
    AND ccc.is_active = 1 AND ccc.is_deleted = 0    
GROUP BY cc.channel_category_id
HAVING days_left <= :min_val