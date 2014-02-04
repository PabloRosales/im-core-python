SELECT
    a.key
FROM
    role r
    JOIN role_has_action USING(role_id)
    JOIN action a USING(action_id)
WHERE
    r.key IN (%(roles)s)
GROUP BY a.key
;
