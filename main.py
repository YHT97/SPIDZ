import http.client
import json
import os

from PIL import ImageTk,Image
from dotenv import load_dotenv, find_dotenv
from jinja2 import FileSystemLoader, Environment, select_autoescape
from matplotlib import pyplot as pp
from tkinter import *
from tkinter import ttk

OPTIONS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
]


def api():
    date = OPTIONS.index(date_day.get())

    if (date + 1) // 10 == 0:
        date = "0" + str(date + 1)
    else:
        date = str(date + 1)
    print(date)

    conn.request("GET", "/stations/daily?station=10637&start=2022-"+date+"-01&end=2022-"+date+"-31", headers=headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode('utf-8'))
    print(json_data)
    tavg = []
    tmin = []
    for i in range(0, 31):
        tavg.append(json_data['data'][i]['tavg'])
        tmin.append(json_data['data'][i]['tmin'])
    label_tavg["text"] = round(sum(tavg) / len(tavg), 2)
    label_tmin["text"] = round(min(tmin), 2)
    pp.plot(tavg)
    pp.savefig("tavg.png")
    pp.show()

    img = PhotoImage(file='tavg.png')
    canv.create_image(0, 0, anchor=NW, image=img)  # TODO:test on another os

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render()

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)





if __name__ == '__main__':
    load_dotenv(find_dotenv())
    conn = http.client.HTTPSConnection("meteostat.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': os.environ.get("X-RapidAPI-Key"),
        'X-RapidAPI-Host': "meteostat.p.rapidapi.com"
    }

    tk = Tk()
    tk.resizable(False, False)
    tk.title("IDZ")
    tk.minsize(800 , 600)  # минимальные размеры: ширина - 200, высота - 150
    tk.maxsize(1440, 1024)  # максимальные размеры: ширина - 400, высота - 300

    date_day = StringVar(tk)
    date_day.set(OPTIONS[0])
    label_select_text = ttk.Label(text="Выберите месяц")
    w = OptionMenu(tk, date_day, *OPTIONS)

    button = Button(tk, text="Enter", command=api)

    label_tavg_text = ttk.Label(text="Средняя температура в месяце")
    label_tavg = ttk.Label(text="???")
    label_tmin_text = ttk.Label(text="Наименьшая температура в месяце")
    label_tmin = ttk.Label(text="???")

    canv = Canvas(tk, width=640, height=480, bg='grey')
    canv.grid(row=2, column=3)

    label_select_text.pack()
    w.pack()
    button.pack()
    label_tavg_text.pack()
    label_tavg.pack()
    label_tmin_text.pack()
    label_tmin.pack()
    canv.pack()
    tk.mainloop()











