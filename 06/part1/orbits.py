def read_input(input_file):
    orbits = None
    with open(input_file) as file:
        orbits = {}
        for line in file.readlines():
            orbitals = line.strip(' ')
            orbitals = orbitals.strip('\n')
            orbitals = orbitals.split(')')
            # orbitals.reverse()
            # orbits.append(orbitals)
            if orbitals[0] in orbits:
                orbits[orbitals[0]].append(orbitals[1])
            else:
                orbits[orbitals[0]] = [orbitals[1]]

            if not orbitals[1] in orbits:
                orbits[orbitals[1]] = []

    return orbits

def find_orbit_distances(orbits):
    orbit_distances = {}
    next_nodes = ['COM']
    orbit_distances[next_nodes[0]] = 0

    while len(next_nodes) > 0:
        cur_node = next_nodes.pop(0)

        for node in orbits[cur_node]:
            next_nodes.append(node)
            orbit_distances[node] = orbit_distances[cur_node] + 1

    total_distance = 0
    for key in orbit_distances:
        total_distance += orbit_distances[key]

    return total_distance

if __name__ == '__main__':
    input_file = './input.txt'
    orbits = read_input(input_file)

    distance = find_orbit_distances(orbits)
    print('Total Orbital Distance: %s' % distance)
