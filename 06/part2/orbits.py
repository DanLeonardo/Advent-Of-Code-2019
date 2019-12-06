class OrbitalGrid:
    def __init__(self,  input_file=None):
        self.orbits = None
        if input_file is not None:
            self.load_orbits(input_file)
            print(self.orbits)

    def load_orbits(self, input_file):
        with open(input_file) as file:
            self.orbits = {}
            for line in file.readlines():
                orbitals = line.strip(' ')
                orbitals = orbitals.strip('\n')
                orbitals = orbitals.split(')')
                # orbitals.reverse()
                # orbits.append(orbitals)

                # Set to neighbor
                if orbitals[0] in self.orbits:
                    self.orbits[orbitals[0]].append(orbitals[1])
                else:
                    self.orbits[orbitals[0]] = [orbitals[1]]
                # Set from neighbor
                if orbitals[1] in self.orbits:
                    self.orbits[orbitals[1]].append(orbitals[0])
                else:
                    self.orbits[orbitals[1]] = [orbitals[0]]

    def BFS(self, source, dest):
        # Mark nodes undiscovered
        discovered_list = {}
        for key in self.orbits:
            discovered_list[key] = False

        # Path list
        path_list = {}

        # Mark source node discovered
        discovered_list[source] = True

        node_list = [source]
        while len(node_list) > 0:
            node = node_list.pop(0)
            print('Searching %s' % node)
            # Found destination
            if node == dest:
                break

            # Check all neighbors
            for edge in self.orbits[node]:
                if not discovered_list[edge]:
                    discovered_list[edge] = True
                    path_list[edge] = node
                    node_list.append(edge)

        # Print path to node
        final_path = []
        cur_node = dest
        while cur_node is not source:
            next_node = path_list[cur_node]
            # print('%s -> %s' % (cur_node, path_list[cur_node]))
            final_path.append((next_node, cur_node))
            cur_node = next_node

        final_path.reverse()
        print(final_path)
        print(len(final_path))

if __name__ == '__main__':
    grid = OrbitalGrid('./input.txt')
    grid.BFS('YOU', 'SAN')
