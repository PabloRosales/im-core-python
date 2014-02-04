INSERT INTO user_session (user_id, session_id, data, created_on, modified_on, expires_on, closed_on, status)
VALUES (:user_id, :session_id, :data, NOW(), NOW(), :expires_on, NULL, 'OPEN')
ON DUPLICATE KEY UPDATE data = :data;
