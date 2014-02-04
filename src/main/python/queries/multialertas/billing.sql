select stats_date, sum(transaction_total) as transac, 
       sum(transaction_success_total) as success, 
       sum(transaction_local_price) as local_price , sum(transaction_price) tranc_price
from st_billing_daily_stats
where stats_date >= '2013-01-01'
and telco_code = :telco
group by stats_date;