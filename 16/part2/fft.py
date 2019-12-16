def phase_signal(input, freq, num_phases):
	signal = str(input)
	# print(signal)

	for phase in range(num_phases):
		if phase % 1 == 0:
			print('Phase %d' % phase)
			
		# output = []
		# for i in range(len(signal)):
			# output.append(calculate_digit(signal, freq, i))

		output = ['' for _ in signal]
		for i in range(len(signal)-1, -1, -1):
			if i == len(signal) - 1:
				output[i] = signal[i]
			else:
				output[i] = str((int(signal[i]) + int(output[i+1])) % 10)

		signal = ''.join(output)
		# print(signal)

	return signal

def calculate_digit(input, freq, digit):
	# print('Digit %d' % digit)
	i = 1

	results = []
	for e in input:
		if i // (digit+1) >= len(freq):
			i = 0

		# print('%d * %d' % (int(e), freq[i // (digit+1)]))
		results.append(int(e) * freq[i // (digit+1)])
		i += 1

	return str(sum(results))[-1]

if __name__ == '__main__':
	test_files = ['./test1.txt', './test2.txt', './test3.txt']
	input_file = './input.txt'

	base_freq = [0, 1, 0, -1]

	with open(input_file) as file:
		input = file.read().strip('\n')
		input = ''.join(input for _ in range(10000))
		offset = int(input[0:7])
		input = input[offset:]

	# input = 12345678
	output = phase_signal(input, base_freq, 100)
	print(output[0:8])