import requests
import json
import main
import csv
import pickle

def get_route(lon1, lat1, lon2, lat2):
    link = "http://router.project-osrm.org/route/v1/foot/"+str(lon1)+','+str(lat1)+';'+str(lon2)+','+str(lat2)
    print(link)
    response = requests.get(link).json()
    return response

places = []
with open('places.csv') as file:
    csv_reader = csv.reader(file, delimiter=';')
    for i in csv_reader:
        x = main.Place(str(i[0]), float(i[4]), float(i[5]), float(i[6]), float(i[3]), i[7],i[8])
        places.append(x)

routes = main.Routes(places)


lista = []
for pi in range(len(places)-1):
    for pj in range(pi,len(places)):
        i = places[pi]
        j = places[pj]
        print(places[pi].name, places[pj].name)
        lista.append([places[pi].name, places[pj].name, float(get_route(i.lat,i.lan,j.lat,j.lan)['routes'][0]['distance'])/5/1000])
        

print(lista)
dbfile = open('routes', 'ab')
pickle.dump(lista, dbfile)
dbfile.close()