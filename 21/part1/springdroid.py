from intcode_computer import IntcodeComputer

class SpringdroidInterface:
	def __init__(self, file_str):
		self.computer = IntcodeComputer(file_str, echo=False)

	def run(self):
		# Easier instructions to assemble
		not1j = 'NOT A J'
		not2j = 'NOT B J'
		not3j = 'NOT C J'
		not4j = 'NOT D J'
		andtj = 'AND T J'
		walk = 'WALK\n'

		# Example: jump if a thre-tile-wide hole is detected
		# NOT A J - NOT 1 J
		# NOT B T - NOT 2 T
		# AND T J - AND T J
		# NOT C T - NOT 3 T
		# AND T J - AND T J
		# AND D J - AND 4 J

		# GOAL: (!C && D) || A

		# Translate instructions into ASCII
		instructions = ['NOT C J', 'AND D J', 'NOT A T', 'OR T J']
		instructions.append(walk)
		input_str = '\n'.join([step for step in instructions])
		print(input_str)
		
		# Input instructions and run computer
		# Print output
		self.computer.read_ascii(input_str)
		output = self.computer.get_output()
		# output = ''.join([chr(char) for char in self.computer.get_output()[:-1]])

		print(''.join([chr(char) for char in self.computer.get_output()[:-1]]))
		print(output[-1])


if __name__ == '__main__':
	spring = SpringdroidInterface('./input.txt')
	spring.run()