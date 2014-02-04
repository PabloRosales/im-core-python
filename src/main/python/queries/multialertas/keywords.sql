SELECT phone_number, short_number, message, message_datetime
FROM message_log
WHERE
    direction = 'MO'
    AND message_datetime BETWEEN :date_start AND :date_end
    AND message = :keyword