SELECT mc.*, cfm.base_path
FROM multimedia_content mc
JOIN channel_feed_multimedia cfm ON cfm.channel_feed_multimedia_id = mc.channel_feed_multimedia_id
WHERE multimedia_content_id = :multimedia_content_id;