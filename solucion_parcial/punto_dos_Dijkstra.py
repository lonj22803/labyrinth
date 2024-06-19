import json
import heapq
import labyrinth
import threading
import shutil

def cargar_grafo(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    grafo = {}
    for nodo, vecinos in data["V"].items():
        grafo[str(nodo)] = []
        for vecino in vecinos:
            peso = data["E"].get(f"({nodo}, {vecino})") or data["E"].get(f"({vecino}, {nodo})")
            if peso is not None:
                grafo[str(nodo)].append((str(vecino), peso))
    return grafo

def backup_labyrinth(ruta):
    original_json_path = ruta
    backup_json_path = r'buckup.json'

    # Copia del archivo original a uno de respaldo
    shutil.copy(original_json_path, backup_json_path)

    return backup_json_path

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

def guardar_solucion(filename,rute,type_method:str):

    with open(filename, "r") as file:
        data = json.load(file)
    camino = rute
    turtle_solucion={}

    #Creamos el diccionario, basados en el camino de dijkstra
    diccionario_ruta = {}
    for i in range(len(camino)):
        if i < len(camino) - 1:
            diccionario_ruta[camino[i]] = int(camino[i + 1])
        else:
            diccionario_ruta[camino[i]] = 'f'  # Finaliza con 'f' para el último elemento

    data["turtle"] = diccionario_ruta
    #Guardamos el archivo con la solucion
    filename = filename.replace(".json", f"_solucion{type_method}.json")
    with open(filename, "w") as file:
        json.dump(data, file,indent=4)

    print(f"Solucion guardada en {filename}")



def main():
    grafo = cargar_grafo('grafo1.json')
    # Imprimir el grafo para depuración
    inicio = '0'
    objetivo = '224'
    camino, distancia = dijkstra(grafo, inicio, objetivo)
    guardar_solucion('grafo1.json',camino,"Dijkstra")
    print(f"La distancia más corta entre {inicio} y {objetivo} es {distancia}")

if __name__ == "__main__":
    hilo1 = threading.Thread(target=lambda: labyrinth.Labyrinth(15, 15, path=backup_labyrinth('grafo1.json')).start())
    hilo2 = threading.Thread(target=main)
    hilo3 = threading.Thread(target=lambda: labyrinth.Labyrinth(15, 15, path=backup_labyrinth('grafo1_solucionDijkstra.json')).start())

    hilo1.start()
    hilo2.start()

    hilo2.join()
    hilo1.join()
    hilo3.start()

    hilo3.join()