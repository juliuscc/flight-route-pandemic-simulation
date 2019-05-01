
def read_airports_from_file(filename):
    file = open(filename, "r")

    lines = list()

    for line in file:
        lines.append(line.strip())

    file.close()

    def divide_lines(line):
        line = line.split(',')

        for i in range(len(line)):
            line[i] = line[i].strip('"')

        return line

    def parse_airports(airport): # 1 = id, 2 = airport name, 3 = city, 4 = country
        return (airport[0], airport[1], airport[2], airport[3])


    airports = list(map(parse_airports, map(divide_lines, lines)))


    airportDict = {}
    for i in range(len(airports)):
        airportDict[airports[i][0]] = (airports[i][1], airports[i][2], airports[i][3])

    print(airportDict['1'])
    return airportDict

read_airports_from_file("../input/airports.dat")