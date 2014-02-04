UPDATE channel_category_conf 
SET is_deleted= 1
WHERE channel_category_conf_id = :ccc_id;