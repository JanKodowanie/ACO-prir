import json
import numpy as np
from map import Map


class Config:

    def __init__(self):
        self.random_map = False
        self.rand_places = 100
        self.iterations = 100
        self.ants = 20
        self.alpha = 1
        self.beta = 1
        self.decay = 0.1

    def read_config_from_file(self, filename: str):
        file_ = open(filename, 'r')
        config_data = json.load(file_)
        file_.close()

        self.random_map = config_data.get('random_map', self.random_map)
        self.rand_places = config_data.get('rand_places', self.rand_places)
        self.iterations = config_data.get('iterations', self.iterations)
        self.ants = config_data.get('ants', self.ants)
        self.alpha = config_data.get('alpha', self.alpha)
        self.beta = config_data.get('beta', self.beta)
        self.decay = config_data.get('decay', self.decay)

    def randomize_map(self) -> Map:
        random_connections = np.random.rand(self.rand_places, self.rand_places) * 100.0 + 20.0
        random_places = []
        for i in range(self.rand_places):
            random_connections[i][i] = None
            random_places.append(i)

        random_start = np.random.choice(a=random_places)
        random_end = np.random.choice(a=random_places)

        random_places = list(map(lambda x: 'place ' + str(x), random_places))
        return Map(random_start, random_end, random_places, self.rand_places, random_connections)