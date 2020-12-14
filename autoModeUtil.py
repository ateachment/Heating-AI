# programs auto mode of thermostat

def timePeriod(time, targetTemp):
    timePeriod = {'start_hour': int(time.split(':')[0]), 'start_minute': int(time.split(':')[1]),'temp': targetTemp}
    return timePeriod

def programAutoMode(times, targetTemp):
    numTimePeriod = 6
    
    weekday = []
    targetT = -1
    numTimes = len(times)
    for i in range(numTimes):
        # print(i)
        if targetTemp[i] != targetT:
            weekday.append(timePeriod(times[i], targetTemp[i]))
            targetT = targetTemp[i]
            numTimePeriod -= 1
            if numTimePeriod == 0:
                break
    
    while numTimePeriod >= 0:
        # print(numTimePeriod)
        weekday.append(timePeriod(times[numTimes-1], targetT))
        numTimePeriod -= 1
        
    return weekday

       