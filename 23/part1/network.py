from intcode_computer import IntcodeComputer

class Network:
	def __init__(self, file_str):
		self.file_str = file_str

	def setup_network_addresses(self):
		for i, computer in enumerate(self.computers):
			computer.read_input(i)

	def run(self):
		self.computers = [IntcodeComputer(self.file_str, echo=False) for _ in range(50)]
		self.setup_network_addresses()

		input_queue = [[] for computer in self.computers]

		running = True
		while running:
			for i, computer in enumerate(self.computers):
				input = input_queue[i]
				if len(input) > 0:
					computer.read_input(input)
					input.clear()
				else:
					computer.read_input(-1)
					computer.run()

				output = computer.get_output()

				while len(output) > 0:
					address = output[0]
					x = output[1]
					y = output[2]

					if address != 255:
						input_queue[address].extend([x, y])
						output = output[3:]
					else:
						return (x, y)


if __name__ == '__main__':
	network = Network('./input.txt')
	packet = network.run()
	print(packet)