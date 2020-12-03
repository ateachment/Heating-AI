# Heating-AI

The project idea is that residential heating is controlled by an AI. 
For example, the heating should be switched on half an hour before the first resident arrives, so that it is already warm at the time of arrival. Conversely, the heating could also be lowered half an hour before the last occupant leaves.

The training data of the AI are the presences of the persons of the last weeks. Whereby this data are obtained from the WLAN connection data of their devices.

The following data is collected:

2020-12-02 20:00:38,4,0

2020-12-02 20:10:38,3,0

...

At these times 4 or 3 residents are at home, whereby it is a normal weekday (0) and no public holiday (1).

To save energy, the data should be collected with an energy-saving device, such as a Raspberry Pi.

As times change rapidly, the training period should not be too long (perhaps 8-12 weeks).
The training could take place once a week. 
But the best way to proceed is still to be found out.