SELECT * 
FROM feature_set
JOIN product_has_feature_set ON (feature_set.feature_set_id = product_has_feature_set.feature_set)
WHERE product_has_feature_set.product_id = :product_id ;  
