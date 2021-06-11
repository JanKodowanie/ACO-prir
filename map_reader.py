import json
import numpy as np
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

        places_num = len(places)
        routes = self.__parse_routes(map_data['routes'], places_num)

        return Map(start, places, places_num, routes)

    def __parse_places(self, places) -> List[str]:
        return list(map(lambda place: place['name'], places))

    def __parse_routes(self, routes, places_num) -> np.ndarray:
        routes_as_arr = np.full((places_num, places_num), np.inf)

        for route_data in routes:
            start = route_data['start'] - 1
            end = route_data['end'] - 1
            len_ = route_data['len']

            routes_as_arr[start][end] = len_
            routes_as_arr[end][start] = len_

        return routes_as_arr