import time
from globales import candado
from grafo import Grafo
from random import randint


def trabajador(rows, columns, ruta=''):
    done = False
    reps = 0
    while not done and reps < 50:
        grafo = Grafo()
        # Create a graph of 10 by 20 vertices with random edges
        for i in range(rows * columns):
            # Horizontal edges
            vertex_o = i
            vertex_i = i + 1
            if vertex_i % columns != 0:
                grafo.add_edge(vertex_o, vertex_i, randint(0, 1))
            # Vertical edges
            vertex_i = i + columns
            if vertex_i < rows * columns:
                grafo.add_edge(vertex_o, vertex_i, randint(0, 1))
        with candado:
            # grafo.save_graph(ruta)
            grafo.send_graph()
        time.sleep(1)
        reps += 1
