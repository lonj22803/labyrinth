
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
