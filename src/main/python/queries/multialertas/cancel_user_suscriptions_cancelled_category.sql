UPDATE user_suscriptions
SET user_suscriptions.is_deleted=1, user_suscriptions.deleted = NOW()
WHERE user_suscriptions.channel_category_conf_id = :ccc_id