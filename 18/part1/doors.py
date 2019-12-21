import string
import sys

class DungeonPath:
	def __init__(self, input_str=None):
		self.input_str = input_str
		self.map = None
		# self.door_map = None
		self.doors = None
		self.keys = None
		self.tile_dist = None
		self.entrance = None
		self.key_cache = {}

		self.read_map()

	def read_map(self):
		if self.input_str is None:
			return

		self.map = []
		x, y = 0, 0
		with open(self.input_str) as ifile:
			for line in ifile.readlines():
				x = 0
				for tile in line:
					if tile != '\n':
						if y == 0:
							self.map.append([])
						self.map[x].append(tile)
						x += 1
				y += 1

		self.height = len(self.map[0])
		self.width = len(self.map)

		self.find_entrance()
		self.find_doors()
		self.find_keys()
		# self.mark_tiles()

	def print_map(self):
		if self.map is None:
			return

		for y in range(self.height):
			for x in range(self.width):
				print(self.map[x][y], end='')
			print('\n', end='')

	def count_tiles(self):
		if self.map is None:
			return None

		tile_count = 0
		for y in range(self.height):
			for x in range(self.width):
				tile = self.get_tile(x, y)
				if tile != '#':
					tile_count += 1

		return tile_count

	def find_entrance(self):
		for y in range(self.height):
			for x in range(self.width):
				tile = self.get_tile(x, y)
				if tile == '@':
					self.entrance = (x, y)

	def find_doors(self):
		self.doors = {}
		for y in range(self.height):
			for x in range(self.width):
				tile = self.get_tile(x, y)
				if tile in string.ascii_uppercase:
					self.doors[tile] = (x, y)

	def find_keys(self):
		self.keys = {}
		for y in range(self.height):
			for x in range(self.width):
				tile = self.get_tile(x, y)
				if tile in string.ascii_lowercase:
					self.keys[tile] = (x, y)

	def get_door(self, x, y):
		for door, pos in self.doors.items():
			if pos == (x, y):
				return door
		return None

	def get_key(self, x, y):
		for key, pos in self.keys.items():
			if pos == (x, y):
				return key
		return None

	def get_door_pos(self, id):
		for door, pos in self.doors.items():
			if door == id:
				return pos
		return None

	def get_key_pos(self, id):
		for key, pos in self.keys.items():
			if key == id:
				return pos
		return None

	def get_tile(self, x, y):
		if x < 0 or x >= self.width:
			return None
		if y < 0 or y >= self.height:
			return None

		return self.map[x][y]

	def find_path(self, start, stop):
		if start == '@':
			start_pos = self.entrance
		elif start >= 'a' and start <= 'z':
			start_pos = self.get_key_pos(start)
		elif start >= 'A' and start <= 'Z':
			start_pos = self.get_door_pos(start)
		else:
			print('Invalid start position "%s"' % start)

		if stop == '@':
			stop_pos = self.entrance
		elif stop >= 'a' and stop <= 'z':
			stop_pos = self.get_key_pos(stop)
		elif stop >= 'A' and stop <= 'Z':
			stop_pos = self.get_door_pos(stop)
		else:
			print('Invalid stop position "%s"' % stop)

		# (Node Position, List of needed keys to get to node position from start)
		nodes = [(start_pos, [])]
		parents = [[None for y in range(self.height)] for x in range(self.width)]

		while nodes != []:
			node = nodes.pop(0)
			node_x, node_y = node[0]
			keys = node[1]

			if node[0] == stop_pos:
				break

			# Up
			u_node = self.get_tile(node_x, node_y-1)
			u_keys = [key for key in keys]
			# Tile is not a wall and is not visited
			if u_node != '#' and parents[node_x][node_y-1] is None:
				u_door = self.get_door(node_x, node_y-1)
				# Tile is a door and we have the key or it is not a door
				if u_door:
					u_keys.append(u_door.lower())
					u_keys.sort()

				parents[node_x][node_y-1] = ((node_x, node_y), u_keys)
				nodes.append(((node_x, node_y-1), u_keys))

			# Down
			d_node = self.get_tile(node_x, node_y+1)
			d_keys = [key for key in keys]
			# Tile is not a wall and is not visited
			if d_node != '#' and parents[node_x][node_y+1] is None:
				d_door = self.get_door(node_x, node_y+1)
				# Tile is a door and we have the key or it is not a door
				if d_door:
					d_keys.append(d_door.lower())
					d_keys.sort()

				parents[node_x][node_y+1] = ((node_x, node_y), d_keys)
				nodes.append(((node_x, node_y+1), d_keys))

			# Left
			l_node = self.get_tile(node_x-1, node_y)
			l_keys = [key for key in keys]
			# Tile is not a wall and is not visited
			if l_node != '#' and parents[node_x-1][node_y] is None:
				l_door = self.get_door(node_x-1, node_y)
				# Tile is a door and we have the key or it is not a door
				if l_door:
					l_keys.append(l_door.lower())
					l_keys.sort()

				parents[node_x-1][node_y] = ((node_x, node_y), l_keys)
				nodes.append(((node_x-1, node_y), l_keys))

			# Right
			r_node = self.get_tile(node_x+1, node_y)
			r_keys = [key for key in keys]
			# Tile is not a wall and is not visited
			if r_node != '#' and parents[node_x+1][node_y] is None:
				r_door = self.get_door(node_x+1, node_y)
				# Tile is a door and we have the key or it is not a door
				if r_door:
					r_keys.append(r_door.lower())
					r_keys.sort()

				parents[node_x+1][node_y] = ((node_x, node_y), r_keys)
				nodes.append(((node_x+1, node_y), r_keys))

		node = stop_pos
		node_x, node_y = node
		needed_keys = parents[node_x][node_y][1]
		distance = 0
		path = []
		while node != start_pos:
			distance += 1
			path.append(node)
			node_x, node_y = node
			node = parents[node_x][node_y][0]

		# print('%d, %s' % (distance, str(needed_keys)))

		return (distance, needed_keys)

	def find_key_distances(self):
		self.key_dist = {}

		points = [key for key in self.keys]
		points.append('@')
		points.sort()
		
		for start in points:
			self.key_dist[start] = {}
			for stop in points:
				if start == stop:
					continue

				path = self.find_path(start, stop)
				# self.key_dist[start].append((stop, path))
				self.key_dist[start][stop] = path

		# for point in points:
		# 	print(point)
		# 	for key in self.key_dist[point]:
		# 		path = self.key_dist[point][key]
		# 		print('\t%s, %s' % (key, str(path)))

	def find_all_keys(self, start='@', found_keys=None, cur_dist=0):
		if found_keys is None:
			found_keys = []

		found_keys.sort()
		found_key_str = start + '-' + ''.join(found_keys)
		# print('%s:' % found_key_str, end='\n')

		# Check if we've found a better path before
		if found_key_str in self.key_cache:
			best_dist = self.key_cache[found_key_str]
			if best_dist <= cur_dist:
				return None
			else:
				self.key_cache[found_key_str] = cur_dist
		else:
			self.key_cache[found_key_str] = cur_dist

		# Find needed keys
		needed_keys = []
		for key in self.keys:
			if key not in found_keys:
				needed_keys.append(key)
		needed_keys.sort(key = lambda x: self.key_dist[start][x][0])

		min_dist = None
		for key in needed_keys:
			path = self.key_dist[start][key]
			dist = path[0]
			path_keys = path[1]

			can_reach = all(path_key in found_keys for path_key in path_keys)
			if can_reach:
				new_keys = [found_key for found_key in found_keys]
				new_keys.append(key)
				new_keys.sort()

				total_dist = self.find_all_keys(key, new_keys, cur_dist+dist)
				if total_dist:
					if min_dist is None or total_dist < min_dist:
						min_dist = total_dist

		if len(needed_keys) == 0:
			return cur_dist
		else:
			return min_dist

if __name__ == '__main__':
	input_file = './input.txt'
	test_files = ['', './test1.txt', './test2.txt', './test3.txt', './test4.txt', './test5.txt']

	path_file = input_file

	if len(sys.argv) > 1:
		file_num = int(sys.argv[1])
		if file_num < 0 or file_num >= len(test_files):
			print('No Test File %d' % file_num)
		else:
			path_file = test_files[file_num]
	
	print('Running Test File %s' % path_file)

	path = DungeonPath(path_file)
	# print(path.count_tiles())
	path.find_key_distances()
	distance = path.find_all_keys()
	print(distance)