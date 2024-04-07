"""
Modulo que ejecuta el front end para visualizar la solucion al laberinto
"""

import tkinter as tk


class Laberinto:
    def __init__(self, lienzo: tk.Canvas):
        self.lienzo = lienzo

    def _draw_line(self, x: int, y: int, orientacion="v", largo=50, relleno="black"):
        """

        :param x:
        :param y:
        :param orientacion:
        :param largo:
        :param relleno:
        :return:
        """
        if orientacion == "h":
            linea = self.lienzo.create_line(x, y, x + largo, y, fill=relleno, width=5)
        else:
            linea = self.lienzo.create_line(x, y, x, y + largo, fill=relleno, width=5)
        return linea

    def draw_borders(self):
        pass


if __name__ == '__main__':
    # Create window
    window = tk.Tk()
    window.title("Laberinto")
    # Define window's size
    window.geometry("500x550")
    # Create Canvas
    canvas = tk.Canvas(window, bg="light gray", height=500, width=500)
    canvas.pack()

    laberinto = Laberinto(canvas)

    laberinto._draw_line(0, 0)
    laberinto._draw_line(0, 0, orientacion="h")

    window.mainloop()
