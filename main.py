from map_reader import MapReader
from ant_colony import AntColony
from config import Config


MAP_FILENAME = 'map.json'
CONFIG_FILENAME = 'config.json'

config = Config()
config.read_config_from_file(CONFIG_FILENAME)

places_map = None
if not config.random_map:
    map_reader = MapReader(MAP_FILENAME)
    places_map = map_reader.read_map()
else:
    places_map = config.randomize_map()

colony = AntColony(places_map, config.alpha, config.beta, config.decay)
best_route = None

for i in range(config.iterations):
    i_routes = []
    colony.evaporate_pheromones()
    for j in range(config.ants):
        route = colony.find_new_route()
        # lengths are under index 1
        if not best_route or route[1] < best_route[1]:
            best_route = route
        i_routes.append(route[0])
    colony.leave_pheromones(i_routes)


best_route_str = list(map(lambda id: places_map.places[id], best_route[0]))
print('Best route:')
print(' -> '.join(best_route_str))
print(f'Length: {best_route[1]}')
