from map_reader import MapReader
from ant_colony import AntColony
from config import Config
import time
import parallelize as pl
import copy


MAP_FILENAME = 'map.json'
CONFIG_FILENAME = 'config.json'
RANDOM_MAP_SAVE_FILENAME = 'randmap.json'

config = Config()
config.read_config_from_file(CONFIG_FILENAME)

places_map = None
if not config.random_map:
    map_reader = MapReader(MAP_FILENAME)
    places_map = map_reader.read_map()
else:
    places_map = config.randomize_map()


def main():
    
    # inicjalizacja MPI i przygotowanie środowiska
    comm, rank, num_proc = pl.init_mpi()
    best_route = None
    colony = AntColony(places_map, config.alpha, config.beta, config.decay)
    
    # podział liczby mrówek na porcje wysyłane do wątków
    ants = pl.divide_ants(config.ants, num_proc)

    # wątek główny - czas start
    if rank == 0:
        calc_start_time = time.time()

    # wszystkie wątki - właściwa sekcja algorytmu
    for i in range(config.iterations):
        i_routes = []

        # wątek główny - przygotowanie iteracji
        if rank == 0:
            print("Performing iteration:", i)
            colony.evaporate_pheromones()
            pl.scatter_data(comm, ants)

        # wszystkie wątki - poszukiwanie najlepszej drogi
        ants_subgroup = int(pl.get_ants(comm, ants, rank))
        subcolony = copy.deepcopy(colony)
        for j in range(ants_subgroup):
            route = subcolony.find_new_route()
            # lengths are under index 1
            if not best_route or route[1] < best_route[1]:
                best_route = route
            i_routes.append(route[0])
        
    # wyniki częściowe po iteracji
    gathered_routes = pl.gather_data(comm, i_routes)
    if rank == 0:
        subcolony.leave_pheromones(gathered_routes)

    # wątek główny - agregacja wyników
    if rank == 0:
        best_route_str = list(map(lambda id: places_map.places[id], best_route[0]))
        calc_time_elapsed = time.time() - calc_start_time
        print('Best route:')
        print(' -> '.join(best_route_str))
        print(f'Length: {best_route[1]}')
        print()
        print("Elapsed time: %.3f seconds" % calc_time_elapsed)

    if config.rand_places and config.save_generated_map:
        config.save_generated_map_to_file(RANDOM_MAP_SAVE_FILENAME, places_map)


main()