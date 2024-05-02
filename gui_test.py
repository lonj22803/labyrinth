"""
Modulo que ejecuta el front end para visualizar la solucion al laberinto
"""
import tkinter as tk
from tiles import Tile


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
            color = 'lightblue'
            if m % 2 != 0:
                color = 'lightgreen'
            tile_mn.draw(bg=color)
            if m == 0 and n == 0:
                tile_mn.rotate_turtle('d')
                tile_mn.change_turtle_state(erase=False)

            tiles.append(tile_mn)

    return tiles


if __name__ == '__main__':
    pass
