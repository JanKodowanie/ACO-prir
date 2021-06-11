from map_reader import MapReader
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

print(map.connections)