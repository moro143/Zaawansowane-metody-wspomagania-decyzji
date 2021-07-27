import classes
import opt_api_test as opt
import OSRM_API

l = []

_, _, lat, lon = opt.get_place("cieszyn")
print(lat, lon)
for i in opt.get_list(500, lon, lat):
    if i['properties']['name']!="":
        l.append(classes.Place(i['properties']['name'], i['geometry']['coordinates'][0], i['geometry']['coordinates'][1], i['properties']['rate'], None, []))

s = 0
for i in range(len(l)):
    for j in range(len(l)-i-1):
        s+=1

print(s)
r = []
c = 0
for i in range(len(l)):
    for j in range(len(l)-i-1):
        print(int(c/s*100))
        c+=1
        response = OSRM_API.get_route(l[i].lon,l[i].lat, l[len(l)-1-j].lon, l[len(l)-1-j].lat)
        print(response['routes'][0]['duration'])
        r.append( classes.Route( l[i], l[len(l)-1-j], response['routes'][0]['duration'], response['routes'][0]['distance'] ) )

for i in r:
    print(i.place1.name, i.place2.name)