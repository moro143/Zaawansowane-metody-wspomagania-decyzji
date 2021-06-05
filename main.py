import numpy as np

class Pheromone:
    def __init__(self, places, minPheromone, maxPheromone):
        self.trail = {}
        self.places = places
        for p1 in places:
            self.trail[p1.name] = {}
            for p2 in places: 
                self.trail[p1.name][p2.name]=minPheromone
        self.minP = minPheromone
        self.maxP = maxPheromone
    def evaporation(self, er=0.1):
        for i in self.places:
            for j in self.places:
                self.trail[i.name][j.name]*=(1-er)
    def update(self, points, solutions):
        self.evaporation()
        maxPoint = max(points)
        c=0
        for solution in solutions:
            for placeIdx in range(len(solution)-1):
                place1 = solution[placeIdx]
                place2 = solution[placeIdx+1]
                pheromone.trail[place1.name][place2.name] += points[c]/maxPoint
            c+=1

class Ant:
    def __init__(self, starting_place, starting_hour=0, ending_hour=0):
        self.current_place = starting_place
        self.places_visited = [starting_place]
        self.starting_hour = starting_hour
        self.ending_hour = ending_hour
        self.current_hour = starting_hour
        self.starting_placeR = starting_place
        self.current_hourR = starting_hour
        
    def step(self, places, routes, pheromone):
        poss = []
        for p in places:
            if p not in self.places_visited:
                godzina_skonczenia = self.current_hour+routes.routes[p.name][self.current_place.name][0]+p.sredni_czas_w
                if p.zamkniecie>godzina_skonczenia and self.ending_hour>godzina_skonczenia:
                    poss.append(p)
        if poss==[]:
            return 
        c = 0
        prob = {}
        prob_list = []
        for i in poss:
            prob[i.name] = pheromone.trail[self.current_place.name][i.name]
            c+=pheromone.trail[self.current_place.name][i.name]
        for i in poss:
            prob_list.append(prob[i.name]/c)
        #print(prob_list)
        choice = np.random.choice(poss, p=prob_list)
        self.current_hour+=choice.sredni_czas_w
        self.current_hour+=routes.routes[choice.name][self.current_place.name][0]
        self.current_place = choice
        self.places_visited.append(choice)
    
    def simulation(self, places, routes, pheromone):
        #print(places)
        for _ in places:
            self.step(places, routes, pheromone)
        return self.places_visited
    
    def simulationPointsAtrakcyjnosc(self, places, routes, pheromone):
        places_visited = self.simulation(places, routes, pheromone)
        point = 0
        for place in places_visited:
            point+=place.atrakcyjnosc
        return places_visited, point
    
    def reset(self):
        self.current_place = self.starting_placeR
        self.places_visited = [self.starting_placeR]
        self.current_hour = self.current_hourR


class Place:
    def __init__(self, name, atrakcyjnosc, otwarcie, zamkniecie, sredni_czas_w=0):
        self.name = name
        self.atrakcyjnosc = atrakcyjnosc
        self.otwarcie = otwarcie
        self.zamkniecie = zamkniecie
        self.sredni_czas_w = sredni_czas_w

class Routes:
    def __init__(self, places):
        self.places = places
        self.routes = {}
        for i in places:
            self.routes[i.name]={}
    def add_route(self, place1, place2, time, distance):
        self.routes[place1.name][place2.name]=[time,distance]
        self.routes[place2.name][place1.name]=[time,distance]

class Colony:
    def __init__(self, nbAnts, starting_place, starting_hour=0, ending_hour=24):
        self.colony = []
        self.starting_place = starting_place
        self.starting_hour = starting_hour
        self.ending_hour = ending_hour
        self.nbAnts = nbAnts
        for _ in range(nbAnts):
            self.colony.append(Ant(starting_place, starting_hour, ending_hour))
    def simulation(self, places, routes, pheromone):
        placesAnts = []
        pointAnts = []
        for ant in self.colony:
            placesAnt, pointAnt = ant.simulationPointsAtrakcyjnosc(places, routes, pheromone)
            placesAnts.append(placesAnt)
            pointAnts.append(pointAnt)
        self.colony = []
        for _ in range(self.nbAnts):
            self.colony.append(Ant(self.starting_place, self.starting_hour, self.ending_hour))
        return placesAnts, pointAnts

p1 = Place('dom', 0, 0, 24, 0)
p2 = Place('krzysiu', 7, 0, 24, 2)
p3 = Place('pawel', 7, 0, 24, 2)
p4 = Place('piatak', 9, 16, 24, 2)
p5 = Place('kino', 6, 9, 22, 3)
p6 = Place('baseny', 8, 9, 20, 3)
p7 = Place('zoo', 7, 9, 20, 6)

r = Routes([p1,p2,p3,p4,p5,p6,p7])

r.add_route(p1,p2,0.75,2)
r.add_route(p1,p3,0.75,2)
r.add_route(p1,p4,0.45,2)
r.add_route(p1,p5,0.45,2)
r.add_route(p1,p6,1,2)
r.add_route(p1,p7,0.75,2)

r.add_route(p2,p3,0,2)
r.add_route(p2,p4,0.45,2)
r.add_route(p2,p5,0.47,2)
r.add_route(p2,p6,0.45,2)
r.add_route(p2,p7,0.6,2)

r.add_route(p3,p4,0.4,2)
r.add_route(p3,p5,0.47,2)
r.add_route(p3,p6,0.35,2)
r.add_route(p3,p7,0.63,2)

r.add_route(p4,p5,0.35,2)
r.add_route(p4,p6,0.57,2)
r.add_route(p4,p7,0.57,2)

r.add_route(p5,p6,0.73,2)
r.add_route(p5,p7,0.28,2)

r.add_route(p6,p7,1,2)

places = [p1, p2, p3, p4, p5, p6, p7]
routes = r
pheromone = Pheromone([p1,p2,p3,p4,p5, p6, p7],1,10)
colony = Colony(100, p1, 13, 20)

all = []
c=0
for _ in range(100):
    #colony = Colony(100, p1, 13, 20)
    solutions, points = colony.simulation(places, routes, pheromone)
    print(points.count(max(points)))
    all_one = []
    for solution in solutions:
        all_one_ant = []
        for place in solution:
            all_one_ant.append(place.name)
        all_one.append(all_one_ant)
    pheromone.update(points, solutions)
    all.append(all_one)
    c+=1 
print(all[0]==all[-1])