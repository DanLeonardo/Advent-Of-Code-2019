from intcode_computer import IntcodeComputer

class ScaffoldInterface:
	def __init__(self, file_str=None):
		self.computer = IntcodeComputer(file_str, echo=False)
		self.scaffolding = None

	def run(self):
		self.computer.program[0] = 2
		self.computer.run()
		output = self.computer.get_output_values()
		self.print_output(output)
		# self.save_output(output, './map.txt')
		self.save_scaffolding(output)
		self.find_path()

		# Main Routine
		routine_main = [ord(char) for char in 'A,A,B,C,B,C,B,C,B,A\n']
		print('Main Len %d' % len(routine_main))
		# Function A
		routine_A = [ord(char) for char in 'L,10,L,8,R,8,L,8,R,6\n']
		print('A Len %d' % len(routine_A))
		# Function B
		routine_B = [ord(char) for char in 'R,6,R,8,R,8\n']
		print('B Len %d' % len(routine_B))
		# Function C
		routine_C = [ord(char) for char in 'R,6,R,6,L,8,L,10\n']
		print('C Len %d' % len(routine_C))

		# Main:
		self.computer.set_input(routine_main)
		print(routine_main)
		self.computer.run()
		output = self.computer.get_output_values()
		self.print_output(output)

		# Function A:
		self.computer.set_input(routine_A)
		print(routine_A)
		self.computer.run()
		output = self.computer.get_output_values()
		self.print_output(output)

		# Function B:
		self.computer.set_input(routine_B)
		print(routine_B)
		self.computer.run()
		output = self.computer.get_output_values()
		self.print_output(output)

		# Function C:
		self.computer.set_input(routine_C)
		print(routine_C)
		self.computer.run()
		output = self.computer.get_output_values()
		self.print_output(output)


		# Continuous Video Feed?
		in_yes = [ord(char) for char in 'Y,E,S\n']
		in_no = [ord(char) for char in 'N,O\n']

		self.computer.set_input(in_no)
		self.computer.run()
		last_value = self.computer.get_last_value()
		output = self.computer.get_output_values()
		self.print_output(output[:-1])

		print(last_value)

	def save_scaffolding(self, output):
		self.scaffolding = [[]]
		for val in output[:-2]:
			if val == ord('\n'):
				self.scaffolding.append([])
			else:
				self.scaffolding[-1].append(chr(val))
		self.scaffolding = self.scaffolding[:-2]

	def find_path(self):
		height = len(self.scaffolding)
		width = len(self.scaffolding[0])

		for y in range(height):
			for x in range(width):
				tile = self.scaffolding[y][x]
				if tile == '^':
					cur_x, cur_y = x, y

		# print('%d, %d' % (cur_x, cur_y))
		# Directions ^ v < >
		cur_dir = '^'
		path = []

		print('Finding path from (%d, %d)' % (cur_x, cur_y))
		while True:
			# Find direction to trun
			if cur_dir == '^' or cur_dir == 'v':
				if cur_x > 0 and self.scaffolding[cur_y][cur_x-1] == '#':
					if cur_dir == '^':
						# print('L')
						path.append('L')
						cur_dir = '<'
					else:
						# print('R')
						path.append('R')
						cur_dir = '<'
				elif cur_x < width-1 and self.scaffolding[cur_y][cur_x+1] == '#':
					if cur_dir == '^':
						# print('R')
						path.append('R')
						cur_dir = '>'
					else:
						# print('L')
						path.append('L')
						cur_dir = '>'
				else:
					print('Reached the end at (%d, %d) facing %s' % (cur_x, cur_y, cur_dir))
					break
			elif cur_dir == '<' or cur_dir == '>':
				if cur_y > 0 and self.scaffolding[cur_y-1][cur_x] == '#':
					if cur_dir == '<':
						# print('R')
						path.append('R')
						cur_dir = '^'
					else:
						# print('L')
						path.append('L')
						cur_dir = '^'
				elif cur_y < height-1 and self.scaffolding[cur_y+1][cur_x] == '#':
					if cur_dir == '<':
						# print('L')
						path.append('L')
						cur_dir = 'v'
					else:
						# print('R')
						path.append('R')
						cur_dir = 'v'
				else:
					print('Reached the end at (%d, %d) facing %s' % (cur_x, cur_y, cur_dir))
					break
			else:
				print('Error: Invalid direction %s' % cur_dir)

			# Count steps until off scaffolding
			step_x, step_y = 0, 0
			if cur_dir == '^':
				step_y = -1
			elif cur_dir == 'v':
				step_y = 1
			elif cur_dir == '<':
				step_x = -1
			elif cur_dir == '>':
				step_x = 1
			else:
				print('Error: Invalid direction %s' % cur_dir)

			distance = 0
			next_tile = self.scaffolding[cur_y+step_y][cur_x+step_x]
			while next_tile != '.':
				distance += 1
				cur_x += step_x
				cur_y += step_y
				if cur_x + step_x < 0 or cur_x + step_x >= width or cur_y + step_y < 0 or cur_y + step_y >= height:
					next_tile = None
					break

				next_tile = self.scaffolding[cur_y+step_y][cur_x+step_x]
			# print(distance)
			path.append(distance)

		print(path)
		with open('./path.txt', 'w') as file:
			for step in path:
				file.write(str(step))
				file.write(',')

	def print_output(self, output):
		for val in output:
			print(chr(val), end='')

	def save_output(self, output, file_str):
		with open(file_str, 'w') as file:
			for val in output:
				file.write(chr(val))

if __name__ == '__main__':
	interface = ScaffoldInterface('./input.txt')
	interface.run()