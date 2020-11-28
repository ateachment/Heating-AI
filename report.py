import settings
from fritzbox.Fritzbox import Fritzbox

import time
import datetime
import os  

SEPERATOR = " "


def main():
    wlanAccessPoint = Fritzbox(settings.IP_ADDRESS, settings.PASSWORD) 
    dt = datetime.datetime.now()
    numResidentsAtHome = wlanAccessPoint.getNumberActiveMacs(settings.MACS)

    print(numResidentsAtHome, dt.isocalendar()[1] % 2, dt.weekday(), int(dt.hour * 60 / settings.CHECK_INTERVAL) + int(dt.minute / settings.CHECK_INTERVAL))

    with open(os.path.join(os.path.dirname(__file__),'data', "data.txt"),"a") as file:
        file.write(str(numResidentsAtHome) + SEPERATOR + str(dt.isocalendar()[1] % 2) + SEPERATOR + str(dt.weekday()) + SEPERATOR + str(int(dt.hour * 60 / settings.CHECK_INTERVAL) + int(dt.minute / settings.CHECK_INTERVAL)) + "\n") 
        file.close() 

if __name__ == '__main__':
    main()