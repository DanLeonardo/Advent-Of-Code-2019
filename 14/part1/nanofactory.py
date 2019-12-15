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

	def find_ore_for_product(self, product, amount):
		inventory = {recipe: 0 for recipe in self.recipes}
		inventory['ORE'] = 0
		inventory[product] = amount

		running = True
		while running:
			print(inventory)

			# Try to reduce everything in inventory
			reduced = False
			for inv_product in inventory:
				if inventory[inv_product] > 0:
					reduced_products = self.reduce_product(inv_product, inventory[inv_product])

					if reduced_products is not None:
						reduced = True
						for key in reduced_products:
							if key == inv_product:
								inventory[key] = reduced_products[key]
							else:
								inventory[key] += reduced_products[key]

			# If we can't reduce we need to add to the inventory
			if not reduced:
				print('# Adding to Inventory')
				for inv_product in inventory:
					if inv_product != 'ORE' and inventory[inv_product] > 0:
						recipe = self.recipes[inv_product]
						inventory[inv_product] = recipe[0]

			# Check if only ore in inventory
			running = False
			for key in inventory:
				if key != 'ORE' and inventory[key] > 0:
					running = True
					break

		print('ORE: %d' % inventory['ORE'])

	def find_ore_for_fuel(self, amount):
		self.find_ore_for_product('FUEL', amount)

	def reduce_product(self, product, amount):
		if product == 'ORE':
			return None
		if product not in self.recipes:
			print('Error: %s not in recipes' % product)
			return None
		print('Reducing %d %s' % (amount, product))

		recipe = self.recipes[product]
		recipe_amount = recipe[0]
		recipe_ings = recipe[1]
		recipe_count = amount // recipe_amount

		if recipe_count > 0:
			reduce_amounts = {}
			for ing in recipe_ings:
				ing_amount = ing[0]
				ing_product = ing[1]
				reduce_amounts[ing_product] = ing_amount * recipe_count
				print('-Reduced to %d %s' % (ing_amount * recipe_count, ing_product))

			product_left = amount % recipe_amount
			reduce_amounts[product] = product_left
			print('-%d %s left' % (product_left, product))

			return reduce_amounts
		else:
			print('-Can\'t reduce %d %s' % (amount, product))
			return None


if __name__ == '__main__':
	test_files = ['./test1.txt', './test2.txt', './test3.txt', './test4.txt', './test5.txt']

	input_file = './input.txt'

	factory = Nanofactory(test_files[0])
	# factory.print_recipes()
	factory.find_ore_for_fuel(1)