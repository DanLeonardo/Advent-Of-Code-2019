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
		self.moons = moons
		self.num_steps = num_steps

	def run(self):
		steps = 0
		while steps < self.num_steps:
			moon_velocity = []
			# Update Velocity
			for moon in self.moons:
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
			steps += 1

		print('Total System Energy is %d' % self.get_system_energy())

	def get_system_energy(self):
		total_energy = 0
		for moon in self.moons:
			total_energy += moon.get_total_energy()
		return total_energy

if __name__ == '__main__':
	input_txt = [
		(-13, 14, -7),
		(-18, 9, 0),
		(0, -3, -3),
		(-15, 3, -13)
	]

	test1_txt = [
		(-1, 0, 2),
		(2, -10, -7),
		(4, -8, 8),
		(3, 5, -1)
	]

	moons = [Moon(moon) for moon in input_txt]

	moon_manager = MoonManager(moons, 1000)
	moon_manager.run()