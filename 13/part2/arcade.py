from intcode_computer import IntcodeComputer

class ArcadeCabinet:
	def __init__(self, file=None, echo=True):
		if file is None:
			self.computer = IntcodeComputer(echo=echo)
		else:
			self.computer = IntcodeComputer(file, echo=echo)

		self.width, self.height = 0, 0
		self.grid = []
		self.score = 0
		self.paddle_x = -1

	def run(self):
		running = True
		while running:
			self.computer.execute_program()
			self.read_output()
			self.print_grid()

			ball_pos = self.find_ball()
			paddle_pos = self.find_paddle()

			if ball_pos[0] < paddle_pos[0]:
				move = -1
			elif ball_pos[0] == paddle_pos[0]:
				move = 0
			elif ball_pos[0] > paddle_pos[0]:
				move = 1

			self.move_paddle(move)

			running = not self.computer.finished
		

	def read_output(self):
		output = self.computer.get_output_values()
		for i in range(0, len(output), 3):
			x = output[i]
			y = output[i+1]
			tile = output[i+2]

			if x is -1 and y is 0:
				self.set_score(tile)
			else:
				self.set_tile(x, y, tile)

	def set_tile(self, x, y, tile):
		if not self.in_bounds(x, y):
			self.expand_grid(x+1, y+1)

		self.grid[x][y] = tile

	def set_score(self, score):
		self.score = score

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
				# print(tile, end='')
				if tile == 0:
					print(' ', end='')
				elif tile == 1:
					print('|', end='')
				elif tile == 2:
					print('#', end='')
				elif tile == 3:
					print('-', end='')
				elif tile == 4:
					print('*', end='')
			print('\n', end='')
		print('Score: %d' % self.score)

	def find_ball(self):
		for y in range(self.height):
			for x in range(self.width):
				tile = self.grid[x][y]

				if tile == 4:
					return (x, y)

	def find_paddle(self):
		for y in range(self.height):
			for x in range(self.width):
				tile = self.grid[x][y]

				if tile == 3:
					return (x, y)

	def move_paddle(self, move):
		self.computer.set_input([move])

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