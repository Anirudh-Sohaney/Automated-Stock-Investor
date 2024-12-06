import datamanager
def find_pattern(data):
    data = list(data.values())
    first, second, third = data
    
    #engulfing
    if (second[0] <= third[1]) and (second[1] >= third[0]) and (third[1] > third[0]) and (second[0] > second[1]) and not (third[0] == second[1] and third[1]==second[0]):
        strength = 70
        size_strength =((third[1]-third[0]) / (second[0] - second[1])) * 9
        shadow_strength=( (third[2] - third[1])/ third[1]) + ((third[0] - third[3]) / third[1]) + ((second[2] - second[0]) / second[2]) + ((second[1] - second[3]) / second[2])
        strength -= (size_strength + (shadow_strength*20))
        
        return "engulf", strength   
    #harami 
    elif (third[0] < third[1]) and (second[1] < second[0]) and (third[0] > second[1]) and (third[1] < second[0]) and (third[1] > second[1]):
        strength = 70
        score1 = ((third[1] - third[0]) / (second[0] - second[1]) * 10)
        return "harami" , (strength - score1)
    
    #piercing line
    elif (third[1] > third[0]) and (second[1] > second[1]) and (abs(1 - ((second[0] - second[1]) / (third[1] - third[0]))) < 0.3) and (third[1] > second[0]):
        strength = 80
        score1 = (abs(third[1] - (second[1] + ((second[0] - second[1]) * 0.5)))) * 10
        return "piercing line" , (strength - score1)
    #three inside up
    elif (first[0] > first[1]) and (second[0] < second[1]) and (third[0] < third[1]) and (second[0] > first[1]) and (second[1] < first[0]) and (third[0] > first[1]) and (third[1] > first[0]):
        strength = 80
        score1 = (100/(first[0] - first[1])) / 2
        score2 = ((second[1] - second[0])/100) * 10
        return "three inside up", (strength - (score1 + score2))
    
    #three white soliders
    elif (second[0] > first[0]) and (second[1] > first[1]) and (third[0] > second[0]) and (third[1] > second[1]) and (first[1] > first[0]) and (second[1] > second[0]) and (third[1] > third[0]):
        strength = 75
        score1 = 0
        score2 = 0
        if second[0] < first[1]:
            score1 = ((first[1] - second[0]) / first[1]) * 40
        if third[0] < second[1]:
            score2 = ((second[1] - third[0]) / second[1]) * 40
        strength -= (score1 + score2)
        return "three white soldiers", strength
    
    #morning star
    elif (first[1] < first[0]) and (third[0] < third[1]) and (max([second[1], second[0]]) < (third[0] + ((third[1] - third[0]) *0.05))) and (max([second[1], second[0]])< (first[1] + ((third[1] - third[0]) *0.05))):
        midmin = min([second[0], second[1]])
        strength = 80
        mainbody = third[1] - third[0]
        midmax = max([second[0], second[1]])
        score1 = 0
        score2 = 0
        if midmax > third[0]:
            score1 = (midmax - third[0])/ mainbody
            score1 = score1*10
        if midmax > first[1]:
            score2 = (midmax - first[1])/mainbody
            score2 = score2*10
        score3 = ((midmax- midmin) / (third[1] - third[0])) * 10
        score4 = ((midmax-midmin)  / (first[0] - first[1])) * 10
        strength = strength - (score1 + score2 + score3 + score4)
        return "morning star", strength
    
    #Hammer
    elif (third[0] < third[1]) and ((third[0] - third[3]) > (third[2]-third[1])) and ((third[0] - third[3]) > (third[1] - third[0])):
        strength = 70
        mainbody = third[1] - third[0]
        lowershadow = third[3] - third[0]
        uppershadow = third[2] - third[1]
        full = third[2] - third[0]
        score1 = (mainbody/full) * 8
        score2 = (uppershadow/full) *20
        score3 = (uppershadow/lowershadow) * 5
        return "hammer", (strength - (score1 + score2 + score3))
    else:
        return 0,0
    

def predict_stock_movement(data):
    #converting data to analyze pattern in different time ranges
    hourly_data = datamanager.convert_hour(data)
    thirty_data = datamanager.convert_thirtyminutes(data)
    fifteen_data = datamanager.convert_fifteenminutes(data)
    accuracy = 0
    if len(list(hourly_data.keys()))  < 3:
        hourly_data = {
            "0" : [0,0,0,0,0],
            list(hourly_data.keys())[0] : hourly_data[list(hourly_data.keys())[0]],
            list(hourly_data.keys())[1] : hourly_data[list(hourly_data.keys())[1]]
        }
    #grabbing patterns of previous 6 data points.
    _1, acc1a = find_pattern(datamanager.grabb_last_data(hourly_data, len(list(hourly_data.keys())) - 3, len(list(hourly_data.keys()))))
    _2, acc2a = find_pattern(datamanager.grabb_last_data(thirty_data, len(list(thirty_data.keys())) - 3, len(list(thirty_data.keys()))))
    _3, acc3a = find_pattern(datamanager.grabb_last_data(fifteen_data, len(list(fifteen_data.keys())) - 3, len(list(fifteen_data.keys()))))
    _4, acc1b = find_pattern(datamanager.grabb_last_data(hourly_data, len(list(hourly_data.keys())) - 6, len(list(hourly_data.keys()))-3))
    _5, acc2b = find_pattern(datamanager.grabb_last_data(thirty_data, len(list(thirty_data.keys())) - 6, len(list(thirty_data.keys()))-3))
    _6, acc3b = find_pattern(datamanager.grabb_last_data(fifteen_data, len(list(fifteen_data.keys())) - 6, len(list(fifteen_data.keys()))-3))
    _7, acc4a = find_pattern(datamanager.grabb_last_data(data, len(list(data.keys())) - 3, len(list(data.keys()))))
    _8, acc4b = find_pattern(datamanager.grabb_last_data(data, len(list(data.keys())) - 6, len(list(data.keys()))-3))
    #determining volume strength for pattern prediction  accuracy
    #five minute strength
    volumes = []
    for value in data:
        volumes.append(data[value][4])
    avg_volume = sum(volumes[-10:])/len(volumes[-10:])
    five_min_volume_strength = (sum(volumes[-5:])/len(volumes[-5:]))/avg_volume
    #15 minute strength
    volumes = []
    for value in fifteen_data:
        volumes.append(fifteen_data[value][4])
    avg_volume = sum(volumes[-10:])/len(volumes[-10:])
    fifteen_min_volume_strength = (sum(volumes[-5:])/len(volumes[-5:]))/avg_volume
    #30 minute strength
    volumes = []
    for value in thirty_data:
        volumes.append(thirty_data[value][4])
    avg_volume = sum(volumes[-10:])/len(volumes[-10:])
    thirty_min_data_strength = (sum(volumes[-5:])/len(volumes[-5:]))/avg_volume
    #60 minute strength
    volumes = []
    for value in hourly_data:
        volumes.append(hourly_data[value][4])
    avg_volume = sum(volumes[-10:])/len(volumes[-10:])
    hourly_volume_stregth = (sum(volumes[-5:])/len(volumes[-5:]))/avg_volume
    divident = 2.8
    predictions= [_1, _2, _3, _4, _5, _6, _7, _8]
    while 0 in predictions:
        predictions.remove(0)
    #analyzing pattern strength based on pattern occurences.
    if _7 != 0 or _3 != 0:
        if _8 != 0:
            accuracy += (acc4b*five_min_volume_strength)
            if _7 != 0:
                divident -= 0.7
                accuracy += (acc4a*five_min_volume_strength)
        if _1 != 0:
            accuracy += (acc1a*hourly_volume_stregth)
            if _4 != 0:
                accuracy += (acc1b * hourly_volume_stregth)
                divident -= 0.7
        if _2 != 0:
            accuracy += (acc2a*thirty_min_data_strength)
            if _5 != 0:
                accuracy += (acc2b*thirty_min_data_strength)
                divident -= 0.7
        if _3 != 0:
            accuracy += (acc3a*fifteen_min_volume_strength)
            if _6 != 0:
                accuracy += (acc3b*fifteen_min_volume_strength)
                divident -= 0.7
    if (_1 != 0 and _3 != 0) or (_1 != 0 and _2 != 0) or (_3 != 0 and _2 != 0):
        divident -= 0.09
    volume = 0
    if hourly_volume_stregth > 1:
        volume += 1
    if five_min_volume_strength > 1:
        volume += 1
    if fifteen_min_volume_strength > 1:
        volume += 1
    if thirty_min_data_strength > 1:
        volume += 1
    volume_signs = ["Bad volume", "Poor volume", "Decent volume", "Good volume", "Strong volume"]
    return accuracy / divident , predictions, volume_signs[volume]
 
def calculate_investment_percent(data):
    vals = {}
    for stock in data:
        if data[stock][0] > 65:
            vals[stock] = 0.35
            if data[stock][0] > 80:
                vals[stock] = 0.45
                if data[stock][0] > 95:
                    vals[stock] = 0.55
                    if data[stock][0] > 110:
                        vals[stock] = 0.7
                        if data[stock][0] > 130:
                            vals[stock] = 0.75
                            if data[stock][0] > 180:
                                vals[stock] = 0.85
    while sum(vals.values()) > 0.9:
        for stock in vals:
            vals[stock] = vals[stock] / 1.04
    return vals
    