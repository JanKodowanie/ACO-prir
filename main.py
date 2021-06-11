from map_reader import MapReader
from ant_colony import AntColony
from config import Config


MAP_FILENAME = 'map.json'
CONFIG_FILENAME = 'config.json'

config = Config()
config.read_config_from_file(CONFIG_FILENAME)

map = None
if not config.random_map:
    map_reader = MapReader(MAP_FILENAME)
    map = map_reader.read_map()
else:
    map = config.randomize_map()

colony = AntColony(map, config.alpha, config.beta, config.decay)
route = colony.find_new_route()
print(route)
colony.leave_pheromones([route[0]])
print(map.pheromones)
colony.evaporate_pheromones()
print(map.pheromones)