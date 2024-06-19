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

def guardar_solucion(filename, mst, type_method):
    with open(filename, "r") as file:
        data = json.load(file)
    turtle_solucion = {}
    for frm, to, _ in mst:
        turtle_solucion[frm] = int(to)
    if mst:
        _, to, _ = mst[-1]
        turtle_solucion[to] = 'f'  # Finaliza con 'f' para el nodo objetivo

    data["turtle"] = turtle_solucion

    # Guardamos el archivo con la solucion
    filename = filename.replace(".json", f"_solucion{type_method}.json")
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Solución guardada en {filename}")

def main():
    grafo = cargar_grafo('grafo1.json')
    inicio = '0'
    objetivo = '224'
    mst = prim_modified(grafo, inicio, objetivo)
    guardar_solucion('grafo1.json', mst, "Prim")

    # Presentar el MST y el costo total
    costo_total = sum(peso for _, _, peso in mst)
    print("Árbol de expansión mínima (MST) hasta el objetivo:")
    for frm, to, peso in mst:
        print(f"{frm} --{peso}--> {to}")
    print(f"Costo total hasta el objetivo: {costo_total}")

def backup_labyrinth(ruta):
    original_json_path = ruta
    backup_json_path = r'backup.json'
    shutil.copy(original_json_path, backup_json_path)
    return backup_json_path

if __name__ == "__main__":
    hilo1 = threading.Thread(target=lambda: labyrinth.Labyrinth(15, 15, path=backup_labyrinth('grafo1.json')).start())
    hilo2 = threading.Thread(target=main)
    hilo3 = threading.Thread(target=lambda: labyrinth.Labyrinth(15, 15, path=backup_labyrinth('grafo1_solucionPrim.json')).start())

    hilo1.start()
    hilo2.start()
    hilo2.join()
    hilo1.join()
    hilo3.start()
    hilo3.join()
