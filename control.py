import report
from apis.Thermostat import Thermostat


def controlHeating():
    if report.report() > 0:
        thermostat1 = Thermostat()
        thermostat1.set_mode(auto_mode=0)  # manual mode
        thermostat1.temperature(22.0)
    else:
        thermostat1.set_mode(auto_mode=1)  # auto mode on


    
if __name__ == '__main__':
    controlHeating()
    
    