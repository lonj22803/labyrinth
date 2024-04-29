"""
Module to define the Tile class used as basic unit into the labyrinth

2024
"""

import tkinter as tk


class Tile:
    def __init__(self, sketch: tk.Canvas, pos_x=0, pos_y=0, length=100):
        self.canvas = sketch
        self.position = (pos_x, pos_y)
        self._length = length
        # Represent borders as: [Top, bottom, left, right]
        self.borders = [True, True, True, True]
        self.turtle = False  # If True, draw a turtle in the current tile to simulate de player move
        self.turtle_image = self._get_turtle_image()  # Image as instance attribute to avoid python garbage collection
        self.turtle_orientation = 'r'  # Define turtle orientation: r: right, l: left, u: up, d: down
        # TODO: makes turtle_orientation useful

    def _get_turtle_image(self):
        # c_size = self.canvas.winfo_reqwidth() - 2  # Canvas is always a square (height = width)
        # TODO: path selection based on canvas size and turtle size selection
        turtle_img_path = "resources/turtle_47px.png"
        return tk.PhotoImage(file=turtle_img_path)

    def draw(self, width=5, bg='lightblue'):
        # ---------------------------------------------------------------------
        # Still working on turtle draw method organization
        # ---------------------------------------------------------------------

        # Draw the background color for the tile
        self.canvas.create_rectangle(
            self.position[0], self.position[1], self.position[0] + self._length, self.position[1] + self._length,
            fill=bg,
            outline='')
        # Draw the turtle over the tile background
        if self.turtle:
            self._draw_turtle()

        for k in range(len(self.borders)):
            # Line coords get a 4 element tuple: (x_i, y_i, x_f, y_f)
            line_coords = self._get_line_coords(k, width)  # Get coordinates for the current border

            if self.borders[k]:
                self.canvas.create_line(line_coords[0], line_coords[1], line_coords[2], line_coords[3], width=width)
            else:
                self.canvas.create_line(
                    line_coords[0], line_coords[1], line_coords[2], line_coords[3], fill='white', width=width)

    def _get_line_coords(self, border_id: int, width: int):

        if border_id == 0:  # Top border
            x_init = self.position[0]
            y_init = self.position[1]
            x_final = x_init + self._length
            y_final = y_init
        elif border_id == 1:  # Draw bottom border
            x_init = self.position[0]
            y_init = self.position[1] + self._length
            x_final = x_init + self._length
            y_final = y_init
        elif border_id == 2:  # Draw left border
            x_init = self.position[0]
            y_init = self.position[1]
            x_final = x_init
            y_final = y_init + self._length
        else:  # Draw right border
            x_init = self.position[0] + self._length
            y_init = self.position[1]
            x_final = x_init
            y_final = y_init + self._length

        return x_init, y_init, x_final, y_final

    def _draw_turtle(self):
        pos_x = self.position[0] + self._length // 4
        pos_y = self.position[1] + self._length // 4
        self.canvas.create_image(pos_x, pos_y, image=self.turtle_image, anchor=tk.NW)


# def array_tiles(sketch: tk.Canvas, cv_size: int, tiles_amount: int, wall_width=1, mode='run'):
#     """
#
#     :param sketch: Tkinter canvas to draw the tiles.
#     :param cv_size: [int] canvas border size (it assumes that canvas is a square).
#     :param tiles_amount: [int] tiles amount per row and column.
#     :param wall_width: [int] border width for every tile.
#     :param mode:
#     :return: [list] a list with every tile
#     """
#     tile_length = cv_size // tiles_amount
#     # Need to compensate the width space
#     tiles = list()
#     for m in range(tiles_amount):
#         for n in range(tiles_amount):
#             tile_mn = Tile(n * tile_length, m * tile_length)
#             tile_mn.draw(sketch, length=tile_length, width=wall_width)
#             tiles.append(tile_mn)
#
#     return tiles


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
    # Estos me dan el tamaño del canvas + 2
    # print("Using method 1: ")
    # print(canvas.winfo_reqwidth())
    # print(canvas.winfo_reqheight())
    tile = Tile(canvas, 0, 0, length=100)
    tile.turtle = True
    tile.draw(width=5)
    # array_tiles(canvas, canvas_size, 5)
    # print("using Method 2:")
    # window.update() # Tener presente a futuro
    # # Estos me dan el tamanho de la ventana
    # print(canvas.winfo_height())
    # print(canvas.winfo_width())

    window.mainloop()
