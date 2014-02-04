UPDATE
 user_session
SET 
 status = 'CLOSED',
 closed_on = NOW()
WHERE session_id = :session_id
