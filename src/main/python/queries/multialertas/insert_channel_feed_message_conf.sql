INSERT INTO channel_feed_message_conf (channel_category_conf_id, channel_feed_message_id)
SELECT channel_category_conf_id, :channel_feed_message_id
FROM channel_category_conf
WHERE is_active = 1;