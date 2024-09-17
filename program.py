# get prediction in the morning and program thermostat auto mode

import autoModeUtil
from apis.Thermostat import Thermostat

times, targetTemps = autoModeUtil.readPrediction()
# program auto mode of thermostat
weekday = autoModeUtil.programAutoMode(times, targetTemps)
print(weekday)

thermostat1 = Thermostat()
thermostat1.programAutoMode(weekday)

