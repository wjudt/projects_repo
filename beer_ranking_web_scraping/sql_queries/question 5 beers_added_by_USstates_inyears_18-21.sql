select 
	month(d.date) AS month
	,year(d.date) as year
	,count(PK_date_id) as added_beers
from beer
inner join date_DIM d
on PK_date_id = FK_date_id
inner join brewery_DIM br
on FK_brewery_id = PK_brewery_id
inner join country_DIM c
on FK_country_id = PK_country_id
where 
	d.date >= '2018-01-01' 
	and 
	d.date <= '2021-12-31'
	and
	c.country_name = 'United States'
group by year(d.date), month(d.date)
order by year(d.date), month(d.date)