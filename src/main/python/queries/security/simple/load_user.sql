SELECT
    user.username,
    user.password,
    user.user_id 
FROM
    user 
    JOIN account_user USING(user_id)
    JOIN account_has_website_instance USING(account_id)
    JOIN website_has_instance USING(website_has_instance_id)
WHERE
    user.username=:username
    AND
    user.password=:password
    AND
    website_has_instance.website_id=:website_id
GROUP BY
    user.user_id;
