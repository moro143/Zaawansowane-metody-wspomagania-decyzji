import PySimpleGUI as sg
import csv
import main
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import pickle
import placeGUI

def num_to_time(num):
    hour = str(int(num//1))
    minutes = str(int(((num%1)*60)//1))
    if len(hour)==1:
        hour = '0'+hour
    if len(minutes)==1:
        minutes = '0'+minutes
    return hour+':'+minutes

def solutions(solutions, wagi, start, routes):
    layout = []
    Z = [x for _,x in sorted(zip(wagi,solutions), reverse = True)]
    wagi = sorted(wagi, reverse=True)
    c=1
    for _ in Z:
        layout.append([sg.Button(c)])
        c+=1
    c = 0
    while True:
        x = simulation(Z[c][0], start, routes, c, len(Z))
        if x == 'stop':
            break
        if x == 'poprzedni':
            c-=1
        if x == 'nastepny':
            c+=1
        if c<0:
            c = len(Z)-1
        if c>=len(Z):
            c = 0
    """window = sg.Window('Wyniki', layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        c = 1
        for _ in Z:
            if event == str(c):
                print(wagi[c-1])
                simulation(Z[c-1][0], start, routes)
            c+=1"""


def simulation(solution_result, start, routes, c, call):
    t = str(c+1)+'/'+str(call)
    layout = [[sg.Text(t)]]
    t = start
    layout.append([sg.Text('',size=(10,1)), sg.Text(num_to_time(t), size=(10,1)), sg.Text(solution_result[0].name)])
    tmpPlace = solution_result[0]
    for i in solution_result[1:]:
        t += routes.routes[i.name][tmpPlace.name][0]
        tmpPlace = i
        if t<i.otwarcie:
            t=i.otwarcie
        layout.append([sg.Text(num_to_time(t),size=(10,1)), sg.Text(num_to_time(t+i.sredni_czas_w), size=(10,1)), sg.Button(i.name)])
        t+=i.sredni_czas_w
    layout.append([sg.Button('Poprzedni'), sg.Button('Nastepny')])
    window = sg.Window('Wynik', layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            return 'stop'
        for i in solution_result:
            if event == i.name:
                placeGUI.place(i)
        if event == 'Poprzedni':
            window.close()
            return 'poprzedni'
        if event == 'Nastepny':
            window.close()
            return 'nastepny'
        
