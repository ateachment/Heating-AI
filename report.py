import settings
from apis.Fritzbox import Fritzbox


from apis import holiday

import time
import datetime
from datetime import date
import os  

SEPERATOR = ","
SPECIAL_FILENAME = "specialDay.csv"
DATA_FILENAME = "numResidentsAtHome.csv"


def main():
    dt = datetime.datetime.now()

    specialDay = "2020-01-01 0"  # in the past with standard day = 0

    if os.path.isfile(os.path.join(os.path.dirname(__file__),'data', SPECIAL_FILENAME)) == False:
        # print("write initial file")
        with open(os.path.join(os.path.dirname(__file__),'data', SPECIAL_FILENAME),"w") as file:
            file.write(specialDay) 
            file.close() 

    with open(os.path.join(os.path.dirname(__file__),'data', SPECIAL_FILENAME),"r") as file:
        # print("read file")
        specialDay=file.read() 
        file.close() 
    
    hday = holiday.getHoliday(dt.date(), settings.COUNTRY_CODE)  # tests: date(2020, 5, 21) date(2018,4,8)

    actualDate = str(dt.date())
    
    if specialDay.split(SEPERATOR)[0] != actualDate:
        # print("write new file")
        specialDay = str(actualDate) + SEPERATOR + str(hday)
        with open(os.path.join(os.path.dirname(__file__),'data', SPECIAL_FILENAME),"w") as file:
            file.write(specialDay)
            file.close() 
    

    # get number of residents at home getting their mac addresses in wlan
    wlanAccessPoint = Fritzbox(settings.IP_ADDRESS, settings.PASSWORD) 
    numResidentsAtHome = wlanAccessPoint.getNumberActiveMacs(settings.MACS)

    # datetime, number residents at home, holiday (1)
    print(dt.replace(microsecond=0), numResidentsAtHome, hday)

    with open(os.path.join(os.path.dirname(__file__),'data', DATA_FILENAME),"a") as file:
        file.write(str(dt.replace(microsecond=0)) + SEPERATOR + str(numResidentsAtHome) + SEPERATOR + str(hday) + "\n") 
        file.close() 

if __name__ == '__main__':
    main()