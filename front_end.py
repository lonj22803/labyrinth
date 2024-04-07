"""
Modulo que ejecuta el front end para visualizar la solucion al laberinto
"""

import tkinter as tk


class Laberinto:
    def __init__(self):
        pass

    @staticmethod
    def draw_line(lienzo: tk.Canvas, x, y, orientacion="v", largo=50, relleno="black"):
        if orientacion == "h":
            linea = lienzo.create_line(x, y, x + largo, y, fill=relleno, width=5)
        else:
            linea = lienzo.create_line(x, y, x, y + largo, fill=relleno, width=5)
        return linea


if __name__ == '__main__':
    # Create window
    window = tk.Tk()
    window.title("Laberinto")
    # Define window's size
    window.geometry("500x550")
    # Create Canvas
    canvas = tk.Canvas(window, bg="light gray", height=500, width=500)
    canvas.pack()
    Laberinto.draw_line(canvas, 0, 0)
    Laberinto.draw_line(canvas, 0, 0, orientacion="h")

    window.mainloop()
