from intcode_computer import IntcodeComputer
import time

# print([_ for _ in range(0)])

beam_field = []
computer = IntcodeComputer('./input.txt', echo=False)

def get_beam_point(x, y):
	height = len(beam_field)
	if y >= height:
		print('get_beam_point: %d out of range.')

	row = beam_field[y]
	offset = row[0]
	length = row[1]

	if x < offset or x >= offset + length:
		return 0
	else:
		return 1

def read_point(x, y):
	global computer

	computer.reset()
	computer.set_input([x, y])
	computer.run()
	return computer.get_last_value()

def read_row(start_x, y):
	global beam_field

	x = start_x
	if x < 0:
		x = 0
	left = -1
	while True:
		output = read_point(x, y)
		# print('(%d, %d) %d' % (x, y, output))
		if output == 0:
			if left >= 0:
				length = x - left
				beam_field.append((left, length))
				break
			elif x >= y * 2:
				beam_field.append((-1, 0))
				break
		else:
			if left < 0:
				left = x
		x += 1

def print_beam_field():
	global beam_field

	for y, row in enumerate(beam_field):
		offset = row[0]
		length = row[1]

		print('%d: ' % y, end='')
		for x in range(0, offset):
			print('.', end='')
		for x in range(length):
			print('#', end='')
		print('\n', end='')

def read_beam_field(start_y, stop_y):
	global beam_field

	# if start_y > 0:
	# 	for _ in range(start_y):
	# 		beam_field.append((-1, -1))

	left = -1
	for y in range(start_y, stop_y):
		# if y % 10 == 0:
		# 	print('Reading Row %d' % y)

		if left > 0:
			x = left - 1
			left = -1
		else:
			x = 0
			left = -1

		read_row(x, y)

def fit_area(width, height):
	global beam_field

	start = -1
	for i, row in enumerate(beam_field):
		length = row[1]
		if length >= height:
			start = i
			break

	if start != -1:
		y = start
		while y < len(beam_field):
			row = beam_field[y]
			offset = row[0]
			length = row[1]

			if length >= width:
				# Check that every column underneath the right edge is also full of 1's
				# work our way left until we fail or reach offset
				# keep track of the leftmost x if any the area can fit

				# (3, 4)		OFF:	LENGTH:
				# ...######...	3		6
				# ..#####.....	2		5
				# ....#######.	4		7
				# ....###.....	4		3

				# range(offset, offset+length-width)
				# range(3, 6)
				for col in range(offset, offset+length-width+1):
					# check height-1 beneath in range(col,col+height+1)
					area_fit = True
					for check_y in range(y, y+height):
						if check_y >= len(beam_field):
							area_fit = False
							break

						if not check_row(col, col+width-1, check_y):
							area_fit = False
							break
					if area_fit:
						return (col, y)

			y += 1

	return None

# (4, 6)
# 0 2 4 6 8 0 2 4
# ....######.....
#      ^^^
# check_row(5,7)
# 
# offset <= start
# length >= stop - start + 1
# stop <= offset + length - 1

# 4 <= 5
# 6 >= 7 - 5
# 7 <= 4 + 6 - 1
	
def check_row(start, stop, y):
	global beam_field

	row = beam_field[y]
	offset = row[0]
	length = row[1]

	if offset > start:
		return False
	if length < stop - start + 1:
		return False
	if stop > offset + length - 1:
		return False
	return True

if __name__ == '__main__':
	fit_x, fit_y = 100, 100
	# pos = fit_area(fit_x, fit_y)
	# if pos:
	# 	print('%dx%d fits at %s' % (fit_x, fit_y, pos))
	# else:
	# 	print('%dx%d does not fit in area.' % (fit_x, fit_y))

	cur_row = 1500
	step = fit_y
	max_row = 2000
	pos = None

	beam_field.extend([(-1, -1) for _ in range(cur_row)])

	while not pos and cur_row < max_row:
		print('Reading rows %d - %d' % (cur_row, cur_row + step-1))
		read_beam_field(cur_row, cur_row+step)
		cur_row += step

		pos = fit_area(fit_x, fit_y)

	# print_beam_field()
	print('%dx%d fits at %s' % (fit_x, fit_y, pos))