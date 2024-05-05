"""
This script creates an example graph and a solution for the graph. The graph is saved as a json file in /dev/shm (ram).
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

# Generate a solution example for the graph
# This is a directed graph, 'f' represents the incident node for the final node
G_SOL = {0: 1, 1: 4, 4: 5, 5: 'f'}  # The solution is the path: 0 -> 1 -> 4 -> 5 -> 'f'

# Save the solution as a json file in /dev/shm (ram)
with open('/dev/shm/sol_graph.json', 'w') as f:
    json.dump(G_SOL, f, indent=4)
print(G_SOL)
f.close()

