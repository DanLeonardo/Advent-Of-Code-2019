import numpy as np

class Moon:
	def __init__(self, pos):
		self.x, self.y, self.z = pos
		self.vel_x, self.vel_y, self.vel_z = 0, 0, 0

	def get_pos(self):
		return self.x, self.y, self.z

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_z(self):
		return self.z

	def get_velocity(self):
		return self.vel_x, self.vel_y, self.vel_z

	def get_vel_x(self):
		return self.vel_x

	def get_vel_y(self):
		return self.vel_y

	def get_vel_z(self):
		return self.vel_z

	def add_velocity(self, velocity):
		add_x, add_y, add_z = velocity

		self.vel_x += add_x
		self.vel_y += add_y
		self.vel_z += add_z

	def move(self):
		self.x += self.vel_x
		self.y += self.vel_y
		self.z += self.vel_z

	def get_potential_energy(self):
		potential_energy = abs(self.x) + abs(self.y) + abs(self.z)
		return potential_energy

	def get_kinetic_energy(self):
		kinetic_energy = abs(self.vel_x) + abs(self.vel_y) + abs(self.vel_z)
		return kinetic_energy

	def get_total_energy(self):
		potential_energy = self.get_potential_energy()
		kinetic_energy = self.get_kinetic_energy()
		total_energy = potential_energy * kinetic_energy
		return total_energy

class MoonManager:
	def __init__(self, moons, num_steps):
		self.moons = [Moon(pos) for pos in moons]
		self.num_steps = num_steps

		self.original_state = [Moon(pos) for pos in moons]
		self.x_reset, self.y_reset, self.z_reset = -1, -1, -1

	def run(self):
		steps = 0
		while self.num_steps == -1 or steps < self.num_steps:
			if steps % 1000000 == 0:
				print('Step %d' % steps)

			moon_velocity = []
			# Update Velocity
			for i, moon in enumerate(self.moons):
				add_x, add_y, add_z = 0, 0, 0
				for other_moon in self.moons:
					if other_moon.get_x() < moon.get_x():
						add_x -= 1
					elif other_moon.get_x() > moon.get_x():
						add_x += 1

					if other_moon.get_y() < moon.get_y():
						add_y -= 1
					elif other_moon.get_y() > moon.get_y():
						add_y += 1

					if other_moon.get_z() < moon.get_z():
						add_z -= 1
					elif other_moon.get_z() > moon.get_z():
						add_z += 1
				moon_velocity.append((add_x, add_y, add_z))

			# Update Position
			for i, velocity in enumerate(moon_velocity):
				self.moons[i].add_velocity(velocity)
				self.moons[i].move()

			# Check New Position
			## Check X
			if self.x_reset is -1:
				current_px = [moon.get_x() for moon in self.moons]
				original_px = [moon.get_x() for moon in self.original_state]

				if current_px == original_px:
					x_kinetic = [abs(moon.get_vel_x()) for moon in self.moons]
					if sum(x_kinetic) is 0:
						print('X resets on step %d' % steps)
						self.x_reset = steps+1

			## Check Y
			if self.y_reset is -1:
				current_py = [moon.get_y() for moon in self.moons]
				original_py = [moon.get_y() for moon in self.original_state]

				if current_py == original_py:
					y_kinetic = [abs(moon.get_vel_y()) for moon in self.moons]
					if sum(y_kinetic) is 0:
						print('Y resets on step %d' % steps)
						self.y_reset = steps+1

			## Check Z
			if self.z_reset is -1:
				current_pz = [moon.get_z() for moon in self.moons]
				original_pz = [moon.get_z() for moon in self.original_state]

				if current_pz == original_pz:
					z_kinetic = [abs(moon.get_vel_z()) for moon in self.moons]
					if sum(z_kinetic) is 0:
						print('Z resets on step %d' % steps)
						self.z_reset = steps+1

			if self.x_reset is not -1 and self.y_reset is not -1 and self.z_reset is not -1:
				break

			steps += 1

		lcm = np.lcm.reduce([self.x_reset, self.y_reset, self.z_reset])
		print(lcm)
		print('Total System Energy is %d' % self.get_system_energy())

	def get_system_energy(self):
		total_energy = 0
		for moon in self.moons:
			total_energy += moon.get_total_energy()
		return total_energy

	def get_state(self):
		return [moon.get_pos() for moon in self.moons]

if __name__ == '__main__':
	input_txt = [
		(-13, 14, -7),
		(-18, 9, 0),
		(0, -3, -3),
		(-15, 3, -13)
	]

	test1_txt = [
		(-8,-10,0),
		(5,5,10),
		(2,-7,3),
		(9,-8,-3)
	]

	# moons = [Moon(moon) for moon in test1_txt]

	moon_manager = MoonManager(input_txt, -1)
	moon_manager.run()