SELECT
	user.username,
	IFNULL(
		GROUP_CONCAT(user_role.name SEPARATOR ','),
	"") AS roles,
	user.password,
	user.user_id 
FROM
	user 
	LEFT JOIN user_to_role ON (user.user_id = user_to_role.user_id)
	LEFT JOIN user_role ON (user_to_role.user_role_id = user_role.user_role_id)
WHERE
	user.username=:username
GROUP BY
	user.user_id;
