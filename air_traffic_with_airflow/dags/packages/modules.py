import datetime
import pandas as pd


def unix_time_to_datetime(unix_time):
    try:
        dt = datetime.datetime.fromtimestamp(int(unix_time))
        return dt
    except ValueError:
        return None
    except TypeError:
        return None


def string_to_boolean(arg):
    try:
        if arg == 'False':
            return False
        elif arg == 'True':
            return True
        elif arg is True:
            return True
        elif arg is False:
            return False
    except ValueError:
        return None


def clean_data(path):
    df = pd.read_csv(path, delimiter=',', header=None, skipinitialspace=True)
    df = df.drop(df.tail(1).index)
    df.columns = ['icao24',
                  'callsign',  # can be none
                  'origin_country',
                  'time_position',  # can be none
                  'time_last_contact',
                  'longitude_deg',  # can be none
                  'latitude_deg',  # can be none
                  'geo_altitude_m',  # can be none
                  'on_ground',  # True or False
                  'velocity_m_per_s',  # can be none
                  'true_track_dec_deg',  # can be none
                  'vertical_rate_m_per_s',  # can be none
                  'sensors',  # can be none
                  'baro_altitude_m',  # can be none
                  'squawk_code',  # can be none
                  'spi',
                  'position_source',   # 0 = ADS-B, 1 = ASTERIX, 2 = MLAT, 3 = FLARM
                  'useless']

    df = df.drop(labels="useless", axis=1)
    df = df.replace('None', None)
    df['icao24'] = df['icao24'].str.split('[').str[-1].str.replace("'", "").str.strip()
    df['callsign'] = df['callsign'].str.replace("'", "").str.strip()
    df['origin_country'] = df['origin_country'].str.replace("'", "").str.strip()
    df['time_position'] = df['time_position'].apply(unix_time_to_datetime)
    df['time_last_contact'] = df['time_last_contact'].apply(unix_time_to_datetime)
    df['squawk_code'] = df['squawk_code'].str.replace("'", "").str.strip()
    df['position_source'] = df['position_source'].str.findall(r'\d+').str[0]
    df['on_ground'] = df['on_ground'].apply(string_to_boolean)
    df['spi'] = df['spi'].apply(string_to_boolean)

    df = df.astype({'longitude_deg': 'float64',
                    'latitude_deg': 'float64',
                    'geo_altitude_m': 'float64',
                    'velocity_m_per_s': 'float64',
                    'true_track_dec_deg': 'float64',
                    'vertical_rate_m_per_s': 'float64',
                    'baro_altitude_m': 'float64',
                    'position_source': 'int64'
                    })

    return df



if __name__ == "__main__":
    df = clean_data("../../tests/example_raw_data_file.csv")
    df.to_parquet('a.parquet')