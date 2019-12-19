from intcode_computer import IntcodeComputer

if __name__ == '__main__':		
	num_points = 0
	for y in range(50):
		for x in range(50):
			computer = IntcodeComputer('./input.txt', echo=False)
			computer.set_input([x, y])
			computer.run()
			output = computer.get_output_values()
			print(output[0], end='')
			if output[0] == 1:
				num_points += 1
		print('\n', end='')
	print(num_points)