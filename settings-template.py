# wlan accesspoint
IP_ADDRESS = '192.168.178.1'
PASSWORD = 'yourPW'  # be careful

# Mac addresses of the residents' portable devices, which are always taken along
# some names
MACS=["00:00:00:00:00:00","11:11:11:11:11:11"]

# interval of the check if someone is at home in minutes
CHECK_INTERVAL=10

# identifying special days i.e. holidays 
COUNTRY_CODE ="XX"

# download url of data
# from local file system
DATA_URL = "data/YourDataSource.csv" 
# or public url
# DATA_URL = "https://YourDataSource.csv"

 # dependend on 2 switching thresholds
targetTemps = [18, 20, 22]
# 2 switching thresholds of probability of number residents at home
switchingThresholds = [0.5, 1.0] 

# data filenames (no need to change)
SEPARATOR = ","
PREDICTION_FILENAME = "prediction.csv"
SPECIAL_FILENAME = "specialDay.csv"
DATA_FILENAME = "YourDataSource.csv"
