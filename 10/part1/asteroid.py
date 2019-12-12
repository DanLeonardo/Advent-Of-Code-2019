from math import atan2

def get_coord(pos, width):
	x = pos % width
	y = pos // width
	return (x, y)

def get_pos(coord, width):
	x, y = coord
	return x + y * width

def read_asteroid_map(file_str):
	asteroid_map = []
	with open(file_str) as file:
		file_lines = file.readlines()
		width = len(file_lines[0].strip('\n'))
		height = len(file_lines)

		for line in file_lines:
			asteroid_map.extend([tile for tile in line.strip('\n')])

	return (asteroid_map, (width, height))


def print_asteroid_map(asteroid_map, size):
	width, height = size
	for y in range(0, height):
		for x in range(0, width):
			pos = get_pos((x, y), width)
			print(asteroid_map[pos], end='')
		print('\n', end='')

def find_asteroids(asteroid_map, size):
	width, height = size
	asteroid_list = []
	for y in range(0, height):
		for x in range(0, width):
			pos = get_pos((x, y), width)
			if asteroid_map[pos] == '#':
				asteroid_list.append(pos)
	return asteroid_list

def count_visible_asteroids(asteroid_pos, asteroid_list, size):
	width, height = size
	# visible_asteroids = [True for _ in range(0, len(asteroid_list))]
	asteroid_angles = []
	base_x, base_y = get_coord(asteroid_pos, width)

	for asteroid in asteroid_list:
		asteroid_x, asteroid_y = get_coord(asteroid, width)
		dist_x = asteroid_x - base_x
		dist_y = asteroid_y - base_y
		theta = atan2(dist_y, dist_x)

		# print('(%d, %d)' % (dist_x, dist_y))
		# print(theta)

		if dist_x == 0 and dist_y == 0:
			continue
		else:
			if theta not in asteroid_angles:
				asteroid_angles.append(theta)
	
	return len(asteroid_angles)	


input_file = './input.txt'
test1_file = './test1.txt'

asteroid_map, size = read_asteroid_map(input_file)
width, height = size
asteroid_list = find_asteroids(asteroid_map, size)

print(size)

most_visible = 0
most_visible_asteroid = -1

for i in range(len(asteroid_list)):
	visible = count_visible_asteroids(asteroid_list[i], asteroid_list, size)

	if visible > most_visible:
		most_visible = visible
		most_visible_asteroid = asteroid_list[i]

coord = get_coord(most_visible_asteroid, width)

print('Asteroid %d at (%d, %d) sees %d' % (most_visible_asteroid, coord[0], coord[1], most_visible))
