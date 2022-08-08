SELECT TOP(5) 
beer.beer_name,
brewery_DIM.brewery_name,
country_DIM.country_name,
MAX(beer.who_want) AS ppl_who_want_beer
FROM beer
INNER JOIN style_DIM
ON BEER.FK_style_id = style_DIM.PK_style_id
INNER JOIN brewery_DIM
ON beer.FK_brewery_id = brewery_DIM.PK_brewery_id
INNER JOIN country_DIM
ON brewery_DIM.FK_country_id = country_DIM.PK_country_id
WHERE country_DIM.country_name = 'United States'
GROUP BY beer.beer_name,
brewery_DIM.brewery_name,
country_DIM.country_name
ORDER BY ppl_who_want_beer DESC
