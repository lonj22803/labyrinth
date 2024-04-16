"""
Modulo que ejecuta el front end para visualizar la solucion al laberinto
"""
import tkinter as tk
from labyrinth import Labyrinth

if __name__ == '__main__':
    # Create window
    window = tk.Tk()
    window.title("Laberinto")
    # Define window's size
    window.geometry("500x550")
    window.configure(bg='dark gray')
    # Create Canvas
    canvas = tk.Canvas(window, bg="light gray", height=500, width=500)
    canvas.pack()

    laberinto = Labyrinth(canvas)

    laberinto._draw_line(0, 0)
    # laberinto._draw_line(0, 0, orientation="h")

    window.mainloop()
