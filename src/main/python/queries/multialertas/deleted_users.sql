SELECT mu.msisdn as telefono, us.deleted as Eliminado FROM
mobile_user mu
JOIN user_suscriptions us ON ( mu.mobile_user_id = us.mobile_user_id)
JOIN channel_category cc ON ( cc.channel_category_id = us.channel_category_id)
JOIN channel_category_conf ccc ON (cc.channel_category_id = ccc.channel_category_id)
JOIN carrier_configuration cconf ON ( cconf.carrier_configuration_id = ccc.carrier_configuration_id)
JOIN short_code_group scg ON ( cconf.short_code_group_id = scg.short_code_group_id)
WHERE scg.carrier_id = 1
and us.is_deleted = 1
and us.deleted BETWEEN DATE(:date_start) AND DATE(:date_end) ;
