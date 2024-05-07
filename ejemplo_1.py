from grafo import Grafo

if __name__ == '__main__':
    grafo = Grafo()
    grafo.add_edge(0, 1, 1)
    grafo.add_edge(0, 3, 0)
    grafo.add_edge(1, 2, 0)
    grafo.add_edge(1, 4, 1)
    grafo.add_edge(2, 5, 0)
    grafo.add_edge(3, 4, 1)
    grafo.add_edge(4, 5, 1)

    print(grafo)
    # grafo.save_graph('/dev/shm/graph.json')
    grafo.save_graph(r'C:\Users\German Andres\Desktop\grafo.json')
