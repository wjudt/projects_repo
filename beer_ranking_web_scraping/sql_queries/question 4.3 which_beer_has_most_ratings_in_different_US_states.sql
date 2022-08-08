SELECT
	state_name
	,beer_name
	,brewery_name
	,ratings
FROM
	(SELECT
		beer.beer_name,
		brewery_DIM.brewery_name,
		country_DIM.state_name,
		MAX(beer.rating) AS ratings,
		ROW_NUMBER() OVER(PARTITION BY country_DIM.state_name ORDER BY MAX(beer.rating) DESC) AS row_numbers
	FROM beer
	INNER JOIN brewery_DIM
	ON beer.FK_brewery_id = brewery_DIM.PK_brewery_id
	INNER JOIN country_DIM
	ON brewery_DIM.FK_country_id = country_DIM.PK_country_id
	WHERE country_DIM.country_name = 'United States' and state_name IS NOT null
	GROUP BY beer.beer_name, brewery_DIM.brewery_name, country_DIM.state_name) sub
WHERE row_numbers <= 1
ORDER BY state_name, row_numbers