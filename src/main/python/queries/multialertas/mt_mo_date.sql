select stats_date, sum(mo_total) 'MO', sum(mt_ok_total) 'MT'
from st_message_daily_stats
where stats_date BETWEEN DATE(:date_start) AND DATE(:date_end)
and telco_code = :telco
group by stats_date;

