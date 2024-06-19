import json  # Importa la biblioteca JSON para trabajar con archivos JSON.
import heapq  # Importa heapq para trabajar con colas de prioridad.
import labyrinth  # Importa la biblioteca labyrinth para representar el laberinto.
import threading  # Importa threading para trabajar con hilos.
import shutil  # Importa shutil para copiar archivos.
import time  # Importa time para medir el tiempo de ejecución.
import networkx as nx  # Importa networkx para trabajar con grafos y visualizarlos.
import matplotlib.pyplot as plt  # Importa matplotlib para graficar.

# Función para cargar el grafo desde un archivo JSON.
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

# Función para encontrar el representante de un conjunto (usado en Kruskal).
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

# Función para guardar la solución en un archivo JSON.
def guardar_solucion(filename, mst, type_method):
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

# Función principal para ejecutar el algoritmo de Kruskal y guardar la solución.
def main():
    grafo, aristas = cargar_grafo('grafo1.json')  # Carga el grafo y las aristas.
    inicio = '0'
    objetivo = '224'
    start_time = time.time()  # Tiempo de inicio.
    mst, total_peso = kruskal_modified(grafo, aristas, inicio, objetivo)  # Ejecuta el algoritmo de Kruskal.
    end_time = time.time()  # Tiempo de finalización.
    guardar_solucion('grafo1.json', mst, "Kruskal")  # Guarda la solución.

    # Presentar el MST y el costo total.
    print("Árbol de expansión mínima (MST) hasta el objetivo:")
    for frm, to, peso in mst:
        print(f"{frm} --{peso}--> {to}")
    print(f"Costo total hasta el objetivo: {total_peso}")
    print(f"Tiempo de ejecución de Kruskal: {end_time - start_time} segundos")

# Función para hacer una copia de seguridad del archivo JSON.
def backup_labyrinth(ruta):
    original_json_path = ruta
    backup_json_path = r'backup.json'
    shutil.copy(original_json_path, backup_json_path)  # Copia el archivo original.
    return backup_json_path  # Retorna la ruta de la copia de seguridad.

if __name__ == "__main__":
    # Crea los hilos para ejecutar las funciones concurrentemente.
    hilo1 = threading.Thread(target=lambda: labyrinth.Labyrinth(15, 15, path=backup_labyrinth('grafo1.json')).start())
    hilo2 = threading.Thread(target=main)
    hilo3 = threading.Thread(target=lambda: labyrinth.Labyrinth(15, 15, path=backup_labyrinth('grafo1_solucionKruskal.json')).start())

    hilo1.start()  # Inicia el hilo para representar el laberinto original.
    hilo2.start()  # Inicia el hilo para ejecutar el algoritmo de Kruskal.
    hilo2.join()  # Espera a que el hilo del algoritmo de Kruskal termine.
    hilo1.join()  # Espera a que el hilo de la representación del laberinto original termine.
    hilo3.start()  # Inicia el hilo para representar el laberinto con la solución de Kruskal.
    hilo3.join()  # Espera a que el hilo de la representación de la solución termine.
