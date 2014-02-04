UPDATE user_session SET status = 'CLOSED', closed_on = NOW() WHERE user_session_id = :user_session_id
