import json
import numpy as np
import sys
from map import Map
from typing import List


class MapReader:
    def __init__(self, filename: str):
        self.filename = filename

    def read_map(self) -> Map:
        file_ = open(self.filename, 'r')
        map_data = json.load(file_)
        file_.close()

        places = self.__parse_places(map_data['places'])

        # places are enumerated from 1 in map.json
        start = map_data['start'] - 1
        end = map_data['end'] - 1

        places_num = len(places)
        connections = self.__parse_connections(map_data['connections'], places_num)

        for i in range(places_num):
            for j in range(places_num):
                if i != j and not connections[i][j]:
                    print("All places have to be directly connected")
                    sys.exit(-1)

        return Map(start, end, places, places_num, connections)

    def __parse_places(self, places) -> List[str]:
        return list(map(lambda place: place['name'], places))

    def __parse_connections(self, connections, places_num) -> np.ndarray:
        connections_as_arr = np.full((places_num, places_num), None)

        for conn_data in connections:
            start = conn_data['start'] - 1
            end = conn_data['end'] - 1
            len_ = conn_data['len']

            connections_as_arr[start][end] = len_
            connections_as_arr[end][start] = len_

        return connections_as_arr