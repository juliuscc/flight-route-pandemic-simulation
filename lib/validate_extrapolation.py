import matplotlib.cm as cm
import matplotlib
import math
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np

import extrapolate_flow_of_passengers as extr

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
passengerSet = dataset

# Read routes and airport information information
data = pd.read_csv("input/airports.dat", header=-1)
airport_data_frame = pd.DataFrame(data, columns=[1, 4]).rename(
    columns={1: "Name", 4: "Code"})
airport_data_frame = airport_data_frame[airport_data_frame.Code != "\\N"]

airports = {}
for index, row in airport_data_frame.iterrows():
    airports[row['Code']] = row['Name']

data = pd.read_csv("input/routes.dat", header=-1)
routes = pd.DataFrame(data, columns=[2, 4]).rename(
    columns={2: "From", 4: "To"})

# Convert it to a format that graphX reads and load the dataset into it
tuples = [tuple(x) for x in routes.values]

G = nx.Graph()
G.add_edges_from(tuples)

for node in G.nodes():
    G.add_node(node, name=airports.get(node))


def convert(name):
    """Lookup the normalized value for any airport or return 0"""
    airport = passengerSet[passengerSet.Code == name]
    if (len(airport.Code) > 0):
        return airport.iat[0, 1]
    else:
        return 0


# Create values for each of the nodes in the graph based on passenger
# density
extrapolatedValueFun = extr.extrapolateValueFunc()

degree = np.array([node for _, node in G.degree()])

value = np.array([convert(node) for node in G.nodes()])
extrVal = np.array([extrapolatedValueFun(node) for _, node in G.degree()])

# Drop 0 values here
cleanRaw = [(d, v) for d, v, _ in zip(degree, value, extrVal) if v != 0]
cleanValues = list(zip(*cleanRaw))
realX = np.array(cleanValues[0])
realY = np.array(cleanValues[1])

cleanRaw = [(d, e) for d, v, e in zip(degree, value, extrVal) if v == 0]
cleanValues = list(zip(*cleanRaw))
simX = np.array(cleanValues[0])
simY = np.array(cleanValues[1])


with open("results/validate-flow-data-real.dat", "w") as f:
    for locX, locY in zip(realX, realY):
        f.write("%s %s\n" % (locX, locY))

with open("results/validate-flow-data-sim.dat", "w") as f:
    for locX, locY in zip(simX, simY):
        f.write("%s %s\n" % (locX, locY))

plt.scatter(realX, realY, c="red")
plt.scatter(simX, simY, c="blue")
plt.show()
