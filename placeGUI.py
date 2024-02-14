import PySimpleGUI as sg

import main


def num_to_time(num):
    hour = str(int(num // 1))
    minutes = str(int(((num % 1) * 60) // 1))
    if len(hour) == 1:
        hour = "0" + hour
    if len(minutes) == 1:
        minutes = "0" + minutes
    return hour + ":" + minutes


def place(place):
    layout = [
        [sg.Text("Name", size=(20, 1)), sg.Text(place.name, size=(20, 1))],
        [
            sg.Text("Attractivness", size=(20, 1)),
            sg.Text(place.atrakcyjnosc, size=(20, 1)),
        ],
        [sg.Text("Price", size=(20, 1)), sg.Text(place.price, size=(20, 1))],
        [
            sg.Text("Time", size=(20, 1)),
            sg.Text(num_to_time(place.sredni_czas_w), size=(20, 1)),
        ],
        [
            sg.Text("Open hour", size=(20, 1)),
            sg.Text(num_to_time(place.otwarcie), size=(20, 1)),
        ],
        [
            sg.Text("Close hour", size=(20, 1)),
            sg.Text(num_to_time(place.zamkniecie), size=(20, 1)),
        ],
        [
            sg.Text("Popularity", size=(20, 1)),
            sg.Text(int(place.popularity), size=(20, 1)),
        ],
        [sg.Listbox(place.categories, size=(40, 10))],
    ]
    window = sg.Window(place.name, layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    pass
