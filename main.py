import http.client
import json
import os
from dotenv import load_dotenv, find_dotenv


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    conn = http.client.HTTPSConnection("meteostat.p.rapidapi.com")

    headers = {
        #place to .env
        'X-RapidAPI-Key': os.environ.get("X-RapidAPI-Key"),
        'X-RapidAPI-Host': "meteostat.p.rapidapi.com"
    }

    conn.request("GET", "/stations/daily?station=10637&start=2020-01-01&end=2020-01-31", headers=headers)

    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode('utf-8'))
    print(json_data)
    tavg = []
    tmin = []
    for i in range(0,31):
        tavg.append(json_data['data'][i]['tavg'])
        tmin.append(json_data['data'][i]['tmin'])
    print(tavg)
    print(tmin)
    print(min(tmin))

