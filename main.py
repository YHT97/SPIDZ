import http.client
import json
import os
from dotenv import load_dotenv, find_dotenv
from jinja2 import FileSystemLoader, Environment, select_autoescape
from matplotlib import pyplot as pp

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    conn = http.client.HTTPSConnection("meteostat.p.rapidapi.com")

    headers = {
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
    for i in range(0, 31):
        tavg.append(json_data['data'][i]['tavg'])
        tmin.append(json_data['data'][i]['tmin'])
    print(tavg)
    print(tmin)
    print(min(tmin))
    pp.plot(tavg)
    pp.savefig("tavg.png")
    pp.show()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('index.html')

    rendered_page = template.render(
        tmin=round(min(tmin), 3),
        tavg=round(sum(tavg) / len(tavg), 3)
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
