class GameOfBugs:
	def __init__(self, file_str):
		self.read_grid(file_str)

	def read_grid(self, file_str):
		with open(file_str) as file:
			self.grid = []
			y = 0
			for line in file.readlines():
				for x, char in enumerate(line.strip('\n')):
					if y == 0:
						self.grid.append([char])
					else:
						self.grid[x].append(char)
				y += 1

			self.layouts = [[x[:] for x in self.grid]]
			self.width = len(self.grid)
			self.height = len(self.grid[0])

	def print_grid(self):
		for y in range(self.height):
			for x in range(self.width):
				print(self.grid[x][y], end='')
			print('\n', end='')

	def get_tile(self, x, y):
		if x >= 0 and x < self.width and y >= 0 and y < self.height:
			return self.grid[x][y]
		else:
			return None

	def count_bugs(self, x, y):
		bugs = 0
		if self.get_tile(x, y-1) == '#':
			bugs += 1
		if self.get_tile(x, y+1) == '#':
			bugs += 1
		if self.get_tile(x-1, y) == '#':
			bugs += 1
		if self.get_tile(x+1, y) == '#':
			bugs += 1

		return bugs

	def step(self):
		new_grid = []

		for y in range(self.height):
			for x in range(self.width):
				tile = self.get_tile(x, y)
				bugs = self.count_bugs(x, y)

				# print('(%d, %d) %s: %d bugs' % (x, y, tile, bugs))

				if y == 0:
					new_grid.append([tile])
				else:
					new_grid[x].append(tile)

				if tile == '#':
					if bugs != 1:
						new_grid[x][y] = '.'
				elif tile == '.':
					if bugs in (1, 2):
						new_grid[x][y] = '#'

		self.layouts.append([x[:] for x in new_grid])
		self.grid = new_grid

		if self.grid in self.layouts[:-1]:
			return True
		else:
			return False

	def rate_biodiversity(self):
		total_value = 0
		for y in range(self.height):
			for x in range(self.width):
				if self.get_tile(x, y) == '#':
					tile_num = x + y*self.width
					total_value += pow(2, tile_num)

		return total_value


if __name__ == '__main__':
	bugs = GameOfBugs('./input.txt')
	
	print('Initial state:')
	bugs.print_grid()

	while True:
		result = bugs.step()

		if result:
			break

	score = bugs.rate_biodiversity()
	print(score)