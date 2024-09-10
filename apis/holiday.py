import json
import urllib.request
import datetime
from datetime import date


'''
checks  if holiday 
            return 1
        else 
            return 0
'''
def getHoliday(dt: datetime, germanStateCode: str):
    year = dt.year
    source_url = f"https://feiertage-api.de/api/?jahr={year}&nur_land={germanStateCode}"
    with urllib.request.urlopen(source_url) as url:
        data: str = json.loads(url.read().decode())

    # print(json.dumps(data, indent = 4, sort_keys=True))

    for holiday in data:         # iterate
        if data[holiday]['datum'] == dt.isoformat():
            return 1


    source_url = f"https://ferien-api.de/api/v1/holidays/{germanStateCode}"
    # HTTP Error 403: Forbidden is returned if a valid user agent is not used to prevent bots from scraping data.
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
    req = urllib.request.Request(source_url, data=None, headers={"User-Agent" :	user_agent})
    with urllib.request.urlopen(req) as response:
        data: str = json.loads(response.read().decode())

    print(json.dumps(data, indent = 4, sort_keys=True))

    for holidays in data:         # iterate
        if holidays['start'] <= dt.isoformat()+"T00:00Z" and holidays['end'] >= dt.isoformat()+"T00:00Z":
            # print(holidays['name'])
            return 1

    return 0



