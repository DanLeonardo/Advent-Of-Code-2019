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
		idle_markers = [0 for computer in self.computers]
		nat_packet = None
		last_nat_packet = None

		running = True
		while running:
			if all([marker >= 10 for marker in idle_markers]):
				input_queue[0] = [nat_packet[0], nat_packet[1]]
				idle_markers = [0 for computer in self.computers]

				if nat_packet == last_nat_packet:
					return nat_packet
				last_nat_packet = nat_packet

			for i, computer in enumerate(self.computers):
				input = input_queue[i]

				if len(input) > 0:
					computer.read_input(input)
					input.clear()
					idle_markers[i] = 0
				else:
					computer.read_input(-1)
					computer.run()
					idle_markers[i] += 1

				output = computer.get_output()

				while len(output) > 0:
					address = output[0]
					x = output[1]
					y = output[2]

					if address != 255:
						input_queue[address].extend([x, y])
					else:
						nat_packet = (x, y)

					output = output[3:]


if __name__ == '__main__':
	network = Network('./input.txt')
	packet = network.run()
	print(packet)