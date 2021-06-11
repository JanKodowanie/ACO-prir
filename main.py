from map_reader import MapReader


MAP_FILENAME = 'map.json'
CONFIG_FILENAME = 'config.json'
MAX_NUMBER_OF_ITERATIONS = 1000
NUMBER_OF_ANTS = 20
ALPHA_COEFF = 1
BETA_COEFF = 1
DECAY_RATE = 0.5


map_reader = MapReader(MAP_FILENAME)
map = map_reader.read_map()
