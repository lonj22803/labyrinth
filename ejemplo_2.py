import time
from grafo import Grafo
from random import randint
from labyrinth import Labyrinth
import threading

ROWS = 10
COLUMNS = 20


def create_labyrinth():
    maze = Labyrinth(ROWS, COLUMNS, path='/dev/shm/graph.json')
    maze.start()


def create_graph():
    done = False
    while not done:
        grafo = Grafo()
        # Create a graph of 10 by 20 vertices with random edges
        for i in range(ROWS * COLUMNS):
            # Horizontal edges
            vertex_o = i
            vertex_i = i + 1
            if vertex_i % COLUMNS != 0:
                grafo.add_edge(vertex_o, vertex_i, randint(0, 1))
            # Vertical edges
            vertex_i = i + COLUMNS
            if vertex_i < ROWS * COLUMNS:
                grafo.add_edge(vertex_o, vertex_i, randint(0, 1))

        grafo.save_graph('/dev/shm/graph.json')
        time.sleep(1)
        # if input("Press 'q' to quit: ") == 'q':
        #     done = True


if __name__ == '__main__':
    hilo1 = threading.Thread(target=create_labyrinth)
    hilo1.start()

    hilo2 = threading.Thread(target=create_graph)
    hilo2.start()

    hilo2.join()
    hilo1.join()
