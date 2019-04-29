file = open("./input/routes.dat", "r")

lines = list()

for line in file:
    lines.append(line.strip())

file.close()


def divide_lines(line):
    return line.split(',')


def parse_route(route):
    return (route[3], route[5])


routes = list(map(parse_route, map(divide_lines, lines)))

print(lines[0])
print(routes[0])
