from intcode_computer import IntcodeComputer
import random

class DroidController:
	def __init__(self, file_str, echo=True):
		self.computer = IntcodeComputer(file_str, echo=False)
		self.x, self.y = 0, 0
		self.min_x, self.max_x = 0, 0
		self.min_y, self.max_y = 0, 0

		self.map = {(self.x, self.y): '.'}
		self.path = []
		self.target = None

	def print_map(self):
		for y in range(self.min_y, self.max_y+1):
			for x in range(self.min_x, self.max_x+1):
				if (x, y) in self.map:
					if (self.x, self.y) == (x, y):
						print('D', end='')
					else:
						tile = self.map[(x,y)]
						print(tile, end='')
				else:
					print(' ', end='')

			# New Line
			print('\n', end='')

	def find_all_unexplored(self):
		# Find all unexplored tiles
		all_unexplored = []
		for coord in self.map:
			tile = self.map[coord]
			if tile == '.' or tile == 'O':
				unexplored = self.check_unexplored(coord)
				all_unexplored.extend(unexplored)

		return all_unexplored

	def find_nearest_unexplored(self):
		'''
		Returns the (x, y) coordinate of the nearest manhatten distance unexplored tile from self.pos.
		'''
		all_unexplored = self.find_all_unexplored()

		# Find distance of each tile
		distances = []
		for tile in all_unexplored:
			dist_x = abs(self.x - tile[0])
			dist_y = abs(self.y - tile[1])
			distances.append(dist_x + dist_y)

		# Find shortest distance
		min_i = -1
		min_dist = -1
		for i, dist in enumerate(distances):
			if min_dist is -1 or dist < min_dist:
				min_i = i
				min_dist = dist

		return all_unexplored[min_i]

	def find_oxygen_system(self):
		for coord in self.map:
			if self.map[coord] == 'O':
				return coord

		return None

	def find_max_dist_from_oxygen(self):
		start = self.find_oxygen_system()
		if start is None:
			print('Oxygen System not found')
			return None

		# Search for finish from start
		tile_list = [start]
		parents = {start: None}
		distances = {start: 0}

		while len(tile_list) > 0:
			tile = tile_list.pop(0)
			tile_x, tile_y = tile
			tile_dist = distances[tile]

			if tile not in self.map:
				continue

			# Add neighbors to list if not explored or smaller distance
			## Up
			tile_up = tile_x, tile_y-1
			if tile_up in parents:
				# Already searched tile. Check for shorter distance
				tile_up_dist = distances[tile_up]
				if tile_up_dist > tile_dist + 1:
					if tile_up in self.map:
						tile_list.append(tile_up)
					parents[tile_up] = tile
					distances[tile_up] = tile_dist + 1
			elif tile_up in self.map:
				# Nonsearched explored tile. Add to list if not a wall
				if self.map[tile_up] != '#':
					tile_list.append(tile_up)
					parents[tile_up] = tile
					distances[tile_up] = tile_dist + 1
			else:
				# Nonsearched unexplored tile. Add to path but not the search list
				parents[tile_up] = tile
				distances[tile_up] = tile_dist + 1

			## Down
			tile_down = tile_x, tile_y+1
			if tile_down in parents:
				# Already searched tile. Check for shorter distance
				tile_down_dist = distances[tile_down]
				if tile_down_dist > tile_dist + 1:
					if tile_down in self.map:
						tile_list.append(tile_down)
					parents[tile_down] = tile
					distances[tile_down] = tile_dist + 1
			elif tile_down in self.map:
				# Nonsearched explored tile. Add to list if not a wall
				if self.map[tile_down] != '#':
					tile_list.append(tile_down)
					parents[tile_down] = tile
					distances[tile_down] = tile_dist + 1
			else:
				# Nonsearched unexplored tile. Add to path but not the search list
				parents[tile_down] = tile
				distances[tile_down] = tile_dist + 1

			## Left
			tile_left = tile_x-1, tile_y
			if tile_left in parents:
				# Already searched tile. Check for shorter distance
				tile_left_dist = distances[tile_left]
				if tile_left_dist > tile_dist + 1:
					if tile_left in self.map:
						tile_list.append(tile_left)
					parents[tile_left] = tile
					distances[tile_left] = tile_dist + 1
			elif tile_left in self.map:
				# Nonsearched explored tile. Add to list if not a wall
				if self.map[tile_left] != '#':
					tile_list.append(tile_left)
					parents[tile_left] = tile
					distances[tile_left] = tile_dist + 1
			else:
				# Nonsearched unexplored tile. Add to path but not the search list
				parents[tile_left] = tile
				distances[tile_left] = tile_dist + 1

			## Right
			tile_right = tile_x+1, tile_y
			if tile_right in parents:
				# Already searched tile. Check for shorter distance
				tile_right_dist = distances[tile_right]
				if tile_right_dist > tile_dist + 1:
					if tile_right in self.map:
						tile_list.append(tile_right)
					parents[tile_right] = tile
					distances[tile_right] = tile_dist + 1
			elif tile_right in self.map:
				# Nonsearched explored tile. Add to list if not a wall
				if self.map[tile_right] != '#':
					tile_list.append(tile_right)
					parents[tile_right] = tile
					distances[tile_right] = tile_dist + 1
			else:
				# Nonsearched unexplored tile. Add to path but not the search list
				parents[tile_right] = tile
				distances[tile_right] = tile_dist + 1

		max_dist = 0
		for tile in distances:
			if distances[tile] > max_dist:
				max_dist = distances[tile]
		return max_dist


	def check_unexplored(self, coord):
		'''
		Returns a list of (x, y) coordinates containing unexplored tiles in 4 cardinal directions of given coordinate
		'''
		unexplored = []
		x, y = coord

		# Top
		tile_up = x, y-1
		if tile_up not in self.map:
			unexplored.append(tile_up)
		# Bottom
		tile_down = x, y+1
		if tile_down not in self.map:
			unexplored.append(tile_down)
		# Left
		tile_left = x-1, y
		if tile_left not in self.map:
			unexplored.append(tile_left)
		# Right
		tile_right = x+1, y
		if tile_right not in self.map:
			unexplored.append(tile_right)

		return unexplored

	def find_path_to_target(self, start, finish):
		# print('Finding path from %s to %s' % (start, finish))
		# Search for finish from start
		tile_list = [start]
		parents = {start: None}
		distances = {start: 0}

		while len(tile_list) > 0:
			tile = tile_list.pop(0)
			tile_x, tile_y = tile
			tile_dist = distances[tile]

			if tile not in self.map:
				continue

			# Add neighbors to list if not explored or smaller distance
			## Up
			tile_up = tile_x, tile_y-1
			if tile_up in parents:
				# Already searched tile. Check for shorter distance
				tile_up_dist = distances[tile_up]
				if tile_up_dist > tile_dist + 1:
					if tile_up in self.map:
						tile_list.append(tile_up)
					parents[tile_up] = tile
					distances[tile_up] = tile_dist + 1
			elif tile_up in self.map:
				# Nonsearched explored tile. Add to list if not a wall
				if self.map[tile_up] != '#':
					tile_list.append(tile_up)
					parents[tile_up] = tile
					distances[tile_up] = tile_dist + 1
			else:
				# Nonsearched unexplored tile. Add to path but not the search list
				parents[tile_up] = tile
				distances[tile_up] = tile_dist + 1

			## Down
			tile_down = tile_x, tile_y+1
			if tile_down in parents:
				# Already searched tile. Check for shorter distance
				tile_down_dist = distances[tile_down]
				if tile_down_dist > tile_dist + 1:
					if tile_down in self.map:
						tile_list.append(tile_down)
					parents[tile_down] = tile
					distances[tile_down] = tile_dist + 1
			elif tile_down in self.map:
				# Nonsearched explored tile. Add to list if not a wall
				if self.map[tile_down] != '#':
					tile_list.append(tile_down)
					parents[tile_down] = tile
					distances[tile_down] = tile_dist + 1
			else:
				# Nonsearched unexplored tile. Add to path but not the search list
				parents[tile_down] = tile
				distances[tile_down] = tile_dist + 1

			## Left
			tile_left = tile_x-1, tile_y
			if tile_left in parents:
				# Already searched tile. Check for shorter distance
				tile_left_dist = distances[tile_left]
				if tile_left_dist > tile_dist + 1:
					if tile_left in self.map:
						tile_list.append(tile_left)
					parents[tile_left] = tile
					distances[tile_left] = tile_dist + 1
			elif tile_left in self.map:
				# Nonsearched explored tile. Add to list if not a wall
				if self.map[tile_left] != '#':
					tile_list.append(tile_left)
					parents[tile_left] = tile
					distances[tile_left] = tile_dist + 1
			else:
				# Nonsearched unexplored tile. Add to path but not the search list
				parents[tile_left] = tile
				distances[tile_left] = tile_dist + 1

			## Right
			tile_right = tile_x+1, tile_y
			if tile_right in parents:
				# Already searched tile. Check for shorter distance
				tile_right_dist = distances[tile_right]
				if tile_right_dist > tile_dist + 1:
					if tile_right in self.map:
						tile_list.append(tile_right)
					parents[tile_right] = tile
					distances[tile_right] = tile_dist + 1
			elif tile_right in self.map:
				# Nonsearched explored tile. Add to list if not a wall
				if self.map[tile_right] != '#':
					tile_list.append(tile_right)
					parents[tile_right] = tile
					distances[tile_right] = tile_dist + 1
			else:
				# Nonsearched unexplored tile. Add to path but not the search list
				parents[tile_right] = tile
				distances[tile_right] = tile_dist + 1

		# Find path back to start
		new_path = []
		if finish in parents:
			path_node = finish
			while path_node != start:
				new_path.insert(0, path_node)
				path_node = parents[path_node]
			# print('Found Path: %s' % str(new_path))

		# print(new_path)
		return new_path

	def move_on_path(self):
		if self.path == []:
			print('Error: No Path to follow')
			return None
		path_x, path_y = self.path.pop(0)

		move_x = path_x - self.x
		move_y = path_y - self.y

		if move_y is -1 and move_x is 0:
			return 1
		elif move_y is 1 and move_x is 0:
			return 2
		elif move_y is 0 and move_x is -1:
			return 3
		elif move_y is 0 and move_x is 1:
			return 4
		else:
			print('%d, %d is invalid' % (move_x, move_y))
			return None

	def make_move(self):
		# move = -1
		# while move < 1 or move > 4:
		# 	move = int(input('Selection Direction: '))
		# return move

		if self.path == []:
			self.target = self.find_nearest_unexplored()
			self.path = self.find_path_to_target((self.x, self.y), self.target)
		
		move = self.move_on_path()

		return move

	def run(self):
		running = True
		while self.find_all_unexplored() != []:
			# self.print_map()

			# Give input and receive response
			move = self.make_move()
			# print('Move: %d' % move)
			self.computer.set_input([move])
			self.computer.execute_program()
			result = self.computer.get_last_value()

			# Find new position
			if move == 1:
				move_x = self.x
				move_y = self.y - 1
			elif move == 2:
				move_x = self.x
				move_y = self.y + 1
			elif move == 3:
				move_x = self.x - 1
				move_y = self.y
			elif move == 4:
				move_x = self.x + 1
				move_y = self.y

			# Update map bounds
			if move_x < self.min_x:
				self.min_x = move_x
			if move_x > self.max_x:
				self.max_x = move_x
			if move_y < self.min_y:
				self.min_y = move_y
			if move_y > self.max_y:
				self.max_y = move_y

			if result == 0:
				# Hit a wall
				if (move_x, move_y) not in self.map:
					self.map[(move_x, move_y)] = '#'
			elif result == 1:
				# Moved in direction
				if (move_x, move_y) not in self.map:
					self.map[(move_x, move_y)] = '.'
				self.x, self.y = move_x, move_y
			elif result == 2:
				# Found Oxygen System
				if (move_x, move_y) not in self.map:
					self.map[(move_x, move_y)] = 'O'
				self.x, self.y = move_x, move_y
				running = False
			else:
				print('Error: Invalid result %d' % result)
				running = False

		oxygen_distance = self.find_max_dist_from_oxygen()
		print(oxygen_distance)

if __name__ == '__main__':
	controller = DroidController('./input.txt', echo=True)
	controller.run()