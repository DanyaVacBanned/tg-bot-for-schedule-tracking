import datetime 


start = '10:30'
end = '12:45'

start_time = datetime.datetime.strptime(start, '%H:%M').time()
end_time = datetime.datetime.strptime(end, "%H:%M").time()

def time_in_range(curent_time: datetime.time):
    return start_time <= curent_time <= end_time

curent_time = datetime.datetime.strptime('10:30', '%H:%M').time()
print(time_in_range(curent_time=curent_time))
