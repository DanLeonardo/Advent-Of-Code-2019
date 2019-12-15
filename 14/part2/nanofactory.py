class Nanofactory:
	def __init__(self, file_str):
		self.read_recipes(file_str)

	def read_recipes(self, file_str):
		self.recipes = {}
		with open(file_str, 'r') as file:
			for line in file.readlines():
				line = line.strip('\n')
				line = line.replace(',', '')
				line_split = line.split(' ')

				ingredient_list = []
				final_amount = -1
				final_product = None
				i = 0
				while i < len(line_split):
					if line_split[i] == '=>':
						final_amount = int(line_split[i+1])
						final_product = line_split[i+2]
						break
					else:
						ing_amount = int(line_split[i])
						ing_product = line_split[i+1]
						ingredient_list.append((ing_amount, ing_product))
					i += 2

				self.recipes[final_product] = [final_amount, ingredient_list]

	def print_recipes(self):
		for product in self.recipes:
			amount = self.recipes[product][0]
			ingredients = ['%d %s' % (ingredient[0], ingredient[1]) for ingredient in self.recipes[product][1]]
			ingredients_str = ', '.join(ingredients)

			print('%s => %d %s' % (ingredients_str, amount, product))

	def produce_product(self, product, amount, spares=None, level=0):
		indents = ''.join(['\t' for _ in range(level)])

		if product == 'ORE':
			# print(indents + 'Mining: %d ORE' % amount)
			spares['ORE'] += amount
			return
		if product not in self.recipes:
			# print(indents + 'Error: %s not in recipes' % product)
			return

		if spares is None:
			spares = {key: 0 for key in self.recipes}
			spares['ORE'] = 0

		# print(indents + 'Need: %d %s' % (amount, product))
		# print(indents + 'Have: %d %s' % (spares[product], product))

		# Check if we need to produce more product
		to_produce = amount - spares[product]
		if spares[product] > 0:
				if spares[product] <= amount:
					# print(indents + 'Using: %d spare %s' % (spares[product], product))
					spares[product] = 0
				else:
					# print(indents + 'Using: %d spare %s' % (amount, product))
					spares[product] -= amount

		# Produce more if needed
		if to_produce > 0:
			# print(indents + 'Still Need: %d %s' % (to_produce, product))

			# Retrieve recipe info
			recipe = self.recipes[product]
			num_made = recipe[0]
			ingredients = recipe[1]
			num_times = to_produce // num_made
			if to_produce % num_made > 0:
				num_times += 1

			# Calculate how much spare product will be made
			spare_product = (num_made * num_times) - to_produce
			if spare_product > 0:
				spares[product] += spare_product
			# print(indents + '%d reactions produce %d %s leaving %d spare' % (num_times, num_made * num_times, product, spare_product))

			# Produce all needed ingredients
			for ing in ingredients:
				ing_amount = ing[0]
				ing_name = ing[1]

				self.produce_product(ing_name, ing_amount * num_times, spares, level+1)

		if level == 0:
			# print('ORE: %d' % spares['ORE'])
			return spares['ORE']

def find_max_fuel(lower_bound, upper_bound, max_ore, factory):
	if lower_bound >= upper_bound:
		return lower_bound

	guess = (lower_bound + upper_bound) // 2
	ore = factory.produce_product('FUEL', guess)
	# print('%d Fuel takes %d Ore' % (guess, ore))

	if ore > max_ore:
		# Lower the bounds
		return find_max_fuel(lower_bound, guess-1, max_ore, factory)
	elif ore < max_ore:
		# Increase the bounds
		return find_max_fuel(guess+1, upper_bound, max_ore, factory)
	elif ore == max_ore:
		return guess

if __name__ == '__main__':
	test_files = ['./test3.txt', './test4.txt', './test5.txt']
	input_file = './input.txt'

	factory = Nanofactory(input_file)
	# factory.print_recipes()

	trillion = 1000000000000
	ore_per_fuel = factory.produce_product('FUEL', 1)

	# upper_bound = 8000000
	upper_bound = trillion // ore_per_fuel

	max_fuel = find_max_fuel(0, trillion, trillion, factory)
	print('%d FUEL from %d ORE' % (max_fuel, trillion))