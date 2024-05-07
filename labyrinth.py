"""
Module to draw a labyrinth from an array using Tkinter

2024
"""

from tiles import Tile
import tkinter as tk
import os
import json
from globales import candado, cola


class Labyrinth:
    def __init__(self, rows: int, columns: int, path=''):
        """
        Initialize a new instance of the Labyrinth class.

        This method sets up the basic properties of the labyrinth, including the number of rows and columns,
        the length of each tile, and the size of the canvas. It also creates a new Tkinter window and sets its title.

        :param rows: (int) The number of rows in the labyrinth.
        :param columns: (int) The number of columns in the labyrinth.
        """
        self.path = path
        self.list_tiles = list()
        self.rows, self.columns = rows, columns
        # Create a 2D array to store the tiles (not a definitive feature. Could be deleted)
        self.tile_array = [[0 for _ in range(columns)] for _ in range(rows)]
        self.tile_length = 50
        self.canvas_sz = self._get_canvas_sz()
        self.window = tk.Tk()
        self.window.title("Maze")
        self.window.configure(bg='dark gray')
        self._create_canvas()
        self.get_board()
        self.window.after(10, self.update_maze)

    def start(self):
        self.window.mainloop()

    def _create_canvas(self):
        """
        Create a canvas for the labyrinth.

        This method creates a new Tkinter Canvas object, sets its width and height to the size of the canvas,
        and then packs it into the window. The canvas is where the labyrinth will be drawn.

        :return: None
        """
        self.canvas = tk.Canvas(self.window, width=self.canvas_sz[0], height=self.canvas_sz[1])
        self.canvas.pack()  # Pack the canvas into the window

    def get_board(self):
        """
        Generate the board for the labyrinth.
        This method creates a list of Tile objects, one for each cell in the labyrinth.
        Each Tile object is drawn on the canvas.

        :return: (list) A list of Tile objects representing the labyrinth.
        """
        for i in range(self.rows):
            for j in range(self.columns):
                tile_mn = Tile(self.canvas, j * self.tile_length, i * self.tile_length, length=self.tile_length)
                self.tile_array[i][j] = tile_mn  # This still is a possible feature (could be deleted)
                self.list_tiles.append(tile_mn)
                tile_mn.draw()

        return self.list_tiles

    def _get_canvas_sz(self):
        """
        Calculate the size of the canvas.

        This method calculates the size of the canvas based on the number of rows
        and columns in the labyrinth and the length of each tile.

        :return: (tuple) A tuple containing the width and height of the canvas.
        """
        height = self.tile_length * self.rows
        width = self.tile_length * self.columns
        return width, height

    def _get_window_sz(self):
        """
        Calculate the size of the window.

        This method calculates the size of the window based on the size of the canvas.
        It adds a 10-pixel margin to the width and height of the canvas to determine the window size.

        :return: (str) A string representing the size of the window in the format "widthxheight".
        """
        width = self.canvas_sz[0] + 10  # Add 10 pixels to the canvas width for the window width
        height = self.canvas_sz[1] + 10  # Add 10 pixels to the canvas height for the window height
        win_sz = f"{width}x{height}"  # Format the window size as a string in the format "widthxheight"
        return win_sz

    def update_maze(self, imprimir=True):
        """
        Update the maze based on the information in a JSON file.

        This method reads a JSON file located at '/dev/shm/graph.json'.
        If the file exists, it loads the JSON data into a dictionary and checks the walls in the
        maze based on this data. If the file does not exist, it prints a message indicating this.

        After checking the walls, the method schedules itself to be called again after 300 milliseconds. This allows the
        maze to be updated in real time as the JSON file changes.

        :return: None
        """

        # First check the pipe, if there's nothing there, check the file.
        if not cola.empty():
            with candado:
                graph = cola.get()
            imprimir = True
            print('The graph structure has been updated from Queue.')
            self._check_walls(graph)
            self._mark_turtle(graph['turtle'])
        else:
            # read json file, if it does not exist, do nothing
            if os.path.exists(self.path):
                with candado:
                    with open(self.path, 'r') as f:
                        graph = json.load(f)
                    f.close()
                    os.remove(self.path)
                imprimir = True
                print('The graph structure has been updated from file.')
                self._check_walls(graph)
                self._mark_turtle(graph['turtle'])
        if imprimir:
            print("Nothing to update.")
            imprimir = False

        self.canvas.after(20, self.update_maze, imprimir)

    def _check_walls(self, graph: dict):
        vertex_list = graph['V']
        edges_list = graph['E']
        # vertex_o is the origin vertex, vertex_i is the destination vertex
        for vertex_o in vertex_list:
            for vertex_i in vertex_list[vertex_o]:
                if edges_list.get(f"({vertex_o}, {vertex_i})") == 0 or edges_list.get(f"({vertex_i}, {vertex_o})") == 0:
                    # print(f"There is a wall in edge:     ({vertex_o}, {vertex_i})")
                    self._update_border(int(vertex_o), int(vertex_i), state=True)
                else:
                    # print(f"There is not a wall in edge: ({vertex_o}, {vertex_i})")
                    self._update_border(int(vertex_o), int(vertex_i))

    def _update_border(self, vertex_o: int, vertex_i: int, state=False):
        """
        Update the border of a tile in the labyrinth.

        This method calculates the row and column positions of two vertices, determines which border of the tile
        at the position of the first vertex needs to be updated based on the relative positions of the vertices,
        and then updates the border's state.

        :param vertex_o: (int) The origin vertex.
        :param vertex_i: (int) The destination vertex.
        :param state: (bool) The state to set the border to. If True, the border is set to exist.
                      If False, the border is set to not exist.
        :return: None
        """
        # Calculate the row and column positions of the vertices
        row_o, col_o = divmod(vertex_o, self.columns)
        row_i, col_i = divmod(vertex_i, self.columns)

        # Determine the border to be deleted
        if row_o == row_i:  # The vertices are in the same row
            border_id = 3 if col_o < col_i else 2  # Delete left border if vertex_o < vertex_i, else delete right border
            # print(f"row_o: {row_o}, col_o: {col_o}, row_i: {row_i}, col_i: {col_i}, border_id: {border_id}")
        else:  # The vertices are in the same column
            border_id = 1 if row_o < row_i else 0  # Delete upper border if vertex_o < vertex_i, else delete bottom
            # border
        # Get the tile and delete the border
        tile = self.get_tile(row_o, col_o)
        tile.update_border_visualization(border_id, state=state)

    def get_tile(self, row, column):
        """
        Get a specific tile from the list_tiles list.
        :param row: (int) The row position of the tile.
        :param column: (int) The column position of the tile.
        :return: (Tile) The Tile object at the specified position.
        """
        index = row * self.columns + column
        return self.list_tiles[index]

    def _mark_turtle(self, turtle_positions: dict):
        """
        Mark the solution path in the labyrinth.

        This method iterates over the solution graph, which is a dictionary where each key-value pair represents a step
        in the solution path. For each step, it calculates the row and column positions of the vertices, gets the tile
        at the position of the first vertex, determines the direction of the turtle based on the relative positions of
        the vertices, rotates the turtle to the determined direction, and then draws the turtle on the tile.

        :param turtle_positions:
        :return: None
        """

        for tile in self.list_tiles:
            tile.change_turtle_state(erase=True)

        for vertex_o, vertex_i in turtle_positions.items():
            print(f"Path: {vertex_o} -> {vertex_i}")
            # Calculate the row and column positions of the vertices
            if vertex_i == 'f':
                row_o, col_o = divmod(int(vertex_o), self.columns)
                tile = self.get_tile(row_o, col_o)
                tile.rotate_turtle(direction='u')  # Rotate the turtle to the up direction
                # Draw the turtle on the tile
                tile.change_turtle_state(erase=False)

            else:
                row_o, col_o = divmod(int(vertex_o), self.columns)
                row_i, col_i = divmod(int(vertex_i), self.columns)
                # Get the tile
                tile = self.get_tile(row_o, col_o)
                # Determine the direction of the turtle
                if row_o == row_i:  # The vertices are in the same row
                    direction = 'r' if col_o < col_i else 'l'  # Move right if vertex_o < vertex_i, else move left
                else:  # The vertices are in the same column
                    direction = 'd' if row_o < row_i else 'u'  # Move down if vertex_o < vertex_i, else move up
                # Rotate the turtle to the determined direction
                tile.rotate_turtle(direction)
                # Draw the turtle on the tile
                tile.change_turtle_state(erase=False)


if __name__ == '__main__':
    # maze = Labyrinth(2, 3, path='/dev/shm/graph.json') # linux
    maze = Labyrinth(2, 3, path=r'C:\Users\German Andres\Desktop\grafo.json')  # windwos
    maze.start()
