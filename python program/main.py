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

    def evaporation(self, er=0.01):
        for i in self.places:
            for j in self.places:
                self.trail[i.name][j.name]*=(1-er)

    def update(self, point, solution, fmin=1):
        self.evaporation()
        if point<fmin:
            fmin=point
        dr = 1/(1+point-fmin)
        for placeIdx in range(len(solution)-1):
            place1 = solution[placeIdx]
            place2 = solution[placeIdx+1]
            self.trail[place1.name][place2.name] += dr
        return fmin

    """def update(self, points, solutions, maximize=True):
        self.evaporation()
        minPoint = min(points)-0.01
        maxPoint = max(points)-min(points)
        c=0
        for solution in solutions:
            for placeIdx in range(len(solution)-1):
                place1 = solution[placeIdx]
                place2 = solution[placeIdx+1]
                if maximize:
                    self.trail[place1.name][place2.name] += (points[c]-minPoint)/maxPoint
                else:
                    self.trail[place1.name][place2.name] += -(points[c]-minPoint)/maxPoint+1
            c+=1"""

    def minmax(self):
        for i in self.places:
            for j in self.places:
                if self.trail[i.name][j.name]>self.maxP:
                    self.trail[i.name][j.name]=self.maxP
                elif self.trail[i.name][j.name]<self.minP:
                    self.trail[i.name][j.name]=self.minP

class Ant:
    def __init__(self, starting_place, starting_hour=0, ending_hour=0):
        self.current_place = starting_place
        self.places_visited = [starting_place]
        self.starting_hour = starting_hour
        self.ending_hour = ending_hour
        self.current_hour = starting_hour
        self.starting_placeR = starting_place
        self.current_hourR = starting_hour
        
    def step(self, places, routes, pheromones):
        poss = []
        for p in places:
            if p not in self.places_visited:
                godzina_skonczenia = self.current_hour+routes.routes[p.name][self.current_place.name][0]+p.sredni_czas_w
                if p.zamkniecie>godzina_skonczenia and self.ending_hour>godzina_skonczenia:
                    poss.append(p)
        if poss==[]:
            return True
        pheromone = np.random.choice(pheromones)
        c = 0
        prob = {}
        prob_list = []
        for i in poss:
            prob[i.name] = pheromone.trail[self.current_place.name][i.name]
            c+=pheromone.trail[self.current_place.name][i.name]
        for i in poss:
            prob_list.append(prob[i.name]/c)
        choice = np.random.choice(poss, p=prob_list)
        self.current_hour+=routes.routes[choice.name][self.current_place.name][0]
        if self.current_hour<choice.otwarcie:
            self.current_hour=choice.otwarcie
        self.current_hour+=choice.sredni_czas_w

        self.current_place = choice
        self.places_visited.append(choice)
        return False
    
    def simulation(self, places, routes, pheromones):
        while not self.step(places, routes, pheromones):
            pass
        return self.places_visited
    

    def simulationMulti(self, places, routes, pheromones, person):
        places_visited = self.simulation(places, routes, pheromones)
        points = []
        point = 0
        for place in places_visited:
            point+=place.atrakcyjnosc*place.sredni_czas_w
        points.append(1/point)
        point = 0
        for place in places_visited:
            tmp = []
            for cat in place.categories:
                tmp.append(person.categories_points[cat])
            if tmp!=[]:
                point += max(tmp)*place.sredni_czas_w
        points.append(1/point)
        point = 0
        for place in places_visited:
            tmp=[]
            point += place.price
        points.append(point)
        point = 0
        for place in places_visited:
            point+=place.popularity*place.sredni_czas_w
        points.append(1/point)
        return places_visited, points            

    def reset(self):
        self.current_place = self.starting_placeR
        self.places_visited = [self.starting_placeR]
        self.current_hour = self.current_hourR

class Place:
    def __init__(self, name, atrakcyjnosc, otwarcie, zamkniecie, sredni_czas_w=0, lan=0, lat=0, categories=[], price=0, popularity=0):
        self.name = name
        self.atrakcyjnosc = atrakcyjnosc
        self.otwarcie = otwarcie
        self.zamkniecie = zamkniecie
        self.sredni_czas_w = sredni_czas_w
        self.lan = lan
        self.lat = lat
        self.categories = categories
        self.price = price
        self.popularity = popularity

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

    def simulation(self, places, routes, pheromones, person):
        placesAnts = []
        pointAnts = []
        for ant in self.colony:
            placesAnt, pointAnt = ant.simulationPointsAtrakcyjnosc(places, routes, pheromones)
            placesAnts.append(placesAnt)
            pointAnts.append(pointAnt)
        self.colony = []
        for _ in range(self.nbAnts):
            self.colony.append(Ant(self.starting_place, self.starting_hour, self.ending_hour))
        return placesAnts, pointAnts

    def simulationCategories(self, places, routes, pheromones, person):
        placesAnts = []
        pointAnts = []
        for ant in self.colony:
            placesAnt, pointAnt = ant.simulationPointsCategories(places, routes, pheromones, person)
            placesAnts.append(placesAnt)
            pointAnts.append(pointAnt)
        self.colony = []
        for _ in range(self.nbAnts):
            self.colony.append(Ant(self.starting_place, self.starting_hour, self.ending_hour))
        return placesAnts, pointAnts

    def simulationMulti(self, places, routes, pheromones, person):
        placesAnts = []
        pointsAnts = []
        for ant in self.colony:
            placesAnt, pointsAnt = ant.simulationMulti(places, routes, pheromones, person)
            placesAnts.append(placesAnt)
            pointsAnts.append(pointsAnt)
        self.colony = []
        for _ in range(self.nbAnts):
            self.colony.append(Ant(self.starting_place, self.starting_hour, self.ending_hour))
        return placesAnts, pointsAnts

class Person:
    def __init__(self, categories):
        self.categories = categories
        self.categories_points = {}
        for i in categories:
            self.categories_points[i] = 3

def get_categories(categories):
    return categories.split(',')

