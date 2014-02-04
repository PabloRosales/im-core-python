SELECT COUNT(*) as total
from user_suscriptions
JOIN mobile_user USING(mobile_user_id)
 WHERE mobile_user.is_active = 1
AND user_suscriptions.is_deleted = 0
