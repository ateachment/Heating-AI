import json
import urllib.request

def getHoliday(year: str, germanCountryCode: str):

    source_url = f"https://feiertage-api.de/api/?jahr={year}&nur_land={germanCountryCode}"
    with urllib.request.urlopen(source_url) as url:
        data: str = json.loads(url.read().decode())

    print(json.dumps(data, indent = 4, sort_keys=True))


    for holiday in data:         # iterate
        print (data[holiday]['datum'])


getHoliday("2020", "HE")
