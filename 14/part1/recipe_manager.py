class RecipeManager:
	def __init__(self, file_str):
		self.recipes = {}
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

	def make_recipe(self, product, amount):
		ing_amounts = self.count_ingredients(product, amount)
		print(ing_amounts)

	def count_ingredients(self, product, amount):
		if product == 'ORE':
			return {'ORE': amount}
		if product not in self.recipes:
			return None

		recipe = self.recipes[product]
		recipe_amount = recipe[0]
		recipe_ings = recipe[1]

		total_amounts = {product: amount}

		for ing in recipe_ings:
			ing_amount = ing[0]
			ing_product = ing[1]

			ing_counts = self.count_ingredients(ing_product, ing_amount * amount / recipe_amount)
			for count in ing_counts:
				if count in total_amounts:
					total_amounts[count] += ing_counts[count]
				else:
					total_amounts[count] = ing_counts[count]
		
		return total_amounts


class Nanofactory:
	def __init__(self, file_str):
		self.recipes = RecipeManager(file_str)

	def print_recipes(self):
		self.recipes.print_recipes()

	def make_fuel(self, amount):
		ingredients = self.recipes.make_recipe('FUEL', 1)
		# print(ingredients)

if __name__ == '__main__':
	input_file = './input.txt'
	test1_file = './test1.txt'
	test2_file = './test2.txt'

	factory = Nanofactory(test1_file)
	factory.print_recipes()
	factory.make_fuel(1)