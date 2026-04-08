# get prediction in the morning and program thermostat auto mode
import datetime
import autoModeUtil
from apis.Thermostat import Thermostat

# get actual time
now = datetime.datetime.now()
# print("Current time:", now)
# get next full half hour
if now.minute < 30:
    next_half_hour = now.replace(minute=30, second=0, microsecond=0)
else:
    next_half_hour = (now + datetime.timedelta(hours=1)).replace(minute=30, second=0, microsecond=0)
print("Next half hour:", next_half_hour)


times, targetTemps = autoModeUtil.readPrediction(next_half_hour)
# program auto mode of thermostat
weekday = autoModeUtil.programAutoMode(times, targetTemps)
print("weekday:", weekday)

thermostat1 = Thermostat()
thermostat1.programAutoMode(weekday)

