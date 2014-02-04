SELECT  instance.instance_id as instance_id,
        instance.name as instance_name ,
        country.country_id as country_id,
        country.name as country_name,
        carrier.carrier_id as carrier_id,
        carrier.name as carrier_name,
        product.product_id as product_id,
        product.name as product_name
FROM instance 
JOIN country ON (country.country_id = instance.instance_id)
JOIN carrier ON (carrier.carrier_id = instance.carrier_id)
JOIN product ON (product.product_id = instance.product_id)
JOIN website_has_instance ON (website_has_instance.instance_id = instance.instance_id)
JOIN account_has_website_instance ON ( website_has_instance.website_has_instance_id = account_has_website_instance.website_has_instance_id)
WHERE website_has_instance.website_id = :website_id
AND account_has_website_instance.account_id = :account_id ; 
