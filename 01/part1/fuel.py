# Divide by 3
# Round down
# Subtract 2
def calculate_fuel(mass):
    return (mass // 3) - 2

def calculate_all_modules(file_str):
    total_fuel = 0
    total_mass = 0
    try:
        with open(file_str) as file:
            for line in file.readlines():
                module_mass = int(line)
                total_mass += module_mass
                print('%d: %d' % (module_mass, calculate_fuel(module_mass)))
                total_fuel += calculate_fuel(module_mass)
    except Exception as e:
        print(type(e).__name__)
        total_fuel = -1j

    print('Mass %d' % total_mass)
    return total_fuel


if __name__ == '__main__':
    file_name = './input.txt'
    print(calculate_all_modules(file_name))
