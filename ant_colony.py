import numpy as np
import random
from typing import List
from map import Map


class AntColony:
    
    def __init__(self, map: Map, alpha: float, beta: float, 
                decay: float, ants: int, iterations: int):
        self.map = map
        self.alpha = alpha
        self.beta = beta
        self.decay = decay
        self.ants = ants
        self.iterations = iterations

    def find_best_route(self):
        pass

    def __select_next_place(self, current: int, visited: List[int]) -> int:
        pass

    def __leave_pheromones(self, routes: List[int][int]):
        pass

    def __evaporate_pheromones(self):
        self.map.pheromones *= 1 - self.decay