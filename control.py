import report
from apis.Thermostat import Thermostat


def controlHeating():
    thermostat1 = Thermostat()
    if report.report() > 0:     # someone at home -> set manual temperature
        thermostat1.set_mode(auto_mode=0)  # manual mode
        manualTemp = thermostat1.getManualTemp()
        thermostat1.temperature(manualTemp)
    else:                       # nobody at home -> auto mode (was predicted and programmed in the mornimg)
        thermostat1.set_mode(auto_mode=1)  # auto mode on


    
if __name__ == '__main__':
    controlHeating()
    
    