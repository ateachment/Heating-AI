# programs auto mode of thermostat

import settings
import os
import csv

# read file
def readPrediction():    
    times = list()
    targetTemps = list()
    with open(os.path.join(os.path.dirname(__file__),'data', settings.PREDICTION_FILENAME), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=settings.SEPARATOR)
        for row in reader:
            times.append(row[0])
            targetTemps.append(row[2])
    #print(times, targetTemps)
    return times, targetTemps
        
def timePeriod(time, targetTemp):
    timePeriod = {'start_hour': int(time.split(':')[0]), 'start_minute': int(time.split(':')[1]),'temp': int(targetTemp)}
    #print(timePeriod)
    return timePeriod

def programAutoMode(times, targetTemps):
    numTimePeriod = 6
    
    weekday = []
    targetT = -1
    numTimes = len(times)
    for i in range(numTimes):
        # print(i)
        if targetTemps[i] != targetT:
            weekday.append(timePeriod(times[i], targetTemps[i]))
            targetT = targetTemps[i]
            numTimePeriod -= 1
            if numTimePeriod == 0:
                break
    
    while numTimePeriod >= 0:
        # print(numTimePeriod)
        weekday.append(timePeriod(times[numTimes-1], targetT))
        numTimePeriod -= 1
        
    return weekday

       