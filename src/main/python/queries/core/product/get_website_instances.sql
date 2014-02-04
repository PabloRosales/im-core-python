SELECT instance.name as instance_name , country.name as country_name , 
	carrier.name as carrier_name , product.name as product_name
FROM instance 
JOIN  product USING ( product_id)
JOIN  country ON (instance.country_id = country.country_id)
JOIN  carrier ON (instance.carrier_id = carrier.carrier_id)
JOIN  website_has_instance  ON  (instance.instance_id = website_has_instance.instance_id)
WHERE website_has_instance.website_id = :website_id ;
