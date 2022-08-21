import datetime

current_time = datetime.datetime.now()
past_time = current_time - datetime.timedelta(hours=1)
unix_current_timestamp = round(datetime.datetime.timestamp(current_time))
unix_past_timestamp = round(datetime.datetime.timestamp(past_time))
print(f'past time: {unix_past_timestamp}')
print(f'current time: {unix_current_timestamp}')
