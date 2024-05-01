"""
Module to define the Tile class used as basic unit into the labyrinth

2024
"""

import tkinter as tk


class Tile:
    def __init__(self, sketch: tk.Canvas, pos_x=0, pos_y=0, length=100, width=5):
        self.border_width = width
        self.canvas = sketch
        self.position = (pos_x, pos_y)
        self._length = length
        # Represent borders as: [Top, bottom, left, right]
        self.borders = [True, True, True, True]
        self.borders_ID = [None, None, None, None]
        self.turtle = False  # If True, draw a turtle in the current tile to simulate de player move
        self.turtle_image = self._get_turtle_image()  # Image as instance attribute to avoid python garbage collection
        self.turtle_orientation = 'r'  # Define turtle orientation: r: right, l: left, u: up, d: down
        # TODO: makes turtle_orientation useful
        self.bg_ID = None

    def _get_turtle_image(self):
        # Determine the size of the canvas
        c_size = self.canvas.winfo_reqwidth() - 2  # Canvas is always a square (height = width)
        # Select an appropriate image size for the turtle based on the size of the canvas
        if c_size > 500:
            turtle_img_size = "100px"
        elif c_size > 300:
            turtle_img_size = "75px"
        else:
            turtle_img_size = "50px"

        turtle_img_path = f"resources/turtle_{turtle_img_size}.png"
        return tk.PhotoImage(file=turtle_img_path)

    def draw(self, bg='lightblue', turtle=False):
        """
        This method draws the tile on the canvas. It first draws the background color for the tile,
        then draws the turtle if it exists, and finally draws the borders of the tile.

        :param bg: (str) The background color of the tile. Default is 'lightblue'.
        :param turtle: (bool) If True, a turtle is drawn on the tile. Default is False.
        """

        # Draw the background color for the tile
        # The create_rectangle method of the canvas is used to draw the background of the tile.
        # The position of the tile and its length are used to determine the coordinates of the rectangle.
        # The fill parameter is used to set the color of the rectangle, and the outline parameter is set to '' to
        # remove the outline.
        # Draw the background color for the tile
        self.bg_ID = self.canvas.create_rectangle(
            self.position[0], self.position[1], self.position[0] + self._length, self.position[1] + self._length,
            fill=bg,
            outline='')
        # Draw the turtle over the tile background
        self.turtle = turtle
        if self.turtle:
            self._draw_turtle()

        # Draw the borders of the tile
        # The borders are drawn by iterating over the borders attribute, which is a list of booleans representing
        # whether each border exists.
        # For each border, the _get_line_coords method is called to get the coordinates of the border line.
        # If the border exists (the corresponding element in the borders list is True), the create_line method of the
        # canvas is used to draw the border.
        # If the border does not exist (the corresponding element in the borders list is False), the create_line
        # method is used to draw a white line, effectively erasing the border.
        for k in range(len(self.borders)):
            # Line coords get a 4 element tuple: (x_i, y_i, x_f, y_f)
            line_coords = self._get_line_coords(k)  # Get coordinates for the current border

            if self.borders[k]:
                self.borders_ID[k] = self.canvas.create_line(line_coords[0], line_coords[1], line_coords[2],
                                                             line_coords[3],
                                                             width=self.border_width)
            else:
                self.borders_ID[k] = self.canvas.create_line(line_coords[0], line_coords[1], line_coords[2],
                                                             line_coords[3], fill='white',
                                                             width=self.border_width)

    def update_bg_color(self, color: str):
        """
        This method updates the background color of the tile.
        :param color: (str) The new color for the background of the tile.
        """
        # Delete the existing rectangle
        self.canvas.delete(self.bg_ID)

        # Draw a new rectangle with the specified color
        self.bg_ID = self.canvas.create_rectangle(
            self.position[0], self.position[1], self.position[0] + self._length, self.position[1] + self._length,
            fill=color,
            outline=''
        )

    def update_border_visualization(self, border_id: int, state: bool):
        """
        This method updates the visualization of a border in the canvas.
        :param border_id: (int): The id of the border to be updated. The id corresponds to the following borders:
                              0 - Top border
                              1 - Bottom border
                              2 - Left border
                              3 - Right border
        :param state: (bool): The state of the border (True for existing, False for non-existing).
        """
        try:
            self.borders[border_id] = state
        except ValueError:
            raise ValueError('Border ID have to be an int between [0, 3].')

        self.canvas.delete(self.borders_ID[border_id])
        line_coords = self._get_line_coords(border_id)

        if self.borders[border_id]:
            self.borders_ID[border_id] = self.canvas.create_line(line_coords[0], line_coords[1], line_coords[2],
                                                                 line_coords[3], width=self.border_width)
        else:
            self.borders_ID[border_id] = self.canvas.create_line(line_coords[0], line_coords[1], line_coords[2],
                                                                 line_coords[3], fill='white', width=self.border_width)

    def _get_line_coords(self, border_id: int):
        """
        This method calculates the coordinates for borders of a given tile.
        :param border_id: (int): The id of the border for which the coordinates are to be calculated.
                              The id corresponds to the following borders:
                              0 - Top border
                              1 - Bottom border
                              2 - Left border
                              3 - Right border
        :return: tuple: A tuple containing the initial and final coordinates (x_init, y_init, x_final, y_final) of the
        border line.
        """

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

    def rotate_turtle(self, direction: str):
        """
        This method rotates the turtle based on the given direction.
        :param direction: (str) The direction to rotate the turtle.
                          It can be 'r' for right, 'l' for left, 'u' for up, and 'd' for down.
        """
        if direction in ['r', 'l', 'u', 'd']:
            self.turtle_orientation = direction
        else:
            raise ValueError("Invalid direction. It must be 'r' for right, 'l' for left, 'u' for up, or 'd' for down.")

    def _draw_turtle(self):
        """
        This method draws a turtle on the tile. The turtle is positioned at the center of the tile.

        The turtle's position is calculated as the tile's position plus a quarter of the tile's length
        (both horizontally and vertically), which places the turtle at the center of the tile.

        The turtle's image is created on the canvas at the calculated position, with its top-left corner
        anchored at the calculated position. The ID of the turtle image on the canvas is stored in the
        `turtle_ID` attribute for future reference (e.g., to erase the turtle when needed).
        """
        pos_x = self.position[0] + self._length // 4
        pos_y = self.position[1] + self._length // 4
        self.turtle_ID = self.canvas.create_image(pos_x, pos_y, image=self.turtle_image, anchor=tk.NW)

        # # Rotate the turtle image based on the turtle_orientation attribute
        # if self.turtle_orientation == 'r':
        #     self.canvas.itemconfig(self.turtle_ID, image=self.turtle_image.rotate(-90))
        # elif self.turtle_orientation == 'l':
        #     self.canvas.itemconfig(self.turtle_ID, image=self.turtle_image.rotate(90))
        # elif self.turtle_orientation == 'u':
        #     self.canvas.itemconfig(self.turtle_ID, image=self.turtle_image.rotate(180))

    def change_turtle_state(self, erase=True):
        """
        This method changes the state of the turtle on the tile.

        If 'erase' is True, it removes the turtle from the tile by deleting the turtle's image from the canvas.
        If 'erase' is False, it draws the turtle on the tile.

        :param erase: (bool) If True, the turtle is removed from the tile. If False, the turtle is drawn on the tile.
                      Default is True.
        """
        if erase:
            if self.turtle:  # Check if the turtle exists before trying to delete it
                self.canvas.delete(self.turtle_ID)
                self.turtle = False
        else:
            self._draw_turtle()
            self.turtle = True


def array_tiles(sketch: tk.Canvas, cv_size: int, tiles_amount: int):
    """

    :param sketch: Tkinter canvas to draw the tiles.
    :param cv_size: [int] canvas border size (it assumes that canvas is a square).
    :param tiles_amount: [int] tiles amount per row and column.
    :return: [list] a list with every tile with a row-major order
    """
    tile_length = cv_size // tiles_amount
    # Need to compensate the width space
    tiles = list()
    for m in range(tiles_amount):
        for n in range(tiles_amount):
            tile_mn = Tile(sketch, n * tile_length, m * tile_length, length=tile_length)
            tile_mn.draw()
            if m == 0 and n == 0:
                tile_mn.change_turtle_state(erase=False)

            tiles.append(tile_mn)

    return tiles


if __name__ == '__main__':
    # Create window
    window = tk.Tk()
    window.title("Tiles")
    # Define window's size
    window.geometry("500x500")
    window.configure(bg='dark gray')
    window.resizable(False, False)
    # Create Canvas
    canvas_size = 1000
    canvas = tk.Canvas(window, bg="light gray", height=canvas_size, width=canvas_size)
    canvas.pack()
    tiles_array = array_tiles(canvas, canvas_size, 20)
    # tile = Tile(canvas, 0, 0, length=100)
    # tile.turtle = True
    #
    # tile.draw()
    # tile.update_border(3, True)
    # array_tiles(canvas, canvas_size, 5)
    # print("using Method 2:")
    # print(canvas.winfo_height())
    # print(canvas.winfo_width()
    window.mainloop()
