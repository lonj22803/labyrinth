"""
Module to define the Tile class used as basic unit into the labyrinth

2024
"""

import tkinter as tk
from PIL import Image, ImageTk  # For show turtle image and handle it


class Tile:
    def __init__(self, pos_x=0, pos_y=0):
        """

        :param pos_x:
        :param pos_y:
        """
        self.position = (pos_x, pos_y)
        # Represent borders as: [Top, bottom, left, right]
        self.borders = [True, True, True, True]
        self.turtle = False  # If True, draw a turtle in the current tile to simulate de player move
        self.turtle_orientation = 'r'  # Define turtle orientation: r: right, l: left, u: up, d: down

    def draw(self, sketch: tk.Canvas, length=10, width=5, bg='lightblue'):
        """

        :param sketch:
        :param length:
        :param width:
        :param bg:
        :return:
        """
        # Draw the turtle over the tile background
        # ---------------------------------------------------------------------
        # Still working on turtle draw method organization
        # ---------------------------------------------------------------------
        if self.turtle:
            turtle_size = length - length // 3
            self._draw_turtle(sketch, size=turtle_size)

        # Draw the background color for the tile
        sketch.create_rectangle(
            self.position[0], self.position[1], self.position[0] + length, self.position[1] + length, fill=bg,
            outline='')

        for k in range(len(self.borders)):
            # Line coords get a 4 element tuple: (x_i, y_i, x_f, y_f)
            line_coords = self._get_line_coords(k, length, width)  # Get coordinates for the current border

            if self.borders[k]:
                sketch.create_line(line_coords[0], line_coords[1], line_coords[2], line_coords[3], width=width)
            else:
                sketch.create_line(
                    line_coords[0], line_coords[1], line_coords[2], line_coords[3], fill='white', width=width)

    def _get_line_coords(self, border_id: int, length: int, width: int):
        """

        :param border_id:
        :param length:
        :return:
        """
        if border_id == 0:  # Top border
            x_init = self.position[0]
            y_init = self.position[1]
            x_final = x_init + length
            y_final = y_init
        elif border_id == 1:  # Draw bottom border
            x_init = self.position[0]
            y_init = self.position[1] + length
            x_final = x_init + length
            y_final = y_init
        elif border_id == 2:  # Draw left border
            x_init = self.position[0]
            y_init = self.position[1]
            x_final = x_init
            y_final = y_init + length
        else:  # Draw right border
            x_init = self.position[0] + length
            y_init = self.position[1]
            x_final = x_init
            y_final = y_init + length

        return x_init, y_init, x_final, y_final

    def _draw_turtle(self, sketch, size=10):
        turtle_img_path = "resources/turtle.png"
        turtle_img = Image.open()
        pass


def array_tiles(sketch: tk.Canvas, cv_size: int, tiles_amount: int, wall_width=1, mode='run'):
    """

    :param sketch: Tkinter canvas to draw the tiles.
    :param cv_size: [int] canvas border size (it assumes that canvas is a square).
    :param tiles_amount: [int] tiles amount per row and column.
    :param wall_width: [int] border width for every tile.
    :param mode:
    :return: [list] a list with every tile
    """
    tile_length = cv_size // tiles_amount
    # Need to compensate the width space
    tiles = list()
    for m in range(tiles_amount):
        for n in range(tiles_amount):
            tile_mn = Tile(n * tile_length, m * tile_length)
            tile_mn.draw(sketch, length=tile_length, width=wall_width)
            tiles.append(tile_mn)

    return tiles


if __name__ == '__main__':
    # Create window
    window = tk.Tk()
    window.title("Tiles")
    # Define window's size
    window.geometry("500x550")
    window.configure(bg='dark gray')
    window.resizable(False, False)
    # Create Canvas
    canvas_size = 500
    canvas = tk.Canvas(window, bg="light gray", height=canvas_size, width=canvas_size)
    canvas.pack()  # side=tk.LEFT)
    tile = Tile(0, 0)
    tile.turtle = True
    tile.draw(canvas, 200, width=5)
    # array_tiles(canvas, canvas_size, 5)

    window.mainloop()
