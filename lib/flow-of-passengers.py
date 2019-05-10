import matplotlib.cm as cm
import matplotlib
import math
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# Read the airport information data.
data = pd.read_excel("input/other-airports.xls", header=2)
data_other = pd.DataFrame(data, columns=["Code", "Pax 2017"]).rename(
    columns={"Pax 2017": "Passengers"})

data = pd.read_excel("input/american-airport.xls",
                     header=2, sheet_name="2017 pax")
data_america = pd.DataFrame(data, columns=["Code", "Pax 2016"]).rename(
    columns={"Pax 2016": "Passengers"})

data = pd.read_excel("input/european-airports.xls", header=2)
data_europe = pd.DataFrame(data, columns=["Code", "Pax 2017"]).rename(
    columns={"Pax 2017": "Passengers"})

# Create the combined dataset
dataset = data_other.append(data_america).append(data_europe)

# Drop nil and sort
dataset = dataset.dropna()
dataset = dataset.sort_values(by=["Code"])

# Normalize the passenger column
max_passengers = dataset['Passengers'].max()
dataset["Passengers"] = dataset["Passengers"] / max_passengers

passengerSet = dataset

# Read routes and airport information information
data = pd.read_csv("input/airports.dat", header=-1)
airports = pd.DataFrame(data, columns=[0, 4]).rename(
    columns={0: "Id", 4: "Code"})
airports = airports[airports.Code != "\\N"]

data = pd.read_csv("input/routes.dat", header=-1)
routes = pd.DataFrame(data, columns=[2, 4]).rename(
    columns={2: "From", 4: "To"})

# Convert it to a format that graphX reads and load the dataset into it
tuples = [tuple(x) for x in routes.values]

G = nx.Graph()
G.add_edges_from(tuples)


def convert(name):
    """Lookup the normalized value for any airport or return 0"""
    airport = passengerSet[passengerSet.Code == name]
    if (len(airport.Code) > 0):
        return airport.iat[0, 1]
    else:
        return 0


# Create values for each of the nodes in the graph based on passenger
# density
value = [math.sqrt(convert(node)) for node in G.nodes()]


# Extract max degree from graph
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
maxd = degree_sequence[0]

# Normalize the degree for each node (sqrt might not be needed...)
centr_val = [math.sqrt(node / maxd) for _, node in G.degree()]

# Zip the values from passenger flow and degree together.
# For those values that only have degree, value degree higher.
comb_val = [(v + cv) / 2 if v != 0.0 else cv for v,
            cv in zip(value, centr_val)]

# Create a colormapper.
norm = matplotlib.colors.Normalize(vmin=0, vmax=1, clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap=cm.inferno_r)

# Create colors from the values in rage [0,1]
comb_col = [mapper.to_rgba(c) for c in comb_val]

# Plot the graph.
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color=comb_col,
                       cmap=plt.get_cmap('jet'), node_size=15)  #
# nx.draw_networkx_labels(G, pos)
# nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=False)
plt.show()
