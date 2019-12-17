from intcode_computer import IntcodeComputer

class ScaffoldInterface:
	def __init__(self, file_str=None):
		self.computer = IntcodeComputer(file_str, echo=False)
		self.scaffolding = None

	def run(self):
		self.computer.program[0] = 2
		self.computer.run()
		output = self.computer.get_output_values()
		# self.print_output(output)
		# self.save_output(output, './map.txt')
		self.save_scaffolding(output)
		self.find_path()

		# Main Routine
		routine_main = [ord(char) for char in 'B\n']
		# Function A
		routine_A = [ord(char) for char in 'R,8,L,8,R,6\n']
		# Function B
		routine_B = [ord(char) for char in 'L,9,1,L,8\n']
		# Function C
		routine_C = [ord(char) for char in 'L,8\n']

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

		print('%d, %d' % (cur_x, cur_y))
		# Directions ^ v < >
		cur_dir = '^'

		while True:
			# Walk cursor along path
			pass

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