
def read_routes_from_file(filename):
    file = open(filename, "r")

    lines = list()

    for line in file:
        lines.append(line.strip())

    file.close()

    def divide_lines(line):
        return line.split(',')

    def parse_route(route):
        return (route[3], route[5])

    def filter_null_nodes(node):
        return (node[0] != '\\N') and (node[1] != '\\N')

    routes = list(
        filter(filter_null_nodes,
               map(parse_route,
                   map(divide_lines, lines))))

    return routes
