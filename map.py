import numpy as np
from typing import List


class Map:
    def __init__(self, start: int, places: List[str], places_num: int, routes: np.ndarray):
        self.start = start
        self.places = places
        self.routes = routes
        self.pheromones = np.zeros((places_num, places_num))
