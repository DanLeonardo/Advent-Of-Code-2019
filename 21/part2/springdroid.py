from intcode_computer import IntcodeComputer

class SpringdroidInterface:
	def __init__(self, file_str):
		self.computer = IntcodeComputer(file_str, echo=False)

	def run(self):
		walk = 'WALK\n'
		run = 'RUN\n'

		# Example: jump if a thre-tile-wide hole is detected
		# NOT A J
		# NOT B T
		# AND T J
		# NOT C T
		# AND T J
		# AND D J

		# GOAL: (!C && D & (E || H)) || A || (!B && !E)

		# Translate instructions into ASCII
		instructions = ['NOT C J', 'AND D J', 'NOT H T', 'NOT T T', 'OR E T', 'AND T J', 'NOT A T', 'OR T J', 'NOT B T', 'NOT T T', 'OR E T', 'NOT T T', 'OR T J']
		instructions.append(run)
		input_str = '\n'.join([step for step in instructions])
		print(input_str)
		
		# Input instructions and run computer
		# Print output
		self.computer.read_ascii(input_str)
		output = self.computer.get_output()
		# output = ''.join([chr(char) for char in self.computer.get_output()[:-1]])

		for char in output:
			if char > 255:
				break
			print(chr(char), end='')
		print('\n', end='')
		print(output[-1])


if __name__ == '__main__':
	spring = SpringdroidInterface('./input.txt')
	spring.run()