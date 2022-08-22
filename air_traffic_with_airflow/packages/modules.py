import datetime
import pandas as pd

def get_date():
    current_time = datetime.datetime.now()
    past_time = current_time - datetime.timedelta(hours=1)
    unix_current_timestamp = round(datetime.datetime.timestamp(current_time))
    unix_past_timestamp = round(datetime.datetime.timestamp(past_time))
    print(f'past time: {unix_past_timestamp}')
    print(f'current time: {unix_current_timestamp}')


def clean_data():
    df = pd.read_csv("zone1_20220822T124500.txt", delimiter=',', header=None)
    df = df.drop(columns=[8, 12, 15, 16, 17], axis=1)
    # df.columns = ['']
    return df


if __name__ == "__main__":
    clean_data()
