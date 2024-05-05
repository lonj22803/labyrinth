# README

## Labyrinth Project

This project is a Python application that creates and updates a labyrinth based on the information in a JSON file. The labyrinth is represented as a grid of tiles, and each tile can have walls on its borders. The labyrinth is drawn using the Tkinter library.

## Dependencies

- Python 3.6 or higher
- Tkinter

## How to Use

### Labyrinth Class

The `Labyrinth` class is used to create and update the labyrinth. Here's how to use it:

1. Initialize a new instance of the `Labyrinth` class. The constructor takes two arguments: the number of rows and the number of columns in the labyrinth.

```python
maze = Labyrinth(2, 3)
```

2. Generate the board for the labyrinth by calling the `get_board` method. This method creates a list of `Tile` objects, one for each cell in the labyrinth, and draws each tile on the canvas.

```python
maze.get_board()
```

3. Update the labyrinth based on the information in a JSON file by calling the `update_maze` method. This method reads a JSON file located at '/dev/shm/graph.json', loads the JSON data into a dictionary, and checks the walls in the maze based on this data. If the file does not exist, it prints a message indicating this. After checking the walls, the method schedules itself to be called again after 300 milliseconds. This allows the maze to be updated in real time as the JSON file changes.

```python
maze.window.after(5000, maze.update_maze)
```

4. Start the Tkinter event loop by calling the `mainloop` method on the `window` attribute. This method will keep the window open until it is closed by the user.

```python
maze.window.mainloop()
```

### JSON File

The JSON file should be located at '/dev/shm/graph.json' and should have the following structure:

```json
{
    "V": {
        "0": ["1", "3"],
        "1": ["0", "2"],
        "2": ["1"],
        "3": ["0"]
    },
    "E": {
        "(0, 1)": 0,
        "(0, 3)": 1,
        "(1, 0)": 0,
        "(1, 2)": 1,
        "(2, 1)": 1,
        "(3, 0)": 1
    }
}
```

In this JSON file, `"V"` is a dictionary that represents the vertices in the labyrinth. Each key is a vertex, and the value is a list of vertices that are connected to the key vertex.

`"E"` is a dictionary that represents the edges in the labyrinth. Each key is a string representation of a tuple that contains two vertices, and the value is an integer that represents the state of the wall between the two vertices. If the value is 0, there is a wall between the vertices. If the value is 1, there is no wall between the vertices.

## Running the Application

To run the application, navigate to the project directory and run the `labyrinth.py` file:

```bash
python labyrinth.py
```

This will open a new window that displays the labyrinth. The labyrinth will be updated in real time as the JSON file changes.