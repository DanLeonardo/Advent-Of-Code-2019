import string

class DungeonPath:
	def __init__(self, input_str=None):
		self.input_str = input_str
		self.map = None
		self.door_map = None
		self.doors = None
		self.keys = None
		self.entrance = None

	def read_map(self):
		if self.input_str is None:
			return

		# self.map = [
		#	[0, [1, [2,
		# 	 3,  4,  5,
		# 	 6], 7], 8],
		# ]

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

	def print_map(self):
		if self.map is None:
			return

		print('%dx%d' % (self.width, self.height))

		# for row in self.map:
		# 	for tile in row:
		# 		print(tile, end='')
		# 	print('\n', end='')
		for y in range(self.height):
			for x in range(self.width):
				print(self.map[x][y], end='')
			print('\n', end='')

	def find_entrance(self):
		for y in range(self.height):
			for x in range(self.width):
				tile = self.get_tile(x, y)
				if tile == '@':
					self.entrance = (x, y)
					return self.entrance

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

	def get_tile(self, x, y):
		if x < 0 or x >= self.width:
			return None
		if y < 0 or y >= self.height:
			return None

		return self.map[x][y]

	def can_reach_tile(self, x, y, keys):
		needed_keys = self.door_map[x][y]
		for key in needed_keys:
			if key.lower() not in keys:
				return False
		return True

	def found_all_keys(self, keys):
		for key in self.keys:
			if key not in keys:
				return False
		return True

	def find_closest_key(self, cur_x, cur_y, found_keys):
		for key in self.keys:
			key_pos = self.keys[key]
			key_x, key_y = key_pos
			key_doors = self.door_map[key_x][key_y]

			if all(keys.lower() in found_keys for keys in key_doors):
				print('yes %s' % key)
			else:
				print('no %s' % key)

	def mark_tiles(self):
		'''
		Run BFS on the map starting at the entrance. Include a flag on each tile showing the doors that block the path
		to get to that tile. Tiles with a door on them are blocked by that door.
		door_map: 2D list where door_map[x] is a list and door_map[x][y] is a list of doors
		'''
		# Init door_map 
		self.door_map = []
		for x in range(self.width):
			self.door_map.append([])
			for y in range(self.height):
				self.door_map[-1].append([])

		start_node = self.entrance
		parents = []
		for x in range(self.width):
			parents.append([])
			for y in range(self.height):
				parents[-1].append(None)

		nodes = [start_node] 
		while nodes != []:
			node = nodes.pop(0)
			node_x, node_y = node
			par_node = parents[node_x][node_y]
			# print('Marking Node (%d, %d)' % (node_x, node_y))
			# If a door is on this tile add it to the door_map
			on_door = self.get_door(node_x, node_y)
			if on_door:
				self.door_map[node_x][node_y].append(on_door)

			# Up
			up_node = self.get_tile(node_x, node_y-1)
			if up_node is not None and up_node != '#':
				up_node_x, up_node_y = node_x, node_y-1
				if parents[up_node_x][up_node_y] is None:
					parents[up_node_x][up_node_y] = node
					self.door_map[up_node_x][up_node_y].extend(self.door_map[node_x][node_y])
					nodes.append((up_node_x, up_node_y))

			# Down
			down_node = self.get_tile(node_x, node_y+1)
			if down_node is not None and down_node != '#':
				down_node_x, down_node_y = node_x, node_y+1
				if parents[down_node_x][down_node_y] is None:
					parents[down_node_x][down_node_y] = node
					self.door_map[down_node_x][down_node_y].extend(self.door_map[node_x][node_y])
					nodes.append((down_node_x, down_node_y))

			# Left
			left_node = self.get_tile(node_x-1, node_y)
			if left_node is not None and left_node != '#':
				left_node_x, left_node_y = node_x-1, node_y
				if parents[left_node_x][left_node_y] is None:
					parents[left_node_x][left_node_y] = node
					self.door_map[left_node_x][left_node_y].extend(self.door_map[node_x][node_y])
					nodes.append((left_node_x, left_node_y))

			# Right
			right_node = self.get_tile(node_x+1, node_y)
			if right_node is not None and right_node != '#':
				right_node_x, right_node_y = node_x+1, node_y
				if parents[right_node_x][right_node_y] is None:
					parents[right_node_x][right_node_y] = node
					self.door_map[right_node_x][right_node_y].extend(self.door_map[node_x][node_y])
					nodes.append((right_node_x, right_node_y))

		# for y in range(self.height):
		# 	for x in range(self.width):
		# 		if self.get_tile(x, y) in [None, '#']:
		# 			continue
		# 		tile = self.door_map[x][y]
		# 		par = parents[x][y]
		# 		if par:
		# 			print('(%d, %d) (%d, %d): %s' % (x, y,par[0], par[1], tile))
		# 		else:
		# 			print('(%d, %d): %s' % (x, y, tile))		

	def find_path(self):
		if self.input_str is None:
			print('Error: No input provided')
			return None

		if self.map is None:
			self.read_map()

		# Show info of map
		self.print_map()
		print('Entrance at (%d, %d)' % (self.entrance[0], self.entrance[1]))
		sorted_doors = sorted([door for door in self.doors])
		for door in sorted_doors:
			print('Door %s at (%d, %d)' % (door, self.doors[door][0], self.doors[door][1]))
		sorted_keys = sorted([key for key in self.keys])
		for key in sorted_keys:
			print('Key %s at (%d, %d)' % (key, self.keys[key][0], self.keys[key][1]))

		# Mark tiles with the doors blocking them
		self.mark_tiles()

		found_keys = []
		cur_x, cur_y = self.entrance
		while not self.found_all_keys(found_keys):
			break


if __name__ == '__main__':
	input_file = './input.txt'
	test1_file = './test1.txt'
	test2_file = './test2.txt'

	path = DungeonPath(test2_file)
	path.find_path()