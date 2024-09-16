import settings
from apis.Fritzbox import Fritzbox
from apis.Thermostat import Thermostat

from apis import holiday

import time
import datetime
from datetime import date
import os  


'''
Reports date and time with number of residents and if day is public holiday in file
returns present number of residents 
'''
def report():
    hday = -1
    dt = datetime.datetime.now()

    specialDay = "2020-01-01,0"  # in the past with standard day = 0

    if os.path.isfile(os.path.join(os.path.dirname(__file__),'data', settings.SPECIAL_FILENAME)) == False:
        # print("write initial file")
        with open(os.path.join(os.path.dirname(__file__),'data', settings.SPECIAL_FILENAME),"w") as file:
            file.write(specialDay) 
            file.close() 

    with open(os.path.join(os.path.dirname(__file__),'data', settings.SPECIAL_FILENAME),"r") as file:
        # print("read file")
        specialDay=file.read() 
        file.close() 
    
    
    actualDate = str(dt.date())
    
    if specialDay.split(settings.SEPARATOR)[0] != actualDate:
        hday = holiday.getHoliday(dt.date(), settings.COUNTRY_CODE)  # tests: date(2020, 5, 21) date(2018,4,8)
        # print("write new file")
        specialDay = str(actualDate) + settings.SEPARATOR + str(hday)
        with open(os.path.join(os.path.dirname(__file__),'data', settings.SPECIAL_FILENAME),"w") as file:
            file.write(specialDay)
            file.close() 
    else:
        hday = specialDay.split(settings.SEPARATOR)[1]

    
    

    # get number of residents at home getting their mac addresses in wlan
    wlanAccessPoint = Fritzbox(settings.IP_ADDRESS, settings.PASSWORD) 
    numResidentsAtHome = wlanAccessPoint.getNumberActiveMacs(settings.MACS)

    # datetime, number residents at home, holiday (1)
    # print(dt.replace(microsecond=0), numResidentsAtHome, hday)
    
    # get actual temperature for control purposes
    thermostat1 = Thermostat()
    actualTemp = thermostat1.getActualTemp()

    with open(os.path.join(os.path.dirname(__file__),'data', settings.DATA_FILENAME),"a") as file:
        file.write(str(dt.replace(microsecond=0)) + settings.SEPARATOR + str(numResidentsAtHome) + settings.SEPARATOR + str(hday) +  settings.SEPARATOR + str(actualTemp) + "\n") 
        file.close() 
    
    if __name__ == '__main__':
        print("numResidentsAtHome=" + str(numResidentsAtHome))
    return numResidentsAtHome

if __name__ == '__main__':
    report()