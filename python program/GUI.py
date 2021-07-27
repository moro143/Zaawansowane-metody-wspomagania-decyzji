import PySimpleGUI as sg
import csv
import traceback
from PySimpleGUI.PySimpleGUI import ErrorElement
import main
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import pickle
import solutionGUI
import time
from statistics import mean
import AHP_GUI

np.random.seed(453214)

def change(a, i,j, n):
    a[i][j]=n
    a[j][i]=1/n

def pref(a):
    x = np.transpose(a)
    result = []
    for i in x:
        result.append(i/sum(i))
    return np.transpose(result)

def wagi(a):
    result = []
    for i in a:
        result.append(mean(i))
    return result

def is_pareto_efficient(costs, return_mask = True):
    is_efficient = np.arange(costs.shape[0])
    n_points = costs.shape[0]
    next_point_index = 0  # Next index in the is_efficient array to search for
    while next_point_index<len(costs):
        nondominated_point_mask = np.any(costs<costs[next_point_index], axis=1)
        nondominated_point_mask[next_point_index] = True
        is_efficient = is_efficient[nondominated_point_mask]  # Remove dominated points
        costs = costs[nondominated_point_mask]
        next_point_index = np.sum(nondominated_point_mask[:next_point_index])+1
    if return_mask:
        is_efficient_mask = np.zeros(n_points, dtype = bool)
        is_efficient_mask[is_efficient] = True
        return is_efficient_mask
    else:
        return is_efficient


def guiCategories(places, routes, start, koniec):
    categoriesLayout = [[sg.Text('Preferencje kategori atrakcji')]]
    places_name = {}
    for i in places:
        places_name[i.name] = i

    all_categories = []
    for p in places:
        for c in p.categories:
            if c not in all_categories:
                all_categories.append(c)
    for cat in all_categories:
        categoriesLayout.append([sg.Text(cat, size=(20, 1)), sg.Spin(values=('1','2','3','4','5'), initial_value='3', key=cat)])

    categoriesLayout.append([sg.Button('Gotowe')])

    window = sg.Window("Kategorie", categoriesLayout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Gotowe':
            person = main.Person(all_categories)
            for cat in all_categories:
                if float(values[cat])!=0:
                    person.categories_points[cat] = float(values[cat])
                else:
                    person.categories_points[cat] = float(0.1)
            pheromoneAttraction = main.Pheromone(places, 0.01, 50)
            pheromoneCategories = main.Pheromone(places, 0.01, 50)
            pheromonePrice = main.Pheromone(places, 0.01, 50)
            pheromonePopularity = main.Pheromone(places, 0.01, 50)
            pheromone_list = [pheromoneAttraction, pheromoneCategories, pheromonePrice, pheromonePopularity]
            colony = main.Colony(100, places[-1], start, koniec)
            fminlist = np.zeros(len(pheromone_list))
            print(0)
            wykres1 = []
            wykres2 = []
            wykres3 = []
            wykres4 = []
            wykresy = [wykres1, wykres2, wykres3, wykres4]
            try:
                c = 0
                for _ in range(500):
                    c+=1
                    print(c/500*100)
                    solutions, points = colony.simulationMulti(places, routes, pheromone_list, person)
                    points = np.transpose(points)
                    for p in range(len(points)):
                        idx = np.argmin(points[p])
                        """
                        if p==2:
                            wykresy[p].append(points[p][idx])
                        else:
                            wykresy[p].append(1/points[p][idx])"""
                        fminlist[p] = pheromone_list[p].update(points[p][idx], solutions[idx], fminlist[p])
                    """plt.plot(wykres1)
                    plt.savefig('1.png')
                    plt.clf()
                    plt.plot(wykres2)
                    plt.savefig('2.png')
                    plt.clf()
                    plt.plot(wykres3)
                    plt.savefig('3.png')
                    plt.clf()
                    plt.plot(wykres4)
                    plt.savefig('4.png')
                    plt.clf()"""
            except:
                traceback.print_exc()
                pass
            print(1)
            points = np.transpose(points)
            a = is_pareto_efficient(points)
            c=0
            results = []
            for solution_result in solutions:
                if a[c]:
                    results.append([solution_result, points[c]])
                c+=1
            a = AHP_GUI.ahp(pheromone_list)
            """
            a = np.ones([len(pheromone_list),len(pheromone_list)])
            change(a, 0, 1, 1/4)
            change(a, 0, 2, 7)
            change(a, 1, 2, 9)
            """
            a = pref(a)
            a = wagi(a)
            points_ = []
            for i in range(len(results[0][1])):
                tmp = []
                for j in results:
                    tmp.append(j[1][i])
                points_.append(np.array(tmp))
            x = []
            for i in points_:
                x.append(i-max(i))
            points_ = x
            r = []
            for i in points_:
                r.append(i/sum(i))
            #r = np.transpose(r)
            wagicalosc = []
            for i in range(len(r[0])):
                tmp = 0
                for j in range(len(a)):
                    x = r[j][i]
                    tmp+=(a[j]*x)
                wagicalosc.append(tmp)
            solutionGUI.solutions(results, wagicalosc, start, routes)
            