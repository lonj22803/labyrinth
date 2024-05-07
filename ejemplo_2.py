"""
This is an example of multi-threading execution
Front-end and Back-end modules are running in different threads
Inter-thread comm is implemented with a Queue and a mutex lock

Damiel Zapata Y.
German A Holguin L.
UTP - Pereira, Colombia 2024.
"""

from labyrinth import Labyrinth
import threading
from worker import trabajador

# Macro expansions -sort of
ROWS = 10
COLUMNS = 20


def create_labyrinth():
    maze = Labyrinth(ROWS, COLUMNS)
    maze.start()


def create_graph():
    trabajador(ROWS, COLUMNS)


if __name__ == '__main__':
    hilo1 = threading.Thread(target=create_labyrinth)
    hilo1.start()

    hilo2 = threading.Thread(target=create_graph)
    hilo2.start()

    hilo2.join()
    hilo1.join()
