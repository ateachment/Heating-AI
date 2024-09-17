# Heating-AI

The project idea is that residential heating is controlled by an AI. 
For example, the heating should be switched on half an hour before the first resident arrives, so that it is already warm at the time of arrival. 
Conversely, the heating could also be lowered half an hour before the last occupant leaves. But this is not realised at the moment. If a resident arrives unexpectedly, the heating is simply switched on.

The training data of the AI are the presences of the persons of the last weeks. Whereby this data are obtained from the WLAN connection data of their devices.

The following data is collected:

2020-12-02 20:00:38,4,0

2020-12-02 20:10:38,3,0

...

At these times 4 or 3 residents are at home, whereby it is a normal weekday (0) and no public holiday (1).

To save energy, the data should be collected with an energy-saving device, such as a Raspberry Pi.

As times change rapidly, the training period should not be too long (perhaps 8-12 weeks).
The training could take place once a day. 
But the best way to proceed is still to be found out.

Data can be collected using an embedded system (e.g. Raspberry Pi). If you can overcome the difficulties of installing tensorflow with numpy and pandas etc, it is possible to make the time-temperature predictions on the same system. If not, the data is stored after collection, so it is easy to transfer this data to another system for prediction. This predicted data can then be transferred via file back to the smaller system to control the heating. You can use cron jobs to do this. Copy settings-template.py to settings.py on both computers and configure it accordingly

Exemplary use in crontabs of Raspberry Pi and another Linux computer

# Heating-AI collect data on RPI every 10 minutes
*/10 * * * *    yourUser    python3 /yourPathTo/Heating-AI/control.py > /var/log/heatingControl.log
# Optionally copy data to webserver directory once a day in the morning
51 5 * * *      yourUser    cp /yourPathTo/Heating-AI/data/numResidentsAtHome.csv /var/www/Heating-AI/data

# In this case the prediction is done once a day on a different Linux machine,
52 5 * * *      yourUser    python3 /yourPathTo/Heating-AI/prediction.py > /var/log/heatingPrediction.log
# therefore, the predicted data must be uploaded back to the RPI.
57 5 * * *      yourUser    curl --user yourUser:yourPassword -F fileToUpload=@/home/yourUser/Heating-AI/data/prediction.csv https://h.eick-at.de/upload/upload.php

# In this case the uploaded file must be copied back to the data directory.
58 5 * * *      root    cp /var/www/html/downloads/prediction.csv /root/Heating-AI/data/
# Finally, the thermostat can be programmed.
59 5 * * *      root    python3 /root/Heating-AI/program.py > /var/log/heatingProgram.log





