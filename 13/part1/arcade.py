from intcode_computer import IntcodeComputer

class ArcadeCabinet:
	def __init__(self, file=None, echo=True):
		if file is None:
			self.computer = IntcodeComputer(echo=echo)
		else:
			self.computer = IntcodeComputer(file, echo=echo)

		self.width, self.height = 0, 0
		self.grid = []

	def run(self):
		self.computer.execute_program()
		output = self.computer.get_output_values()
		for i in range(0, len(output), 3):
			x = output[i]
			y = output[i+1]
			tile = output[i+2]

			self.set_tile(x, y, tile)

		self.print_grid()
		print('Number Blocks: %d' % self.count_blocks())

	def set_tile(self, x, y, tile):
		if not self.in_bounds(x, y):
			self.expand_grid(x+1, y+1)

		self.grid[x][y] = tile

	def in_bounds(self, x, y):
		if x >= self.width or y >= self.height:
			return False
		else:
			return True

	def expand_grid(self, new_width, new_height):
		if new_width > self.width:
			add_width = new_width - self.width
			for i in range(add_width):
				self.grid.append([0 for tile in range(self.height)])
			self.width = new_width

		if new_height > self.height:
			add_height = new_height - self.height
			for column in self.grid:
				column.extend([0 for tile in range(add_height)])
			self.height = new_height

	def print_grid(self):
		for y in range(self.height):
			for x in range(self.width):
				tile = self.grid[x][y]
				print(tile, end='')
			print('\n', end='')

	def count_blocks(self):
		block_count = 0
		for y in range(self.height):
			for x in range(self.width):
				tile = self.grid[x][y]
				if tile == 2:
					block_count += 1
		return block_count

if __name__ == '__main__':
	input_file = './input.txt'
	arcade = ArcadeCabinet(input_file, echo=False)
	arcade.run()