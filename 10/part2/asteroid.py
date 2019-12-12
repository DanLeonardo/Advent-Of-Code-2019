from math import atan2, sqrt

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

def find_asteroid_angles(base_asteroid, asteroid_list, size):
	width, height = size
	base_x, base_y = get_coord(base_asteroid, width)

	print('Finding angles from Asteroid %d at (%d, %d)' % (base_asteroid, base_x, base_y))
	asteroids_relative = []
	for asteroid in asteroid_list:
		asteroid_x, asteroid_y = get_coord(asteroid, width)
		dist_x = asteroid_x - base_x
		dist_y = asteroid_y - base_y

		theta = atan2(dist_y, dist_x)
		distance = sqrt(dist_x*dist_x + dist_y*dist_y)

		# print('Asteroid %d (%d, %d) has angle %f at distance %f' % (asteroid,asteroid_x, asteroid_y, theta, distance))
		if dist_x == 0 and dist_y == 0:
			continue
		else:
			asteroids_relative.append((asteroid, theta, distance))

	asteroids_by_angle = {}
	for asteroid_info in asteroids_relative:
		pos = asteroid_info[0]
		theta = asteroid_info[1]
		distance = asteroid_info[2]

		if theta not in asteroids_by_angle:
			# Create a new list with the angle as key
			asteroids_by_angle[theta] = []
			asteroids_by_angle[theta].append((pos, distance))
		else:
			# Insert the asteroid and distance into the list sorted by distance
			# insert_index = -1
			# for i, aster in enumerate(asteroids_by_angle[theta]):
			# 	aster_dist = aster[1]
			# 	if distance < aster_dist:
			# 		insert_index = i
			# asteroids_by_angle[theta].insert(insert_index, (pos, distance))
			asteroids_by_angle[theta].append((pos, distance))

	# Sort asteroids_by_angle for each key
	for theta in asteroids_by_angle:
		asteroids_by_angle[theta].sort(key=lambda asteroid: asteroid[1])

	return asteroids_by_angle




input_file = './input.txt'
test1_file = './test1.txt'

asteroid_map, size = read_asteroid_map(input_file)
width, height = size
asteroid_list = find_asteroids(asteroid_map, size)

# Find most visible asteroid
most_visible = 0
base_asteroid = -1
for i in range(len(asteroid_list)):
	visible = count_visible_asteroids(asteroid_list[i], asteroid_list, size)

	if visible > most_visible:
		most_visible = visible
		base_asteroid = asteroid_list[i]

coord = get_coord(base_asteroid, width)
print('Asteroid %d at (%d, %d) sees %d' % (base_asteroid, coord[0], coord[1], most_visible))

# Find angles and distances of all asteroids
asteroid_angles = find_asteroid_angles(base_asteroid, asteroid_list, size)

# for key in asteroid_angles:
# 	print('Angle %f' % key)
# 	for asteroid in asteroid_angles[key]:
# 		print('%d at %f' % (asteroid[0], asteroid[1]))

angle_list = [angle for angle in asteroid_angles]
angle_list.sort()

angle_up = atan2(-1, 0)

for i, angle in enumerate(angle_list):
	if angle >= angle_up:
		angle_index = i
		break

asteroids_destroyed = 0
target_asteroids_destroyed = 200
last_asteroid_destroyed = None

while True:
	# Set angle_index to 0 if it surpassed the list of angle
	if angle_index >= len(angle_list):
		angle_index = 0

	angle = angle_list[angle_index]
	last_asteroid_destroyed = asteroid_angles[angle].pop(0)
	asteroids_destroyed += 1

	if asteroids_destroyed >= target_asteroids_destroyed:
		print('%d destroyed asteroid is %d' % (asteroids_destroyed, last_asteroid_destroyed[0]))
		break

	angle_index += 1

last_coord = get_coord(last_asteroid_destroyed[0], width)
print(last_coord[0] * 100 + last_coord[1])