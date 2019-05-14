import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib
import math
import networkx as nx
import pandas as pd


def extrapolateValueFunc():
    """Create a function that can be used to predict number of passengers from
    the degree of any node in the network."""
    (x, y) = _extrapolateFlow()  # not real x and y values. they need to be remapped
    linReg = _getLineRegFunc(x, y)
    return _getValueFunc(linReg)


def _extrapolateFlow():
    """This function reads the dataset and maps x values to y values such that a linear
    relationship is formed."""
    # Movement data
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

    dataset = data_other.append(data_america).append(data_europe)

    # dataset[dataset['Code'].isnull()]
    dataset = dataset.dropna()
    dataset = dataset.sort_values(by=["Code"])

    dataset["Passengers"] = dataset["Passengers"]

    passengerSet = dataset

    # Airports and routes

    data = pd.read_csv("input/routes.dat", header=-1)
    routes = pd.DataFrame(data, columns=[2, 4]).rename(
        columns={2: "From", 4: "To"})

    # Creating network graph

    tuples = [tuple(x) for x in routes.values]

    G = nx.Graph()
    G.add_edges_from(tuples)

    def lookupNode(name):
        airport = passengerSet[passengerSet.Code == name]
        if (len(airport.Code) > 0):
            return airport.iat[0, 1]
        else:
            return 0

    passengerFlow = [lookupNode(node) for node in G.nodes()]

    # Getting degree values

    centr_val = [node for _, node in G.degree()]

    flowDegree = [(flow, degree) for flow, degree in zip(
        passengerFlow, centr_val) if (flow != 0)]

    flowDegreeList = list(zip(*flowDegree))

    xPoints = [math.log((x+math.e)) for x in flowDegreeList[1]]  # Degree
    yPoints = [math.log((y))
               for y in flowDegreeList[0]]  # Number of passengers

    x = np.array(xPoints)
    y = np.array(yPoints)

    return (x, y)


def _getLineRegFunc(x, y):
    """This function creates a linear regression between the points"""
    def inner(x1):
        return m * x1 + b

    m = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / \
        (len(x)*np.sum(x*x) - np.sum(x) * np.sum(x))
    b = (np.sum(y) - m * np.sum(x)) / len(x)

    # print(f"linreg = a*x + b = {m}*x+{b}")

    return inner


def _getValueFunc(linReg):
    def inner(x1):
        # modulate the values in the same way
        # as we did above
        # add e to x and then take log of that value
        modulatedX = math.log(x1 + math.e)

        # Output Oy is on the for log(y) => real y = e^Oy
        realY = pow(math.e, linReg(modulatedX))
        return realY
    return inner


# Create the plot and write to file.
if (__name__ == '__main__'):
    print("running")
    (x, y) = _extrapolateFlow()

    maxX = np.max(x)
    minX = np.min(x)

    linReg = _getLineRegFunc(x, y)

    distX = maxX - minX
    xRange = np.array([minX + x * distX/100 for x in range(100)])

    with open("results/flow-data-scatter.dat", "w") as f:
        for locX, locY in zip(x, y):
            f.write("%s %s\n" % (locX, locY))

    with open("results/flow-data-linreg.dat", "w") as f:
        for locX, locY in zip(xRange, linReg(xRange)):
            f.write("%s %s\n" % (locX, locY))

    plt.ylabel("ln(#passengers per year)")
    plt.xlabel("ln(degree + e)")

    plt.scatter(x, y)
    plt.plot(xRange, linReg(xRange), color="red")
    plt.show()
