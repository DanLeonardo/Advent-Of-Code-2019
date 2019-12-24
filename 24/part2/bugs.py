import copy

class GameOfBugs:
	def __init__(self, grid=None, size=None):
		self.init_grid = grid
		self.width = len(self.init_grid)
		self.height = len(self.init_grid[0])

		self.grids = {0: copy.deepcopy(self.init_grid)}


	def generate_grid(self):
		new_grid = []
		for y in range(self.height):
			for x in range(self.width):
				if y == 0:
					new_grid.append(['.'])
				else:
					new_grid[x].append('.')

		new_grid[2][2] = '?'
		return new_grid

	def print_grid(self, level):
		grid = self.grids[level]
		for y in range(self.height):
			for x in range(self.width):
				tile = grid[x][y]
				print(tile, end='')
			print('\n', end='')

	def print_levels(self):
		levels = [key for key in self.grids]
		levels.sort()
		
		for level in levels:
			if self.count_bugs_in_level(level) == 0:
				continue
			else:
				print('Depth %d:' % level)
				self.print_grid(level)
				print('\n', end='')
				
	def get_tile(self, x, y, level):
		if level not in self.grids:
			# self.register_grid(self.generate_grid(), level)
			self.grids[level] = self.generate_grid()

		if x >= 0 and x < self.width and y >= 0 and y < self.height:
			grid = self.grids[level]
			return grid[x][y]
		else:
			# print('get_tile: (%d, %d) %d is out of range' % (x, y, level))
			return '?'

	def count_bugs(self):
		bugs = 0
		levels = [key for key in self.grids.keys()]
		levels.sort()
		for level in levels:
			bugs += self.count_bugs_in_level(level)
		return bugs

	def count_bugs_in_level(self, level):
		grid = self.grids[level]
		bugs = 0
		for y in range(self.height):
			for x in range(self.width):
				tile = grid[x][y]
				if tile == '#':
					bugs += 1

		return bugs

	def step(self):
		# new_grids = copy.deepcopy(self.grids)
		levels = [key for key in self.grids.keys()]
		levels.sort()

		count_grid = [[0 for y in range(self.height)] for x in range(self.width)]
		bugs_count = {level: copy.deepcopy(count_grid) for level in levels}
		
		for level in levels:
			for y in range(self.height):
				for x in range(self.width):
					tile = self.get_tile(x, y, level)
					# print('(%d, %d) %s:' % (x, y, tile))
					if tile == '#':
						# Left
						if x == 0:
							# Outside
							if level-1 not in bugs_count:
								bugs_count[level-1] = copy.deepcopy(count_grid)
							bugs_count[level-1][1][2] += 1
						elif (x, y) == (3, 2):
							# Inside
							if level+1 not in bugs_count:
								bugs_count[level+1] = copy.deepcopy(count_grid)
							for level_y in range(self.height):
								bugs_count[level+1][self.width-1][level_y] += 1
						else:
							bugs_count[level][x-1][y] += 1

						# Right
						if x == self.width-1:
							# Outside
							if level-1 not in bugs_count:
								bugs_count[level-1] = copy.deepcopy(count_grid)
							bugs_count[level-1][3][2] += 1
						elif (x, y) == (1, 2):
							# Inside
							if level+1 not in bugs_count:
								bugs_count[level+1] = copy.deepcopy(count_grid)
							for level_y in range(self.height):
								bugs_count[level+1][0][level_y] += 1
						else:
							bugs_count[level][x+1][y] += 1

						# Up
						if y == 0:
							# Outside
							if level-1 not in bugs_count:
								bugs_count[level-1] = copy.deepcopy(count_grid)
							bugs_count[level-1][2][1] += 1
						elif (x, y) == (2, 3):
							# Inside
							if level+1 not in bugs_count:
								bugs_count[level+1] = copy.deepcopy(count_grid)
							for level_x in range(self.width):
								bugs_count[level+1][level_x][self.height-1] += 1
						else:
							bugs_count[level][x][y-1] += 1

						# Down
						if y == self.height-1:
							# Outside
							if level-1 not in bugs_count:
								bugs_count[level-1] = copy.deepcopy(count_grid)
							bugs_count[level-1][2][3] += 1
						elif (x, y) == (2, 1):
							# Inside
							if level+1 not in bugs_count:
								bugs_count[level+1] = copy.deepcopy(count_grid)
							for level_x in range(self.width):
								bugs_count[level+1][level_x][0] += 1
						else:
							bugs_count[level][x][y+1] += 1

		# Update levels
		for level in bugs_count:
			for y in range(self.height):
				for x in range(self.width):
					if level not in self.grids:
						self.grids[level] = copy.deepcopy(self.generate_grid())

					tile = self.get_tile(x, y , level)
					count = bugs_count[level][x][y]

					if tile == '#' and count != 1:
						self.grids[level][x][y] = '.'
					elif tile == '.' and count in (1, 2):
						self.grids[level][x][y] = '#'
			

	def run(self, steps):
		for step in range(steps):
			self.step()

		bugs = self.count_bugs()
		return bugs

if __name__ == '__main__':
	test_grid =  [['.', '#', '#', '.', '#'], ['.', '.', '.', '.', '.'], ['.', '.', '?', '#', '.'], ['.', '#', '#', '.', '.'], ['#', '.', '#', '.', '.']]
	input_grid = [['.', '#', '.', '.', '#'], ['#', '#', '.', '#', '.'], ['#', '.', '?', '.', '#'], ['#', '.', '#', '#', '.'], ['.', '.', '#', '.', '#']]

	bugs = GameOfBugs(input_grid)

	bugs.print_levels()
	print('----------\n')

	num_bugs = bugs.run(200)
	bugs.print_levels()
	print(num_bugs)
