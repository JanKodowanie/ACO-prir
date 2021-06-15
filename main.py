from map_reader import MapReader
from ant_colony import AntColony
from config import Config
import time
import parallelize as pl

############## STAŁE ####################

MAP_FILENAME = 'map.json'
CONFIG_FILENAME = 'config.json'
RANDOM_MAP_SAVE_FILENAME = 'randmap.json'

#########################################

def main():
    
    # inicjalizacja MPI i przygotowanie środowiska
    comm, rank, num_proc = pl.init_mpi()
    places_map = None
    config = Config()
    config.read_config_from_file(CONFIG_FILENAME)
    all_routes = None

    # podział liczby mrówek na porcje wysyłane do procesów
    ants = pl.divide_ants(config.ants, num_proc)

    # proces główny - init
    if rank == 0:
        if not config.random_map:
            map_reader = MapReader(MAP_FILENAME)
            places_map = map_reader.read_map()
        else:
            places_map = config.randomize_map()
        colony = AntColony(places_map, config.alpha, config.beta, config.decay)

        calc_start_time = time.time()

    # wszystkie procesy - właściwa sekcja algorytmu
    for i in range(config.iterations):
        i_routes = []

        # proces główny - przygotowanie iteracji
        if rank == 0:
            print("Performing iteration:", i)
            colony.evaporate_pheromones()
            pl.send_data(comm, num_proc, colony)
        # procesy poboczne - przypisanie właściwej kolonii
        else:
            colony = pl.recv_data(comm)

        # wszystkie procesy - poszukiwanie najlepszej drogi
        ants_subgroup = int(ants[rank])
        for j in range(ants_subgroup):
            route = colony.find_new_route()
            # długości ścieżek są pod indeksem 1
            i_routes.append(route)
        
        # wyniki częściowe po iteracji
        gathered_routes = pl.gather_data(comm, i_routes)
        if rank == 0:
            all_routes = []
            for l in gathered_routes:
                all_routes += l
            colony.leave_pheromones(all_routes)

    # proces główny - agregacja wyników
    if rank == 0:

        # bierzemy pod uwagę ostatnią iterację
        best_route = None
        for route in all_routes:
            if not best_route or route[1] < best_route[1]:
                best_route = route

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