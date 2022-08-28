delete from area1_flat 
where dag_utc_time_str = TIMESTAMP'2022-08-28 12:30:00.000';


copy area1_flat
from '/some_data/zone1_20220828T123000_clean.csv'
delimiter ',' csv;




