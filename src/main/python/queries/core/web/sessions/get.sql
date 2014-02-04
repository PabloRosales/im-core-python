SELECT *
FROM user_session
WHERE session_id = :session_id AND (expires_on IS NULL OR NOW() < expires_on) AND status = 'OPEN'
