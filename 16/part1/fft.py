def phase_signal(input, freq, num_phases):
	signal = str(input)

	for phase in range(num_phases):
		if phase % 10 == 0:
			print('Phase %d' % phase)
			
		output = []
		for i in range(len(signal)):
			output.append(calculate_digit(signal, freq, i))

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

	input = 59776034095811644545367793179989602140948714406234694972894485066523525742503986771912019032922788494900655855458086979764617375580802558963587025784918882219610831940992399201782385674223284411499237619800193879768668210162176394607502218602633153772062973149533650562554942574593878073238232563649673858167635378695190356159796342204759393156294658366279922734213385144895116649768185966866202413314939692174223210484933678866478944104978890019728562001417746656699281992028356004888860103805472866615243544781377748654471750560830099048747570925902575765054898899512303917159138097375338444610809891667094051108359134017128028174230720398965960712
	output = phase_signal(input, base_freq, 100)
	print(output[0:8])