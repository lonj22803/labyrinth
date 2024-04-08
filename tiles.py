"""
Module to define the Tile class used as basic unit into the labyrinth

2024
"""

import tkinter as tk


class Tile:
    def __init__(self, pos_x=0, pos_y=0):
        self.position = (pos_x, pos_y)
        # Represent borders as: [Top, bottom, left, right]
        self.borders = [True, True, True, True]

    def draw(self, sketch: tk.Canvas, length=10, width=5):

        # Draw the background color for the tile
        sketch.create_rectangle(
            self.position[0], self.position[1], self.position[0] + length, self.position[1] + length, fill='lightblue',
            outline='')

        for i in range(len(self.borders)):
            # Line coords get a 4 element tuple: (x_i, y_i, x_f, y_f)
            line_coords = self._get_line_coords(i, length)  # Get coordinates for the current border

            if self.borders[i]:
                sketch.create_line(line_coords[0], line_coords[1], line_coords[2], line_coords[3], width=width)
            else:
                sketch.create_line(
                    line_coords[0], line_coords[1], line_coords[2], line_coords[3], fill='white', width=width
                )

    def _get_line_coords(self, border_id, length):

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


if __name__ == '__main__':
    # Create window
    window = tk.Tk()
    window.title("Baldosas")
    # Define window's size
    window.geometry("500x550")
    window.configure(bg='dark gray')
    # Create Canvas
    width = 500
    height = 500
    canvas = tk.Canvas(window, bg="light gray", height=height, width=width)
    canvas.pack()

    step_y = height // 5  # 5 is the tiles amount
    step_x = width // 5

    for i in range(5):
        for j in range(5):
            tile = Tile(j * step_x, i * step_y)
            tile.draw(canvas, length=step_x, width=1)

    window.mainloop()
