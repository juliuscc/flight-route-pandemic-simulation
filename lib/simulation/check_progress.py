

class SEIRData:
    susceptible = 0
    exposed = 0
    infected = 0
    recovered = 0

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return (
            self.susceptible == other.susceptible and
            self.exposed == other.exposed and
            self.infected == other.infected and
            self.recovered == other.recovered
        )

    def __ne__(self, other):
        """Override the default Not equal behavior"""
        return (
            self.susceptible != other.susceptible or
            self.exposed != other.exposed or
            self.infected != other.infected or
            self.recovered != other.recovered
        )


def collect_SEIR_state_sum(graph):
    dataItem = SEIRData()

    for dataItem in graph.nodes.data():
        # node id = dataItem[0]
        # actual data = dataItem[1]
        dataItem.susceptible += dataItem[1]['susceptible']
        dataItem.exposed += dataItem[1]['exposed']
        dataItem.infected += dataItem[1]['infected']
        dataItem.recovered += dataItem[1]['recovered']

    return dataItem


def normalize_SEIR_data(seirData: SEIRData):
    sum = (seirData.susceptible +
           seirData.exposed +
           seirData.infected +
           seirData.recovered)

    factor = 1 / sum

    normalizedData = SEIRData()

    normalizedData.susceptible = seirData.susceptible * factor
    normalizedData.exposed = seirData.exposed * factor
    normalizedData.infected = seirData.infected * factor
    normalizedData.recovered = seirData.recovered * factor

    return normalizedData


def check_progress(graph):
    """[DEPRECATED] Returns the percentage of nodes that are contaminated.
    This function does not work..."""
    num_of_nodes = graph.number_of_nodes()

    def is_contaminated(node):
        return node[1]['contaminated']

    def get_node_id(node):
        return node[0]

    contaminated_nodes = set(
        map(get_node_id, filter(is_contaminated, graph.nodes.data())))

    num_of_contaminated = len(contaminated_nodes)

    percentage = num_of_contaminated/num_of_nodes
    return percentage
