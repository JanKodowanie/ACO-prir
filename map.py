import numpy as np
from typing import List


class Map:
    def __init__(self, start: int, end: int, places: List[str], places_num: int, connections: np.ndarray):
        self.start = start
        self.end = end
        self.places = places
        self.connections = connections
        self.pheromones = np.zeros((places_num, places_num))