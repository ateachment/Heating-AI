import json
import broadlink  # pip install broadlink - https://github.com/mjg59/python-broadlink

# instructions refer to
# https://github.com/mjg59/python-broadlink/blob/master/broadlink/climate.py

class Thermostat:
    def __init__(self): 
        # discover thermostat in WLAN

        device = broadlink.hysen(('192.168.178.9',80),'780F77D422D7',0x4ead)  
        device.auth()
        self.__thermostat = device

        ''' # does not work anymore with python 3.8 ???
        devices = broadlink.discover(timeout=5)
        print("Found " + str(len(devices)) + " broadlink devices")
        if(len(devices) > 0):
            devices[0].auth()
            self.__thermostat = devices[0]
        '''
    
    def getFullStatus(self):
        return self.__thermostat.get_full_status()

    def temperature(self, temp):
    
        # print(self.__thermostat.get_type()) # Hysen heating controller


        # print('Device: ' + self.__thermostat.type)

        # read the complete status :
        # data = self.__thermostat.get_full_status()

        self.__thermostat.set_temp(temp)
        return self.__thermostat.get_temp()

    def getActualTemp(self):
        return self.__thermostat.get_temp()


    # Abuse of osv (Maximum floor temperature -> normally turns off underfloor heating to protect parquet adhesive).
    # Is not in use here. But memory is needed in thermostat to store current manually set temperature.
    def getManualTemp(self):
        jsonLoad = json.loads(json.dumps(self.getFullStatus()))
        manualTemp = jsonLoad['osv']                    # misuse of osv
        return manualTemp

    def set_mode(self, auto_mode: int = 0, loop_mode: int = 2):
        # Change controller mode
        # auto_mode = 1 for auto (scheduled/timed) mode, 0 for manual mode.
        # Manual mode will activate last used temperature.
        # In typical usage call set_temp to activate manual control and set temp.
        # loop_mode refers to index in [ "12345,67", "123456,7", "1234567" ]
        # E.g. loop_mode = 0 ("12345,67") means Saturday and Sunday follow the "weekend" schedule
        # loop_mode = 2 ("1234567") means every day (including Saturday and Sunday) follows the "weekday" schedule
        self.__thermostat.set_mode(auto_mode, loop_mode)


    def programAutoMode(self, weekday):
        self.set_mode() #loop mode '1234567'
        # set times/temps for auto mode
        # weekday = [{'start_hour':6, 'start_minute':00, 'temp': 22 },{'start_hour':7, 'start_minute':00, 'temp': 16 },{'start_hour':12, 'start_minute':30, 'temp': 22 },{'start_hour':14, 'start_minute':00, 'temp': 20 },{'start_hour':15, 'start_minute':00, 'temp': 22 },{'start_hour':22, 'start_minute':00, 'temp': 16 }]
        weekend = [{'start_hour':6, 'start_minute':00, 'temp': 22 },{'start_hour':22, 'start_minute':00, 'temp': 16 }] # not needed because of loop mode '1234567'
        # print('Test switch to auto mode: ' + str(self.__thermostat.switch_to_auto()) )
        self.__thermostat.set_schedule(weekday, weekend)


if __name__ == '__main__':
    thermostat1 = Thermostat()
    print(thermostat1.getManualTemp())