from intcode_computer import IntcodeComputer

class ScaffoldInterface:
	def __init__(self, file_str=None):
		self.computer = IntcodeComputer(file_str, echo=False)

	def run(self):
		self.computer.run()
		output = self.computer.get_output_values()

		self.scaffolding = [[]]
		for tile in output:
			if tile == 10:
				self.scaffolding.append([])
				# print('\n', end='')
			else:
				self.scaffolding[-1].append(tile)
				# print(chr(tile), end='')
		self.scaffolding = self.scaffolding[0:-2]

		self.print_scaffolding()
		self.count_intersections()

	def print_scaffolding(self):
		height = len(self.scaffolding)
		width = len(self.scaffolding[0])
		# print('%d, %d' % (width, height))

		for y in range(height):
			for x in range(width):
				tile = self.scaffolding[y][x]
				print(chr(tile), end='')
			print('\n', end='')

	def count_intersections(self):
		height = len(self.scaffolding)
		width = len(self.scaffolding[0])

		intersections = []
		for y in range(height):
			for x in range(width):
				tile = self.scaffolding[y][x]

				if chr(tile) is not '#':
					print('%s is not #' % tile)
					continue

				if y > 0 and chr(self.scaffolding[y-1][x]) is not '#':
					continue
				if y < height-1 and chr(self.scaffolding[y+1][x]) is not '#':
					continue
				if x > 0 and chr(self.scaffolding[y][x-1]) is not '#':
					continue
				if x < width-1 and chr(self.scaffolding[y][x+1]) is not '#':
					continue

				intersections.append((x, y))

		intersection_alignment_sum = 0
		for intersection in intersections:
			intersection_alignment_sum += intersection[0] * intersection[1]

		print(intersection_alignment_sum)

if __name__ == '__main__':
	interface = ScaffoldInterface('./input.txt')
	interface.run()