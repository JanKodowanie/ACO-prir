import numpy as np
import random
from typing import List
from map import Map


class AntColony:
    
    def __init__(self, map: Map, alpha: float, beta: float, decay: float):
        self.map = map
        self.alpha = alpha
        self.beta = beta
        self.decay = decay

    def find_new_route(self):
        places_to_visit = [x for x in range(len(self.map.places))].pop(self.map.start)
        if self.map.start != self.map.end:
            places_to_visit.pop(self.map.end)

        current = self.map.start
        route = [].append(current)
        total_len = 0
        
        while places_to_visit:
            next = self.__select_next_place(current, places_to_visit)
            total_len += self.map.connections[current][next]
            current = next
            places_to_visit.pop(current)
            route.append(current)

        route.append[self.map.end]
        total_len += self.map.connections[current][self.map.end]

        return route, total_len

    def leave_pheromones(self, routes: List[List[int]]):
        for route in routes:
            for i in range(0, len(route) - 1):
                conn_start = route[i]
                conn_end = route[i+1]
                self.map.pheromones[conn_start][conn_end] += 1 / self.map.connections[conn_start][conn_end]

    def evaporate_pheromones(self):
        self.map.pheromones *= 1 - self.decay

    def __select_next_place(self, current: int, places_to_visit: List[int]) -> int:
        fitnesses = []
        probabilities = []
        total_fitness = 0
        places_num = len(places_to_visit)

        for i in range(places_num):
            p = places_to_visit[i]
            fitnesses[i] = self.map.pheromones[current][p] ** self.alpha + \
                (1 / self.map.connections[current][p]) ** self.beta 
            total_fitness += fitnesses[i]

        if total_fitness != 0:
            for i in range(places_num):
                probabilities[i] = fitnesses[i] / total_fitness
        else:
            probabilities = [1 / places_num for i in range(0, places_num)]

        return np.random.choice(a = places_to_visit, p = probabilities)