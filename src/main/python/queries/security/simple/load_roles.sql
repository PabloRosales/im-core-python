SELECT
    r.key
FROM
    account_user au
    JOIN account_has_website_instance USING(account_id)
    JOIN website_has_instance wi USING(website_has_instance_id)

    JOIN account_user_has_role USING(account_user_id)
    JOIN role r USING(role_id)
    JOIN website_has_role wr ON(r.role_id = wr.role_id AND wr.website_id = wi.website_id)
WHERE
    wi.website_id = :website_id
    AND
    au.user_id = :user_id
;
