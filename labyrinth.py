"""
Module to draw a labyrinth from an array using Tkinter

2024
"""

from tiles import Tile
import tkinter as tk
import os
import json


class Labyrinth:
    def __init__(self, rows: int, columns: int):
        """
        Initialize a new instance of the Labyrinth class.

        This method sets up the basic properties of the labyrinth, including the number of rows and columns,
        the length of each tile, and the size of the canvas. It also creates a new Tkinter window and sets its title.

        :param rows: (int) The number of rows in the labyrinth.
        :param columns: (int) The number of columns in the labyrinth.
        """
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

    def update_maze(self):
        """
        Update the maze.
        :return:
        """
        # read json file, if it does not exist, do nothing
        if os.path.exists('/dev/shm/graph.json'):
            with open('/dev/shm/graph.json', 'r') as f:
                graph = json.load(f)
            print(graph)
            self._check_walls(graph)

            f.close()
            # os.remove('/dev/shm/graph.json')
        else:
            print("The file does not exist.")

        self.canvas.after(300, self.update_maze)

    def _check_walls(self, graph: dict):
        vertex_list = graph['V']
        edges_list = graph['E']
        # vertex_o is the origin vertex, vertex_i is the destination vertex
        for vertex_o in vertex_list:
            for vertex_i in vertex_list[vertex_o]:
                if edges_list.get(f"({vertex_o}, {vertex_i})") == 0 or edges_list.get(f"({vertex_i}, {vertex_o})") == 0:
                    print(f"There is a wall in edge:     ({vertex_o}, {vertex_i})")
                else:
                    print(f"There is not a wall in edge: ({vertex_o}, {vertex_i})")
                    # 1) Determine the border of the tile to be deleted: u, b, l, r ==> 0, 1, 2, 3
                    # Si estan en la misma fila: l, r ==> l si vertex_o < vertex_i, r si vertex_o > vertex_i
                    # Si estan en la misma columna: u, b ==> u si vertex_o < vertex_i, b si vertex_o > vertex_i
                    # 2) Delete the border tile.update_border_visualization(border_id, erase=True)
                    self._delete_border(int(vertex_o), int(vertex_i))

    def _delete_border(self, vertex_o, vertex_i):
        """
        Delete the border of a tile based on the positions of two vertices.

        :param vertex_o: (int) The origin vertex.
        :param vertex_i: (int) The destination vertex.
        :return: None
        """
        # Calculate the row and column positions of the vertices
        row_o, col_o = divmod(vertex_o, self.columns)
        row_i, col_i = divmod(vertex_i, self.columns)

        # Determine the border to be deleted
        if row_o == row_i:  # The vertices are in the same row
            border_id = 2 if col_o < col_i else 3  # Delete left border if vertex_o < vertex_i, else delete right border
        else:  # The vertices are in the same column
            border_id = 0 if row_o < row_i else 1  # Delete upper border if vertex_o < vertex_i, else delete bottom
            # border

        # Get the tile and delete the border
        tile = self.list_tiles[vertex_o]
        tile.update_border_visualization(border_id, state=False)

    def get_tile(self, row, column):
        """
        Get a specific tile from the list_tiles list.
        :param row: (int) The row position of the tile.
        :param column: (int) The column position of the tile.
        :return: (Tile) The Tile object at the specified position.
        """
        index = row * self.columns + column
        return self.list_tiles[index]


if __name__ == '__main__':
    maze = Labyrinth(2, 3)
    maze.get_board()
    maze.window.after(5000, maze.update_maze)
    maze.window.mainloop()
