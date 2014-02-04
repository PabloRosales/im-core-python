SELECT DATE(scheduled_for) as date_scheduled_for, message
FROM message
WHERE DATE(scheduled_for) BETWEEN :date_start AND :date_end
AND is_active = 1 AND is_aborted = 0