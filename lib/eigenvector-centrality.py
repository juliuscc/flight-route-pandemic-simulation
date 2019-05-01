import math
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from read import read_routes_from_file

routes = read_routes_from_file("input/routes.dat")

shortRoutes = []
# for item in range(0, 1000):
#     shortRoutes.append(routes[item])

G = nx.DiGraph()
G.add_edges_from(routes)

eigencentrality = nx.eigenvector_centrality(G)
centrality = [math.sqrt(c) for v, c in eigencentrality.items()]
# print(centrality)
# G.add_edges_from(shortRoutes)

# val_map = {'A': 1.0,
#            'D': 0.5714285714285714,
#            'H': 0.0}

minimum = min(centrality)
maximum = max(centrality)

print(minimum)
print(maximum)

norm = matplotlib.colors.Normalize(vmin=minimum, vmax=maximum, clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap=cm.inferno_r)

values = [mapper.to_rgba(c) for c in centrality]

# values = [val_map.get(node, 0.25) for node in G.nodes()]

# Specify the edges you want here
# red_edges = [('A', 'C'), ('E', 'C')]
# edge_colours = ['black' if not edge in red_edges else 'red'
#                 for edge in G.edges()]
# black_edges = [edge for edge in G.edges()]

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color=values, cmap=plt.get_cmap(
    'jet'), node_size=20)  #
# nx.draw_networkx_labels(G, pos)
# nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=False)
plt.show()
