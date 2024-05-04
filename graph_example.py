"""
Este script genera un archvo json con la información de los nodos y aristas de la red de la SE.
"""

import json

# Create a dictionary with the nodes of the graph
vertex_list = {0: [1, 3], 1: [0, 2, 4], 2: [1, 5], 3: [0, 4], 4: [1, 3, 5], 5: [2, 4]}
# Create a dictionary with the weighted edges of the graph
# If edge weight is 0, there is no path between the nodes (the wall exists),
# if edge weight is 1, there is a path between the nodes (the wall does not exist)
edges_list = {'(0, 1)': 1, '(0, 3)': 0, '(1, 2)': 0, '(1, 4)': 1, '(2, 5)': 0, '(3, 4)': 0, '(4, 5)': 1}
# Create a dictionary with the graph
G = {'V': vertex_list, 'E': edges_list}
# Save the graph as a json file in /dev/shm (ram)
with open('/dev/shm/graph.json', 'w') as f:
    json.dump(G, f, indent=4)
print(G)
# Close the file
f.close()
