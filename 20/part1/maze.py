class Maze:
	def __init__(self, file_str=None):
		self.map = None
		if file_str is not None:
			self._read_maze(file_str)

	def solve(self):
		if self.map is None:
			return

		self._find_markers()

		self.print_maze()
		self.print_markers()

		start = self.markers['AA'][0]
		stop = self.markers['ZZ'][0]
		print('Start: (%d, %d)' % (start[0], start[1]))
		print('Stop:  (%d, %d)' % (stop[0], stop[1]))

		path = self._bfs(start, stop)
		print(len(path))

	def _read_maze(self, file_str):
		self.map = []
		x, y = 0, 0
		with open(file_str) as file:
			for line in file:
				x = 0
				if y == 0:
					self.map = [[tile] for tile in line.strip('\n')]
				else:
					for tile in line.strip('\n'):
						self.map[x].append(tile)
						x += 1
				y += 1
		self.width = len(self.map)
		self.height = len(self.map[0])

	def _bfs(self, start, stop=None):
		if self.map is None:
			return None

		nodes = [start]
		parents = [[None for h in range(self.height)] for w in range(self.width)]

		while nodes != []:
			node = nodes.pop(0)
			node_x, node_y = node

			if stop and node == stop:
				break

			# Add every portal location that has not been visited to nodes
			portals = self._get_portal(node_x, node_y)
			if portals:
				for portal in portals:
					if portal != node:
						portal_x, portal_y = portal
						if parents[portal_x][portal_y] is None:
							parents[portal_x][portal_y] = node
							nodes.append(portal)

			# Check Up
			u_node = self._get_tile(node_x, node_y-1)
			if u_node == '.' and parents[node_x][node_y-1] is None:
				parents[node_x][node_y-1] = node
				nodes.append((node_x, node_y-1))

			# Check Down
			d_node = self._get_tile(node_x, node_y+1)
			if d_node == '.' and parents[node_x][node_y+1] is None:
				parents[node_x][node_y+1] = node
				nodes.append((node_x, node_y+1))

			# Check Left
			l_node = self._get_tile(node_x-1, node_y)
			if l_node == '.' and parents[node_x-1][node_y] is None:
				parents[node_x-1][node_y] = node
				nodes.append((node_x-1, node_y))

			# Check Right
			r_node = self._get_tile(node_x+1, node_y)
			if r_node == '.' and parents[node_x+1][node_y] is None:
				parents[node_x+1][node_y] = node
				nodes.append((node_x+1, node_y))

		if stop:
			node = stop
			path = []
			while node != start:
				path.insert(0, node)
				node_x, node_y = node
				node = parents[node_x][node_y]
			return path
		else:
			return parents

	def _get_tile(self, x, y):
		if x < 0 or x >= self.width or y < 0 or y >= self.height:
			return None
		else:
			return self.map[x][y]

	def _get_portal(self, x, y):
		if x < 0 or x >= self.width or y < 0 or y >= self.height:
			return None

		for marker in self.markers:
			positions = self.markers[marker]
			if (x, y) in positions:
				return positions

		return None

	def _find_markers(self):
		self.markers = {}

		x, y = 0, 0
		for y in range(self.height):
			for x in range(self.width):
				tile = self._get_tile(x, y)

				if tile >= 'A' and tile <= 'Z':
					marker = tile
					d_tile = self._get_tile(x, y+1)
					r_tile = self._get_tile(x+1, y)					

					if r_tile and r_tile >= 'A' and r_tile <= 'Z':
						marker += r_tile
						if marker not in self.markers:
							self.markers[marker] = []

						if self._get_tile(x-1, y) == '.':
							self.markers[marker].append((x-1, y))
						elif self._get_tile(x+2, y) == '.':
							self.markers[marker].append((x+2, y))
					elif d_tile and d_tile >= 'A' and d_tile <= 'Z':
						marker += d_tile
						if marker not in self.markers:
							self.markers[marker] = []

						if self._get_tile(x, y-1) == '.':
							self.markers[marker].append((x, y-1))
						elif self._get_tile(x, y+2) == '.':
							self.markers[marker].append((x, y+2))

	def print_maze(self):
		if self.map is None:
			return

		x, y = 0, 0
		for y in range(self.height):
			for x in range(self.width):
				tile = self._get_tile(x, y)
				print(tile, end='')
			print('\n', end='')

	def print_markers(self):
		for marker in self.markers:
			print('%s: ' % marker, end='')
			positions = self.markers[marker]
			for i, pos in enumerate(positions):
				if i:
					print(', ', end='')
				print('(%d, %d)' % (pos[0], pos[1]), end='')
			print('\n', end='')


if __name__ == '__main__':
	input_file = './input.txt'
	test1_file = './test1.txt'

	maze = Maze(input_file)
	maze.solve()