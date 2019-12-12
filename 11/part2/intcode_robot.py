from intcode_computer import IntcodeComputer

class PaintingRobot:
	def __init__(self, input_file=None, echo=True):
		if input_file:
			self.computer = IntcodeComputer(input_file, echo=echo)
		else:
			self.computer = IntcodeComputer(echo=echo)

		# 0 UP, 1 RIGHT, 2 DOWN, 3 LEFT
		self.direction = 0
		self.position = (0, 0)
		self.painted_tiles = {}
		self.echo = echo

	def run(self):
		self.paint_tile(self.position, 1)

		running = True
		while running:
			color = self.get_tile_color(self.position)
			self.computer.set_input([color])
			self.computer.execute_program()
			output = self.computer.get_output_values()

			self.paint_tile(self.position, output[0])
			if output[1] == 0:
				self.rotate_left()
			elif output[1] == 1:
				self.rotate_right()
			else:
				print('Error: Invalid rotation direction')
				break

			self.move_forward()

			if self.computer.finished:
				running = False

				print('Robot is finished')
				num_tiles = len(self.painted_tiles)
				print('Num tiles painted %d' % num_tiles)

	def rotate_left(self):
		self.direction -= 1
		if self.direction < 0:
			self.direction = 3

		if self.echo:
			print('Rotating Left. New direction %d' % self.direction)

	def rotate_right(self):
		self.direction += 1
		if self.direction > 3:
			self.direction = 0

		if self.echo:
			print('Rotating Right. New direction %d' % self.direction)

	def move_forward(self):
		move_x, move_y = 0, 0

		if self.direction == 0:
			move_y = -1
		elif self.direction == 1:
			move_x = 1
		elif self.direction == 2:
			move_y = 1
		elif self.direction == 3:
			move_x = -1

		pos_x, pos_y = self.position
		self.position = pos_x + move_x, pos_y + move_y

		if self.echo:
			print('Moving to position (%d, %d)' % (self.position[0], self.position[1]))

	def get_tile_color(self, tile_pos):
		if tile_pos not in self.painted_tiles:
			return 0
		else:
			return self.painted_tiles[tile_pos]

	def paint_tile(self, tile_pos, color):
		self.painted_tiles[tile_pos] = color

		if self.echo:
			print('Painting tile (%d, %d) color %d' % (tile_pos[0], tile_pos[1], color))

	def output_tiles(self):
		min_x, max_x = None, None
		min_y, max_y = None, None
		for key in self.painted_tiles:
			if min_x is None or key[0] < min_x:
				min_x = key[0]
			if max_x is None or key[0] > max_x:
				max_x = key[0]

			if min_y is None or key[1] < min_y:
				min_y = key[1]
			if max_y is None or key[1] > max_y:
				max_y = key[1]

		for y in range(min_y, max_y+1):
			for x in range(min_x, max_x+1):
				pos = x, y

				if pos in self.painted_tiles and self.painted_tiles[pos] == 1:
					print('#', end='')
				else:
					print(' ', end='')
			print('\n', end='')

if __name__ == '__main__':
	input_file = './input.txt'

	robot = PaintingRobot(input_file, echo=False)
	robot.run()
	robot.output_tiles()