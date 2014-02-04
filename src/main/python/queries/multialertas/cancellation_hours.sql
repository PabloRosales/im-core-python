SELECT HOUR(deleted) label, COUNT(*) value
FROM user_suscriptions us
JOIN mobile_user mu ON mu.mobile_user_id = us.mobile_user_id
-- AND mu.telco_code = '056'
WHERE deleted IS NOT NULL
-- AND deleted BETWEEN '2012-07-01 00:00:00' AND '2012-07-31 23:59:59'
GROUP BY HOUR(deleted)