import json
import broadlink  # pip install broadlink - https://github.com/mjg59/python-broadlink

class Thermostat:
    def __init__(self): 
        # discover thermostat in WLAN
        devices = broadlink.discover(timeout=5)
        # print("Found " + str(len(devices)) + " broadlink devices")
        if(len(devices) > 0):
            devices[0].auth()
            self.__thermostat = devices[0]

    def temperature(self, temp):
    
        # print(self.__thermostat.get_type()) # Hysen heating controller


        # print('Device: ' + self.__thermostat.type)
        # print('Current temperature: '+ str(self.__thermostat.get_temp()) + 'C')
        # print('Set temperature: ' + str(self.__thermostat.set_temp(22.0)) )
        # print('Test switch to auto mode: ' + str(self.__thermostat.switch_to_auto()) )


        # set times/temps for auto mode
        # weekday = [{'start_hour':6, 'start_minute':00, 'temp': 22 },{'start_hour':7, 'start_minute':00, 'temp': 16 },{'start_hour':12, 'start_minute':30, 'temp': 22 },{'start_hour':14, 'start_minute':00, 'temp': 20 },{'start_hour':15, 'start_minute':00, 'temp': 22 },{'start_hour':22, 'start_minute':00, 'temp': 16 }]
        # weekend = [{'start_hour':6, 'start_minute':00, 'temp': 22 },{'start_hour':22, 'start_minute':00, 'temp': 16 }]
        # self.__thermostat.set_schedule(weekday, weekend)

        # read the complete status :
        # data = self.__thermostat.get_full_status()

        self.__thermostat.set_temp(temp)
        return self.__thermostat.get_temp()