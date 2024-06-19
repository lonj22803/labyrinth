import json
import heapq
import threading
import shutil
import time
import labyrinth
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def cargar_grafo(filename):
    with open(filename, 'r') as file:
        data = json.load(file)  # Carga los datos del archivo JSON.
    grafo = {}
    aristas = []
    for nodo, vecinos in data["V"].items():
        grafo[str(nodo)] = []
        for vecino in vecinos:
            # Obtiene el peso de la arista entre nodo y vecino.
            peso = data["E"].get(f"({nodo}, {vecino})") or data["E"].get(f"({vecino}, {nodo})")
            if peso is not None:
                grafo[str(nodo)].append((str(vecino), peso))  # Añade el vecino y el peso al grafo.
                aristas.append((peso, str(nodo), str(vecino)))  # Añade la arista a la lista de aristas.
    return grafo, aristas  # Retorna el grafo y la lista de aristas.


def backup_labyrinth(ruta,type_method=None):
    backup_json_path = ruta.replace(".json", f"{type_method}_backup.json")
    shutil.copy(ruta, backup_json_path)
    return backup_json_path

def guardar_solucion(filename, ruta, type_method):
    if type_method == "Dijkstra":
        with open(filename, "r") as file:
            data = json.load(file)
        camino = ruta
        turtle_solucion = {}

        # Creamos el diccionario, basados en el camino de dijkstra
        diccionario_ruta = {}
        for i in range(len(camino)):
            if i < len(camino) - 1:
                diccionario_ruta[camino[i]] = int(camino[i + 1])
            else:
                diccionario_ruta[camino[i]] = 'f'  # Finaliza con 'f' para el último elemento

        data["turtle"] = diccionario_ruta
        # Guardamos el archivo con la solucion
        filename = filename.replace(".json", f"_solucion{type_method}.json")
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Solucion guardada en {filename}")
    else:
        mst=ruta
        with open(filename, "r") as file:
            data = json.load(file)  # Carga los datos del archivo JSON.
        turtle_solucion = {}
        for frm, to, _ in mst:
            turtle_solucion[frm] = int(to)
        if mst:
            _, to, _ = mst[-1]
            turtle_solucion[to] = 'f'  # Finaliza con 'f' para el nodo objetivo.

        data["turtle"] = turtle_solucion

        # Guardamos el archivo con la solución.
        filename = filename.replace(".json", f"_solucion{type_method}.json")
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)  # Guarda los datos en el archivo JSON.
        print(f"Solución guardada en {filename}")



# Algortimo de Dijkstra
def dijkstra(grafo, inicio, objetivo):
    # Cola de prioridad
    cola = [(0, inicio)]
    # Diccionario para las distancias más cortas
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    # Diccionario para rastrear el camino
    anteriores = {nodo: None for nodo in grafo}

    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)

        # Si llegamos al nodo objetivo, terminamos
        if nodo_actual == objetivo:
            break

        # Actualizar las distancias a los vecinos
        for vecino, peso in grafo[nodo_actual]:
            distancia = distancia_actual + peso

            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                anteriores[vecino] = nodo_actual
                heapq.heappush(cola, (distancia, vecino))

    # Reconstruir el camino
    camino = []
    nodo = objetivo
    while nodo is not None:
        camino.append(nodo)
        nodo = anteriores[nodo]
    camino.reverse()

    return camino, distancias[objetivo]

#Algoritmo de Prim
def prim_modified(grafo, inicio, objetivo):
    aristas_pendientes = [(0, inicio, inicio)]
    visitados = set()
    mst = []

    while aristas_pendientes:
        peso, frm, to = heapq.heappop(aristas_pendientes)
        if to not in visitados:
            visitados.add(to)
            mst.append((frm, to, peso))
            if to == objetivo:  # Si alcanzamos el objetivo, terminamos el bucle
                break
            for next_to, next_peso in grafo[to]:
                if next_to not in visitados:
                    heapq.heappush(aristas_pendientes, (next_peso, to, next_to))
    return mst

#Algoritmo de Kruskal
def encontrar(parent, i):
    if parent[i] == i:
        return i
    else:
        return encontrar(parent, parent[i])

# Función para unir dos conjuntos (usado en Kruskal).
def union(parent, rank, x, y):
    root_x = encontrar(parent, x)
    root_y = encontrar(parent, y)

    if rank[root_x] < rank[root_y]:
        parent[root_x] = root_y
    elif rank[root_x] > rank[root_y]:
        parent[root_y] = root_x
    else:
        parent[root_y] = root_x
        rank[root_x] += 1

# Algoritmo de Kruskal modificado para detenerse al alcanzar el objetivo.
def kruskal_modified(grafo, aristas, inicio, objetivo):
    aristas.sort(key=lambda x: x[0])  # Ordena las aristas por peso.
    parent = {}
    rank = {}

    # Inicializa los conjuntos disjuntos.
    for nodo in grafo:
        parent[nodo] = nodo
        rank[nodo] = 0

    mst = []  # Lista para almacenar las aristas del MST.
    total_peso = 0  # Variable para almacenar el peso total del MST.
    for arista in aristas:
        peso, nodo1, nodo2 = arista
        root1 = encontrar(parent, nodo1)
        root2 = encontrar(parent, nodo2)

        if root1 != root2:  # Si no forman un ciclo.
            mst.append((nodo1, nodo2, peso))  # Añade la arista al MST.
            total_peso += peso  # Añade el peso de la arista al peso total.
            union(parent, rank, root1, root2)  # Une los conjuntos.

            # Verifica si se ha alcanzado el objetivo.
            if nodo2 == objetivo or nodo1 == objetivo:
                break

    return mst, total_peso  # Retorna el MST y su peso total.

def ejecutar_algoritmo(grafo, metodo, inicio, objetivo,aristas):
    start_time = time.time()
    if metodo == 'Dijkstra':
        ruta, _ = dijkstra(grafo, inicio, objetivo)
    elif metodo == 'Kruskal':
        ruta, _ = kruskal_modified(grafo,aristas,inicio, objetivo)
    elif metodo == 'Prim':
        ruta = prim_modified(grafo, inicio, objetivo)
    end_time = time.time()
    elapsed_time=(end_time-start_time)*1e6
    #print(f"Tiempo de ejecución de {metodo}: {elapsed_time:.15f} segundos")
    return ruta,elapsed_time

def main():
    grafo, aristas = cargar_grafo('grafo1.json')
    inicio = '0'
    objetivo = '224'
    resultados = {'Dijkstra': [], 'Kruskal': [], 'Prim': []}
    metodos = ['Dijkstra', 'Kruskal', 'Prim']
    #Mostamos el laberinto
    labyrinth.Labyrinth(15, 15, path=backup_labyrinth('grafo1.json')).start()

    # Ejecuta cada algoritmo
    for metodo in metodos:
        tiempo=[]
        print(f"Ejecutando {metodo}")
        for i in range(100):
            ruta,elapsed_time=ejecutar_algoritmo(grafo, metodo, inicio, objetivo,aristas)
            tiempo.append(elapsed_time)
            if i == 99:
                guardar_solucion('grafo1.json', ruta, metodo)
                backup_path = backup_labyrinth(f'grafo1_solucion{metodo}.json',type_method=metodo)
                # Inicia la visualización del laberinto con la solución
                labyrinth.Labyrinth(15, 15, path=backup_path).start()
        resultados[metodo] = np.mean(tiempo)

        #Caculemos momentos
        media = np.mean(tiempo)
        desviacion_std = np.std(tiempo)


        print(f"Resultados para el algoritmo {metodo}:")
        print(f"Media: {media:.8f} ± {desviacion_std:.8f} µs")

        # Graficar la distribución de los tiempos
        plt.figure(metodos.index(metodo)+1)
        plt.figure(figsize=(8, 6))
        plt.title(f"Distribución del tiempo de ejecución para {metodo}")
        plt.xlabel('Tiempo de Ejecución (µs)')
        plt.ylabel('Frecuencia')
        count, bins, ignored = plt.hist(tiempo, bins=30, density=True, alpha=0.6, color='g',
                                        label=f'Histograma de {metodo}')

        # Ajuste de la curva gaussiana
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, media, desviacion_std)
        plt.plot(x, p, 'k', linewidth=2, label=f'Ajuste Gaussiano de {metodo} (μ={media:.2f}, σ={desviacion_std:.2f})')
        plt.legend()

    plt.show()


if __name__ == "__main__":
    threading.Thread(target=main).start()