-- sum of beers in each of analyzed state
select
	state_name
	,count(PK_beer_id) as beers_in_total
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
	and (c.state_name = 'Georgia'
	or c.state_name = 'Michigan')
group by
	state_name
order by
	beers_in_total desc
	,state_name
	

--number of beers in each style, average and max abv in each style
select
	state_name
	,style_name
	,count(PK_beer_id) as beers_in_style
	,round(avg(abv_value), 1) as ave_abv_in_style
	,max(abv_value) as max_abv_in_style
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
	and (c.state_name = 'Georgia'
	or c.state_name = 'Michigan')
group by
	state_name
	,style_name
order by
	state_name
	,beers_in_style desc
	,style_name

--rank of sum from who wants parameter in each style
SELECT
	state_name
	,style_name
	,sum(who_want) AS sum_who_want
FROM beer
INNER JOIN style_DIM
ON beer.FK_style_id = style_DIM.PK_style_id
INNER JOIN brewery_DIM
ON beer.FK_brewery_id = brewery_DIM.PK_brewery_id
INNER JOIN country_DIM
ON brewery_DIM.FK_country_id = country_DIM.PK_country_id
where 
	style_name is not null
	and (state_name = 'Georgia'
	or state_name = 'Michigan')
GROUP BY state_name, style_name
order by state_name, sum_who_want desc



