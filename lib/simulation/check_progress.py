

class SEIRData:
    susceptible = 0
    exposed = 0
    infectious = 0
    recovered = 0

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return (
            self.susceptible == other.susceptible and
            self.exposed == other.exposed and
            self.infectious == other.infectious and
            self.recovered == other.recovered
        )

    def __ne__(self, other):
        """Override the default Not equal behavior"""
        return (
            other == None or
            self.susceptible != other.susceptible or
            self.exposed != other.exposed or
            self.infectious != other.infectious or
            self.recovered != other.recovered
        )

    def __str__(self):
        return f"{self.susceptible} {self.exposed} {self.infectious} {self.recovered}"


def collect_SEIR_state_sum(graph):
    dataItem = SEIRData()

    for node_id in graph.nodes:
        data_item = graph.nodes[node_id]
        dataItem.susceptible += data_item['susceptible']
        dataItem.exposed += data_item['exposed']
        dataItem.infectious += data_item['infectious']
        dataItem.recovered += data_item['recovered']

    return dataItem


def normalize_SEIR_data(seirData: SEIRData):
    sum = (seirData.susceptible +
           seirData.exposed +
           seirData.infectious +
           seirData.recovered)

    factor = 1 / sum

    normalizedData = SEIRData()

    normalizedData.susceptible = seirData.susceptible * factor
    normalizedData.exposed = seirData.exposed * factor
    normalizedData.infectious = seirData.infectious * factor
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
