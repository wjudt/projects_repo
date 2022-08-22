import datetime
import pandas as pd


def get_date():
    current_time = datetime.datetime.now()
    past_time = current_time - datetime.timedelta(hours=1)
    unix_current_timestamp = round(datetime.datetime.timestamp(current_time))
    unix_past_timestamp = round(datetime.datetime.timestamp(past_time))
    print(f'past time: {unix_past_timestamp}')
    print(f'current time: {unix_current_timestamp}')


def unix_time_to_datetime(unix_time):
    dt = datetime.datetime.fromtimestamp(unix_time)
    return dt


def clean_data(path):
    df = pd.read_csv(path, delimiter=',', header=None)
    df = df.drop(columns=17, axis=1)
    df = df.drop(df.tail(1).index)
    df.columns = ['icao24',
                  'callsign',
                  'origin_country',
                  'time_position',
                  'time_last_contact',
                  'longitude_deg',
                  'latitude_deg',
                  'geo_altitude_m',
                  'on_ground',
                  'velocity_m_per_s',
                  'true_track_dec_deg',
                  'vertical_rate_m_per_s',
                  'sensors',
                  'baro_altitude_m',
                  'squawk_code',
                  'spi',
                  'position_source']

    df['icao24'] = df['icao24'].str.split('[').str[-1].str.replace("'", "").str.strip()
    df['callsign'] = df['callsign'].str.replace("'", "").str.strip()
    df['origin_country'] = df['origin_country'].str.replace("'", "").str.strip()
    df['time_position'] = df['time_position'].apply(unix_time_to_datetime)
    df['time_last_contact'] = df['time_last_contact'].apply(unix_time_to_datetime)

    print(df.dtypes)
    return df


if __name__ == "__main__":
    clean_data("zone1_20220822T124500.txt")
