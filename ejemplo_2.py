
from labyrinth import Labyrinth
import threading
from worker import trabajador

# Macro expansions -sort of
ROWS = 10
COLUMNS = 20
# windows path
RUTA = r'C:\Users\German Andres\Desktop\grafo.json'
# Linux path
# RUTA = '\dev\shm\grafo.json'


def create_labyrinth():
    maze = Labyrinth(ROWS, COLUMNS, path=RUTA)
    maze.start()


def create_graph():
    trabajador(ROWS, COLUMNS, RUTA)


if __name__ == '__main__':
    hilo1 = threading.Thread(target=create_labyrinth)
    hilo1.start()

    hilo2 = threading.Thread(target=create_graph)
    hilo2.start()

    hilo2.join()
    hilo1.join()
