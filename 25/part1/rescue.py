from intcode_computer import IntcodeComputer
import re
import copy

class Room:
	def __init__(self):
		self.text = None
		self.name = None
		# self.items = {}
		self.edges = {}		# direction(str): room_name(str) e.g. 'north': 'Observatory'	# room_name is None if unknown

	def print(self):
		print(self.name)
		for edge in self.edges:
			print('%s: %s' % (edge, self.edges[edge]))

	def has_unknown_edge(self):
		for dir, name in self.edges.items():
			if name is None:
				return True
		return False

		#Pressure-Sensitive Floor

class RescueBot:
	def __init__(self, file_str):
		self.computer = IntcodeComputer(file_str, echo=False)
		self.running = False

		self.rooms = {}		# name(str): room(Room)
		self.items = {}		# name(str): room(Room)
		self.directions = []		# e.g. ['north', 'west', 'west', 'south']

		self.cur_room = None
		self.last_room = None
		self.last_dir = None

	def run(self):
		self.running = True
		self.computer.run()
		while self.running:
			output = self.computer.get_output()
			output = ''.join([chr(char) for char in output])
			# print(output)

			# Find/Create Room
			self.last_room = self.cur_room
			room_name = self.get_name_from_output(output)
			if re.search('You can\'t go that way.', output):
				print(output)
			elif room_name in self.rooms:
				self.cur_room = self.rooms[room_name]
			else:
				self.cur_room = self.get_room_from_output(output)
				self.rooms[room_name] = self.cur_room

				print('New Room:')
				self.cur_room.print()
				# print(self.cur_room.text)

			# Link the rooms if they are not already
			if self.last_room and self.last_room is not self.cur_room:
				print('Linking: %s and %s' % (self.cur_room.name, self.last_room.name))
				if self.last_room.edges[self.last_dir] is None:
					self.last_room.edges[self.last_dir] = self.cur_room.name

				if self.last_dir == 'north':
					inv_last_dir = 'south'
				elif self.last_dir == 'south':
					inv_last_dir = 'north'
				elif self.last_dir == 'east':
					inv_last_dir = 'west'
				elif self.last_dir == 'west':
					inv_last_dir = 'east'
				if inv_last_dir in self.cur_room.edges and self.cur_room.edges[inv_last_dir] is None:
					self.cur_room.edges[inv_last_dir] = self.last_room.name

				# self.cur_room.print()
				# self.last_room.print()

			print(output)
			command = self.get_command()
			print('####################')
			print('Current Room: %s' % self.cur_room.name)
			print('Command: %s' % command)
			print('####################')

			if command in ('north', 'south', 'east', 'west'):
				self.last_dir = command

			if command is None:
				self.running = False
				break

			ascii_command = [ord(char) for char in command]
			ascii_command.append(ord('\n'))
			self.computer.read_input(ascii_command)

	def get_command(self):
		if self.directions:
			return self.directions.pop(0)
		elif self.cur_room.has_unknown_edge():
			for dir, name in self.cur_room.edges.items():
				if name is None:
					return dir
			print('Unknown Edge not found')
		else:
			dest = self.find_nearest_unexplored()
			self.directions = self.get_directions_to_room(self.cur_room.name, dest)

			if self.directions is not None:
				return self.directions.pop(0)
			else:
				print('Directions not found')
				self.running = False
				return None

	def find_nearest_unexplored(self):
		for name, room in self.rooms.items():
			print(name)
			for dir, edge in room.edges.items():
				if edge is None:
					return name
		return None

	def get_directions_to_room(self, start_room, stop_room):
		if start_room not in self.rooms:
			print('Error: "%s" not in rooms to path.' % start_room)
			return None
		if stop_room not in self.rooms:
			print('Error: "%s" not in rooms to path.' % stop_room)
			return None

		print('Finding directions from %s to %s' % (start_room, stop_room))

		parents = {start_room: None}
		distances = {start_room: 0}
		node_list = [start_room]

		while len(node_list) > 0:
			node_name = node_list.pop(0)
			if node_name == stop_room:
				break

			node_room = self.rooms[node_name]
			node_edges = node_room.edges
			node_dist = distances[node_name]

			for dir, edge in node_edges.items():
				if edge is not None and edge not in parents:
					parents[edge] = (node_name, dir)
					distances[edge] = node_dist + 1
					node_list.append(edge)

		directions = []
		path_par = parents[stop_room]
		while path_par is not None:
			directions.insert(0, path_par[1])
			path_par = parents[path_par[0]]

		return directions

	def get_name_from_output(self, output):
		# Room Name
		name_match = re.search('== ([a-zA-Z ]+) ==', output)
		if name_match:
			name = name_match.group(1)
			# print('Room Name: %s' % name)
			return name
		else:
			# print('Error: Name not found')
			# print(output)
			return None

	def get_room_from_output(self, output):
		new_room = Room()
		new_room.text = output

		# Room Name
		name_match = re.search('== ([a-zA-Z ]+) ==', output)
		if name_match:
			name = name_match.group(1)
			new_room.name = name
			# print('Room Name: %s' % name)

		# Adding edge rooms
		dir_match = re.search('Doors here lead:\n(- north)?\n?(- east)?\n?(- south)?\n?(- west)?', output)
		if dir_match:
			if dir_match.group(1):
				# print('north found')
				new_room.edges['north'] = None

			if dir_match.group(3):
				# print('south found')
				new_room.edges['south'] = None

			if dir_match.group(2):
				# print('east found')
				new_room.edges['east'] = None

			if dir_match.group(4):
				# print('west found')
				new_room.edges['west'] = None

		return new_room

		# Handling Items
		# item_str_match = re.search('Items here:\n', output)
		# if item_str_match:
		# 	before, keyword, items = output.partition('Items here:\n')
		# 	items_match = re.findall('- [a-z ]+', items)
		# 	# print(items_match)
		# 	new_room.items = items_match

		# 	for item in items_match:
		# 		self.items[item[2:]] = pos

	def find_room_by_name(self, name):
		for room in self.rooms:
			if room.name == name:
				return room

		return None

	def find_closest_unexplored_room(self):
		min_dist = -1
		closest = None

		for pos in self.unexplored:
			pos_x, pos_y = pos
			dist = abs(self.x - pos_x) + abs(self.y - pos_y)

			if not closest or dist < min_dist:
				closest = pos
				min_dist = dist

		return closest

if __name__ == '__main__':
	rescue = RescueBot('./input.txt')
	rescue.run()