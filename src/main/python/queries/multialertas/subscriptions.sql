SELECT COUNT(*) as 'value', DATE_FORMAT(%(field)s, '%%Y%%m%%d') as label
FROM user_suscriptions s
WHERE %(field)s BETWEEN :date_start AND :date_end