#functions to convet data to different time periods
def convert_fifteenminutes(data):
    fifteen_data = {}    
    times = []
    for time in data:
        if "00" in time or "30" in time or ":15" in time or "45" in time:
            times.append(time)
    times.pop(len(times)-1)
    highs, lows, ends, opens, volume = [],[],[],[],0
    for time in data:
        opens.append(data[time][0])
        ends.append(data[time][1])
        highs.append(data[time][2])
        lows.append(data[time][3])
        volume += data[time][4]
        if time in times:
            if len(opens) == 1:
                pass
            else:
                fifteen_data[time] = [opens[0], ends[-1], max(highs), min(lows), volume]
            highs, lows, ends, opens, volume = [],[],[],[],0
    
    return fifteen_data

def convert_thirtyminutes(data):
    thirty_data = {}    
    times = []
    for time in data:
        if "00" in time or "30" in time:
            times.append(time)
    times.pop(len(times)-1)
    highs, lows, ends, opens, volume = [],[],[],[],0
    for time in data:
        opens.append(data[time][0])
        ends.append(data[time][1])
        highs.append(data[time][2])
        lows.append(data[time][3])
        volume += data[time][4]
        if time in times:
            if len(opens) == 1:
                pass
            else:
                thirty_data[time] = [opens[0], ends[-1], max(highs), min(lows), volume]
            highs, lows, ends, opens, volume = [],[],[],[],0
    
    return thirty_data    
def convert_hour(data):
    hourly_data = {}    
    times = []
    for time in data:
        if "30" in time:
            times.append(time)
    highs, lows, ends, opens, volume = [],[],[],[],0
    for time in data:
        opens.append(data[time][0])
        ends.append(data[time][1])
        highs.append(data[time][2])
        lows.append(data[time][3])
        volume += data[time][4]
        if time in times:
            if len(opens) == 1:
                pass
            else:
                hourly_data[time] = [opens[0], ends[-1], max(highs), min(lows), volume]
            highs, lows, ends, opens, volume = [],[],[],[],0
    
    return hourly_data
def grabb_last_data(data, start, stop): 
    data_ = {}
    for j in range(start, stop):
       data_[list(data.keys())[j]] = data[list(data.keys())[j]]   
    return data_
