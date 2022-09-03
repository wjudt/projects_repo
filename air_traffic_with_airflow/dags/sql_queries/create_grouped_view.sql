create view grouped_view as
select origin_country,
count(origin_country) as plane_counter,
max(velocity_m_per_s) as max_velocity,
round(avg(geo_altitude_m), 0) as avg_altitude,
date_trunc('day', time_position) as day
from main_view mv 
group by origin_country, day