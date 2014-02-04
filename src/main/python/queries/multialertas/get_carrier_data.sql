SELECT carrier_id AS id , concat(co.name,'-',ca.name)  AS  carrier_name
FROM carrier_configuration cc
JOIN short_code_group scg USING (short_code_group_id)
JOIN carrier ca USING (carrier_id)
JOIN country co ON (cc.country_id = co.country_id);