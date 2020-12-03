import report
from apis.Thermostat import Thermostat


def controlHeating():
    if report.report() > 0:
        thermostat1 = Thermostat()
        thermostat1.temperature(22.0)



    
if __name__ == '__main__':
    controlHeating()
    
    