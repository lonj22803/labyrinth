"""
Module to draw a labyrinth from an array using Tkinter

2024
"""

import tkinter as tk


class Labyrinth:
    def __init__(self, sketch: tk.Canvas):
        self.canvas = sketch

    def _draw_line(self, x: int, y: int, orientation="v", length=50, fill="black"):
        """

        :param x:
        :param y:
        :param orientation:
        :param length:
        :param fill:
        :return:
        """
        if orientation == "h":
            linea = self.canvas.create_line(x, y, x + length, y, fill=fill, width=5)
        else:
            linea = self.canvas.create_line(x, y, x, y + length, fill=fill, width=5)
        return linea

    def draw_borders(self):
        pass


if __name__ == '__main__':
    pass
