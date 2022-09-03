create view main_view as
select origin_country, time_position, longitude_deg, latitude_deg, geo_altitude_m, velocity_m_per_s, squawk_code 
from area1_flat af 