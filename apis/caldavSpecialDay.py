import caldav
from icalendar import Calendar
import codecs

import time
import datetime

def getCaldavSpecialDays(url):
    client = caldav.DAVClient(url=url)

    print(client.report(url))
    principal = client.principal()
    calendars = principal.calendars()
    if len(calendars) > 0:
        calendar = calendars[0]
        results = calendar.date_search(datetime.now(), datetime.now() + timedelta(days=30))   # time span 30 days
        data = []
        for event in results:
            gcal = Calendar.from_ical(event.data)
            for component in gcal.walk():
                if component.name == "VEVENT":            
                    #lines = component.to_ical().splitlines()
                    #print(lines)
                
                    summary = component.get('SUMMARY')
                    dtstart =  str(toLocalDatetime(component.get('DTSTART').dt))
                    dtstartName = ""
                    if(dtstart.find(" ") == -1):  # no time, only date
                        dtstartName = "date"
                    else:
                        dtstartName = "dateTime"

                    duration = ["0 days",""]
                    dtendName = ""
                    durations = component.get('DURATION')
                    #print(summary)
                    if type(durations) == list:  # periodic events are represented by 2 durations?!
                        for d in durations:
                            durationObj = d      # take the last one
                    else:
                        durationObj = durations  # no periodic event
                    if(str(durationObj.dt).find(",") == -1):  # no day, only time
                        duration[1] = str(durationObj.dt)
                        dtendName = "dateTime"
                    else:
                        duration = str(durationObj.dt).split(", ") # has days
                        dtendName = "date"
                    
                    noDays = duration[0].split(" ")[0]
                    noHours = duration[1].split(":")[0]
                    noMinutes = duration[1].split(":")[1]
                    tDelta = timedelta(days=int(noDays), hours=int(noHours), minutes=int(noMinutes))
                    dtend = str(toLocalDatetime(component.get('DTSTART').dt) + tDelta)
                    #print(dtend)
                    
                    event = "{ \"summary\": \"" + summary + "\" , \"start\": { \"" + dtstartName + "\": \"" + dtstart.replace(" ","T") + "\" }, \"end\": { \"" + dtendName + "\": \"" + dtend.replace(" ","T") + "\" } }"
                    #print(event)
                    data.append(json.loads(event))

        #print(data)
        return(json.dumps(data))

def toLocalDatetime(utc_dt):
    if(utc_dt.strftime("%H:%M:%S") != "00:00:00"): # get only local time, if DTSTART is not beginning of a whole day     
        dt = datetime.fromtimestamp(cal.timegm(utc_dt.timetuple()))
        return dt
    else:
        return utc_dt

getCaldavSpecialDays("https://start.schulportal.hessen.de/kalender.php?a=ical&i=6273&export=ical&t=bb206dd30fc709060d55f113668f609fcf50d7f99b9a3a94fe884d605bf5230dc6daf774eac7d24d5285eb34e5cd968271faf28bf61f1da6a94869e2ccc46572")