# get prediction in the mornig and program thermostat auto mode

import prediction
import autoModeUtil
from apis.Thermostat import Thermostat

# program auto mode of thermostat
weekday = autoModeUtil.programAutoMode(prediction.times, prediction.targetTemp)
# print(weekday)

thermostat1 = Thermostat()
thermostat1.programAutoMode(weekday)

