# Divide by 3
# Round down
# Subtract 2
def calculate_fuel(mass):
    fuel = (mass // 3) - 2
    if fuel <= 0:
        return 0
    else:
        return fuel

def calculate_fuel_for_mass(mass):
    fuel = calculate_fuel(mass)
    if fuel <= 0:
        return 0
    else:
        new_fuel = calculate_fuel_for_mass(fuel)
        fuel += new_fuel
        return fuel

def calculate_fuel_for_trip(file_name):
    with open(file_name) as file:
        total_fuel = 0

        for module in file.readlines():
            fuel = calculate_fuel_for_mass(int(module))
            total_fuel += fuel

    return total_fuel

if __name__ == '__main__':
    file_name = './input.txt'
    needed_fuel = calculate_fuel_for_trip(file_name)
    print(needed_fuel)
