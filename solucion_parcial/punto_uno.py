# Importa los módulos necesarios
import random
import tkinter as tk
from grafo import Grafo
from tiles import Tile
from worker import trabajador
import networkx as nx
import matplotlib.pyplot as plt
import json

# Define la clase LabyrinthGenerator
class LabyrinthGenerator:
    def __init__(self, num_vertices, canvas, cell_size):
        # Inicializa las variables de la clase
        self.delay = 100  # Retardo para la animación
        self.num_vertices = num_vertices  # Número de vértices en el grafo
        self.canvas = canvas  # Canvas de tkinter para dibujar
        self.cell_size = cell_size  # Tamaño de cada celda

        # Inicializa el grafo y las tiles (celdas)
        self.grafo = Grafo()
        self.tiles = [
            Tile(canvas, (i % int(num_vertices ** 0.5)) * cell_size, (i // int(num_vertices ** 0.5)) * cell_size,
                 length=cell_size)
            for i in range(num_vertices)]

        self.turtle_tile = None  # Tile actual donde está la "tortuga"

    # Dibuja la cuadrícula inicial
    def draw_grid(self):
        for tile in self.tiles:
            tile.draw()

    # Genera el laberinto comenzando desde un vértice inicial
    def generate_maze(self, start_vertex=0):
        self.stack = [start_vertex]  # Pila para almacenar el camino actual
        self.visited = [False] * self.num_vertices  # Lista de vértices visitados
        self.visited[start_vertex] = True  # Marca el vértice inicial como visitado
        self.canvas.after(self.delay, self.step)  # Llama al método step después del retardo

    # Realiza un paso en la generación del laberinto
    def step(self):
        if self.stack:
            current_vertex = self.stack[-1]  # Obtiene el vértice actual

            neighbors = self.get_unvisited_neighbors(current_vertex)  # Obtiene los vecinos no visitados
            if neighbors:
                next_vertex = random.choice(neighbors)  # Selecciona un vecino aleatorio
                self.remove_wall(current_vertex, next_vertex)  # Elimina la pared entre los vértices

                self.visited[next_vertex] = True  # Marca el vecino como visitado
                self.stack.append(next_vertex)  # Añade el vecino a la pila

                self.show_turtle(current_vertex, next_vertex)  # Muestra la "tortuga" en el nuevo vértice
            else:
                self.stack.pop()  # Si no hay vecinos no visitados, retrocede en la pila

            self.canvas.after(self.delay, self.step)  # Llama al método step después del retardo
        else:
            print("Labyrinth generation complete")
            self.display_graph()  # Muestra el grafo una vez que el laberinto esté completo

    # Obtiene los vecinos no visitados de un vértice dado
    def get_unvisited_neighbors(self, vertex):
        num_per_row = int(self.num_vertices ** 0.5)  # Asumiendo una matriz cuadrada
        neighbors = []
        row, col = divmod(vertex, num_per_row)  # Calcula la fila y la columna del vértice

        if row > 0 and not self.visited[vertex - num_per_row]:
            neighbors.append(vertex - num_per_row)  # Vecino de arriba
        if row < num_per_row - 1 and not self.visited[vertex + num_per_row]:
            neighbors.append(vertex + num_per_row)  # Vecino de abajo
        if col > 0 and not self.visited[vertex - 1]:
            neighbors.append(vertex - 1)  # Vecino de la izquierda
        if col < num_per_row - 1 and not self.visited[vertex + 1]:
            neighbors.append(vertex + 1)  # Vecino de la derecha

        return neighbors

    # Elimina la pared entre dos vértices
    def remove_wall(self, vertex_o, vertex_i):
        border_to_update = self.determine_border(vertex_o, vertex_i)  # Determina la pared a eliminar
        if border_to_update is not None:
            self.tiles[vertex_o].update_border_visualization(border_to_update, False)  # Actualiza la visualización de la pared
            self.tiles[vertex_i].update_border_visualization(self.determine_border(vertex_i, vertex_o), False)
            self.tiles[vertex_o].draw()  # Dibuja el tile actualizado
            self.tiles[vertex_i].draw()
            self.grafo.add_edge(vertex_o, vertex_i, 1)  # Añade una arista al grafo
        else:
            print(f"No valid border found between vertices {vertex_o} and {vertex_i}")

    # Determina qué pared eliminar entre dos vértices
    def determine_border(self, vertex_o, vertex_i):
        num_per_row = int(self.num_vertices ** 0.5)
        row_o, col_o = divmod(vertex_o, num_per_row)
        row_i, col_i = divmod(vertex_i, num_per_row)

        if row_o == row_i:
            if col_o + 1 == col_i:
                return 3  # Derecha
            elif col_o - 1 == col_i:
                return 2  # Izquierda
        elif col_o == col_i:
            if row_o + 1 == row_i:
                return 1  # Abajo
            elif row_o - 1 == row_i:
                return 0  # Arriba

        return None

    # Muestra la "tortuga" (representación visual) en el laberinto
    def show_turtle(self, vertex_o, vertex_i):
        if self.turtle_tile:
            self.turtle_tile.change_turtle_state(erase=True)  # Borra la "tortuga" del tile anterior

        direction = self.determine_turtle_direction(vertex_o, vertex_i)  # Determina la dirección de la "tortuga"
        self.tiles[vertex_i].rotate_turtle(direction)  # Rota la "tortuga" en la dirección correcta
        self.tiles[vertex_i].change_turtle_state(erase=False)  # Muestra la "tortuga" en el nuevo tile
        self.turtle_tile = self.tiles[vertex_i]

    # Determina la dirección en la que debe moverse la "tortuga"
    def determine_turtle_direction(self, vertex_o, vertex_i):
        num_per_row = int(self.num_vertices ** 0.5)
        row_o, col_o = divmod(vertex_o, num_per_row)
        row_i, col_i = divmod(vertex_i, num_per_row)

        if row_o == row_i:
            if col_o < col_i:
                return 'r'  # Derecha
            else:
                return 'l'  # Izquierda
        else:
            if row_o < row_i:
                return 'd'  # Abajo
            else:
                return 'u'  # Arriba

    # Muestra el grafo generado en una visualización
    def display_graph(self):
        self.grafo.save_graph('grafo1.json')  # Guarda el grafo en un archivo JSON
        
        # Carga los datos del archivo JSON
        with open("grafo1.json", "r") as file:
            data = json.load(file)

        # Crea un grafo vacío
        G = nx.Graph()

        # Agrega nodos al grafo con sus conexiones
        for node, edges in data["V"].items():
            G.add_node(int(node))
            for edge in edges:
                G.add_edge(int(node), edge)

        # Dibuja el grafo usando NetworkX y Matplotlib
        plt.figure(figsize=(18, 10))
        spring_pos = nx.spring_layout(G)
        nx.draw(G, spring_pos, with_labels=True, node_size=700, node_color='skyblue', edge_color='gray', font_weight='bold')
        plt.title("Grafo Creado")
        plt.show()

# Bloque principal del script
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Labyrinth Generator")
    canvas_size = 500
    canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
    canvas.pack()

    num_vertices = 15**2  # Asumiendo una matriz cuadrada de 15x15
    cell_size = canvas_size // int(num_vertices ** 0.5)
    labyrinth_generator = LabyrinthGenerator(num_vertices, canvas, cell_size)
    labyrinth_generator.draw_grid()  # Dibuja la cuadrícula inicial
    labyrinth_generator.generate_maze()  # Genera el laberinto
    root.mainloop()  # Inicia el bucle principal de tkinter
