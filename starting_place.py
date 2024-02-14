import csv
import json
import pickle
import urllib.parse

import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
import requests

import GUI
import main


def get_route(lon1, lat1, lon2, lat2):
    link = (
        "http://router.project-osrm.org/route/v1/foot/"
        + str(lon1)
        + ","
        + str(lat1)
        + ";"
        + str(lon2)
        + ","
        + str(lat2)
    )
    response = requests.get(link).json()
    return response


places = []
places_name = {}
with open("places.csv") as file:
    csv_reader = csv.reader(file, delimiter=";")
    for i in csv_reader:
        x = main.Place(
            str(i[0]),
            float(i[4]),
            float(i[5]),
            float(i[6]),
            float(i[3]),
            i[7],
            i[8],
            categories=main.get_categories(i[2]),
            price=float(i[1]),
            popularity=int(i[9]),
        )
        places_name[x.name] = x
        places.append(x)
dbfile = open("routes", "rb")
db = pickle.load(dbfile)
dbfile.close()

layout = [
    # [sg.Text('Szerokosc geograficzna:', size=(20, 1)), sg.InputText('48.83317293971395',key='lan')],
    # [sg.Text('Dlugosc geograficzna:', size=(20, 1)), sg.InputText('2.3246822191145866', key='lat')],
    [
        sg.Text("Miejsce rozpoczecia podrozy:", size=(22, 1)),
        sg.InputText("Hôtel Malte - Astotel", key="address"),
    ],
    [sg.Text("Godzina rozpoczecia:", size=(22, 1)), sg.InputText("11", key="start")],
    [sg.Text("Godzina zakonczenia:", size=(22, 1)), sg.InputText("21", key="koniec")],
    [sg.Button("Gotowe")],
]

window = sg.Window("Wybor miejsca poczatkowego", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Gotowe":
        # lan = float(values['lan'])
        # lat = float(values['lat'])
        address = values["address"]
        url = (
            "https://nominatim.openstreetmap.org/search?q="
            + urllib.parse.quote(address)
            + "&format=json"
        )
        print(url)
        response = requests.get(url).json()
        lan = response[0]["lat"]
        lat = response[0]["lon"]
        response = requests.get(url).json()
        start = float(values["start"])
        koniec = float(values["koniec"])
        place = main.Place("Start", 0, 0, 24, 0, lan, lat)
        places.append(place)
        routes = main.Routes(places)
        for i in db:
            routes.add_route(places_name[i[0]], places_name[i[1]], i[2], 10)
        c = 0
        for i in places:
            print(c / len(places) * 100)
            c += 1
            routes.add_route(
                place,
                i,
                float(
                    get_route(place.lat, place.lan, i.lat, i.lan)["routes"][0][
                        "distance"
                    ]
                )
                / 5
                / 1000,
                10,
            )
        GUI.guiCategories(places, routes, start, koniec)
