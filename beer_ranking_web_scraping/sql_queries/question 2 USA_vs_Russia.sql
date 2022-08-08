-- find most popular beers in usa vs russia
select
	country_name
	,style_name
	,beer_name
	,abv_value
	,rating
from
	(
	select
		country_name
		,style_name
		,beer_name
		,abv_value
		,max(rating) as rating
		,ROW_NUMBER() OVER(PARTITION BY country_name ORDER BY max(rating) DESC) AS row_numbers
	
	from beer b
	inner join brewery_DIM br
	on FK_brewery_id = PK_brewery_id
	inner join country_DIM c
	on FK_country_id = PK_country_id
	left join style_DIM
	on FK_style_id = PK_style_id
	left join abv_DIM a
	on FK_abv_id = PK_abv_id
	where 
		style_name is not null
		and (c.country_name = 'United States'
		or c.country_name = 'Russian Federation')
	group by
		country_name
		,style_name
		,beer_name
		,abv_value
	) sub
where sub.row_numbers <= 5
