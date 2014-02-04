SELECT
    a.account_id
FROM
    account_user a
    JOIN account_has_website_instance USING(account_id)
    JOIN website_has_instance w USING(website_has_instance_id)
WHERE
    a.user_id = :user_id
    AND
    w.website_id = :website_id
GROUP BY user_id
;
