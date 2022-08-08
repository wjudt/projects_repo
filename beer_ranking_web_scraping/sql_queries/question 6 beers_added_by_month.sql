select 
	month(d.date) AS month_number
	,count(PK_date_id) as added_beers
from beer
left join date_DIM d
on PK_date_id = FK_date_id
group by month(d.date)
order by month(d.date)