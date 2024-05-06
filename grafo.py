"""
Minimum example creating a labyrinth. In this case, the graph was created by hand.
"""

import json


class Grafo:
    """
    Class to represent a graph, specifically a labyrinth.
    """

    def __init__(self, V: dict = None, E: dict = None, turtle: dict = None):
        """
        Initialize the graph with the vertices, edges and the turtle
        """
        if V is None:
            V = dict()
        self.V = V
        if E is None:
            E = dict()
        self.E = E
        if turtle is None:
            turtle = dict()
        self.turtle = turtle

    def __repr__(self):
        """
        Return the graph as a string
        """
        return f'Vertices: {self.V}\nEdges: {self.E}\nTurtle: {self.turtle}'

    def save_graph(self, path: str):
        """
        Save the graph as a json file_graph
        """
        grafo_g = {'V': self.V, 'E': self.E, 'turtle': self.turtle}
        with open(path, 'w') as file_graph:
            json.dump(grafo_g, file_graph, indent=4)
        # Close the file_graph
        file_graph.close()

    def add_edge(self, vertex_o: int, vertex_i: int, weight: int):
        """
        Add an edge to the graph
        """
        # Verify if the edge already exists
        if f"({vertex_o}, {vertex_i})" in self.E or f"({vertex_i}, {vertex_o})" in self.E:
            print(f"The edge ({vertex_o}, {vertex_i}) already exists.")
        else:
            # Verify if vertices exist or add them if they are not in the graph
            if vertex_o not in self.V:
                self.V[vertex_o] = [vertex_i]
            else:
                self.V[vertex_o].append(vertex_i)
            if vertex_i not in self.V:
                self.V[vertex_i] = [vertex_o]
            else:
                self.V[vertex_i].append(vertex_o)
            # Add the edge to the graph
            self.E[f"({vertex_o}, {vertex_i})"] = weight


if __name__ == '__main__':
    # Create a dictionary with the adjacency list of vertices of the graph
    vertex_list = {0: [1, 3], 1: [0, 2, 4], 2: [1, 5], 3: [0, 4],
                   4: [1, 3, 5], 5: [2, 4]}
    # Create a dictionary with the adjacency list of weighted edges of the graph
    # If edge weight is 0, there is no path between the nodes (a wall exists),
    # if edge weight is 1, there is a path between the nodes (a wall does not exist)
    edges_list = {'(0, 1)': 1, '(0, 3)': 0, '(1, 2)': 0, '(1, 4)': 1, '(2, 5)': 0, '(3, 4)': 1, '(4, 5)': 1}
    # List of all vertices to show a turtle (the key) and the turtle's goal (the value)
    turtle_list = {1: 5}  # {0: 1, 1: 4, 4: 5, 5: 'f'}  # 'f' is a centinel value to represent turtle's exit
    # Create a graph
    grafo = Grafo(vertex_list, edges_list, turtle_list)
    # Save the graph as a json file
    grafo.save_graph('/dev/shm/graph.json')
    print(grafo)
