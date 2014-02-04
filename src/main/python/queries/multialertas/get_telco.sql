SELECT distinct (short_code.telco_code ) as telco_code
FROM short_code
JOIN short_code_group ON (short_code_group.short_code_group_id = short_code.short_code_group_id)
WHERE short_code_group.carrier_id = :carrier_id;