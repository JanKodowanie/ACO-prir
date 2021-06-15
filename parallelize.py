from typing import Any
from mpi4py import MPI as mpi
from numpy import ceil


# funkcja: inicjalizacja MPI
def init_mpi() -> Any:
    comm = mpi.COMM_WORLD
    return comm, comm.Get_rank(), comm.Get_size()


# funkcja: przydział liczby mrówek do każdego z wątków
def divide_ants(num_ants: int, num_proc: int) -> list:
    blocks = []
    block_size =  ceil(num_ants / num_proc)
    current_idx = 0
    
    while (current_idx < num_ants):
        blocks.append(min((num_ants - current_idx), block_size)) # zapewnia że ostatnia wartość dostanie modulo
        current_idx += block_size

    return blocks
    

# funkcja: rozdzielenie danych pomiędzy wątki
def scatter_data(comm: Any, blocks: list[int], root_rank=0) -> None: # root_rank na wypadek, gdybyśmy chcieli zmienić głównego workera na jeden z wątków potomnych
    comm.scatter(blocks, root=root_rank)


# funkcja odbierająca mrówki w wątku potomnym
def get_ants(comm: Any, blocks: list[int], current_rank: int, root_rank=0) -> int:
    current_ants = comm.scatter(blocks, root=root_rank)
    return current_ants


# funkcja zbierająca wszystkie dane w wątku głównym
def gather_data(comm: Any, ant_product: Any, root_rank=0) -> Any:
    return comm.gather(ant_product, root=root_rank)