select 
	brewery_name
	,year(date) as year_added
	,sum(count(PK_beer_id)) over (partition by brewery_name order by year(date)) as rooling_sum_beers_per_year
	,count(PK_beer_id) as beers_in_year
	,round(avg(avg_score), 1) as brewery_avg_score
from beer
	inner join brewery_DIM
	on FK_brewery_id = PK_brewery_id
	inner join date_DIM
	on FK_date_id = PK_date_id

where brewery_name in (
	-- upper subquery where name of breweries were obtained
	select brewery_name
	from (
		-- basic subquery which allowed to find brewery from USA,
		-- which has average scoe greater than 4.2 and had sum of beers greater than 100
		select
				brewery_name
				,avg(avg_score) as avg_score
				,count(PK_beer_id) as beer_count
			from beer
			inner join brewery_DIM
			on FK_brewery_id = PK_brewery_id
			inner join country_DIM
			on FK_country_id = PK_country_id
			where
				country_name = 'United States'
			group by brewery_name
			having 
				count(PK_beer_id) > 100
				and avg(avg_score) > 4.2
		) sub
	)
group by 
	brewery_name
	,year(date)
order by year_added


