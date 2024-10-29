import datetime
import broadlink  # pip install broadlink - https://github.com/mjg59/python-broadlink

# instructions refer to
# https://github.com/mjg59/python-broadlink/blob/master/broadlink/climate.py

class Thermostat:
    def __init__(self): 
        # discover thermostat in WLAN

        device = broadlink.hysen(('192.168.178.9',80),'780F77D422D7',0x4ead)  
        device.auth()
        self.__thermostat = device
        self.__full_status = self.__thermostat.get_full_status()

    def temperature(self, temp):
        self.__thermostat.set_temp(temp)

    def getActualTemp(self):
        return self.__full_status['room_temp']

    # Abuse of osv (Maximum floor temperature -> normally turns off underfloor heating to protect parquet adhesive).
    # Is not in use here. But memory is needed in thermostat to store current manually set temperature.
    def getManualTemp(self):
        return self.__full_status['osv']                    # misuse of osv
    
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

    def correctTime(self):
        now = datetime.datetime.now()
        dayofweek = now.isoweekday()               # number of weekday: monday = 1 .. sunday = 7
        time = now.time()
        hour = time.hour
        minute = time.minute
        second = time.second
        if hour != self.__full_status['hour'] or minute != self.__full_status['min'] or second != self.__full_status['sec'] or dayofweek != self.__full_status['dayofweek']:
            self.__thermostat.set_time(hour, minute, second, dayofweek)
            print("time corrected")


if __name__ == '__main__':
    thermostat1 = Thermostat()
    #print(thermostat1.getManualTemp())
    thermostat1.correctTime()