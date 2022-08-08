SELECT 
country_name,
substyle_name,
rating
FROM
(SELECT
style_DIM.substyle_name,
country_DIM.country_name,
SUM(beer.rating) AS rating,
ROW_NUMBER() OVER(PARTITION BY country_DIM.country_name ORDER BY SUM(beer.rating) DESC) AS row_numbers1
FROM beer
INNER JOIN style_DIM
ON beer.FK_style_id = style_DIM.PK_style_id
INNER JOIN brewery_DIM
ON beer.FK_brewery_id = brewery_DIM.PK_brewery_id
INNER JOIN country_DIM
ON brewery_DIM.FK_country_id = country_DIM.PK_country_id
GROUP BY country_DIM.country_name, style_DIM.substyle_name) sub
WHERE row_numbers1 <= 3 AND rating > 0
ORDER BY country_name, rating DESC