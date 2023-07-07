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
    date = OPTIONS.index(variable.get())

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
    tk.minsize(600 , 450)  # минимальные размеры: ширина - 200, высота - 150
    tk.maxsize(1440, 1024)  # максимальные размеры: ширина - 400, высота - 300

    variable = StringVar(tk)
    variable.set(OPTIONS[0])  # default value

    w = OptionMenu(tk, variable, *OPTIONS)
    w.pack()
    button = Button(tk, text="OK", command=api)
    button.pack()
    label_tavg = ttk.Label()
    label_tavg.pack()

    label_tmin = ttk.Label()
    label_tmin.pack()


    canv = Canvas(tk, width=500, height=500, bg='white')
    canv.grid(row=2, column=3)

    # ✅ changed the image to .png
    img = PhotoImage(file="./tavg.png")

    canv.create_image(0, 0, anchor=NW, image=img)
    tk.mainloop()





"""
    
    
    print(tavg)
    print(tmin)
    print(min(tmin))
    
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('index.html')


    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
"""
