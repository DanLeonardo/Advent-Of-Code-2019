def load_program(file_name):
    with open(file_name) as file:
        program = file.readline()
        program = program.rstrip('\n')
        program = program.split(',')
        program = [int(op) for op in program]
        return program

def execute_opcode(position, program):
    operation = str(program[position])
    print('position-%d' % position)

    op_code = int(operation[-2:]) if len(operation) > 1 else int(operation[0])
    param_modes = [int(mode) for mode in str(operation[:-2])]

    param_modes.reverse()
    while len(param_modes) < 2:
        param_modes.append(0)

    # print(op_code)
    if op_code == 1:
        # Add
        if param_modes[0] == 0:
            param_1 = int(program[program[position+1]])
        elif param_modes[0] == 1:
            param_1 = int(program[position+1])

        if param_modes[1] == 0:
            param_2 = int(program[program[position+2]])
        elif param_modes[1] == 1:
            param_2 = int(program[position+2])

        param_3 = program[position+3]

        program[param_3] = param_1 + param_2
        return 4
    elif op_code == 2:
        # Multiply
        if param_modes[0] == 0:
            param_1 = int(program[program[position+1]])
        elif param_modes[0] == 1:
            param_1 = int(program[position+1])

        if param_modes[1] == 0:
            param_2 = int(program[program[position+2]])
        elif param_modes[1] == 1:
            param_2 = int(program[position+2])

        param_3 = program[position+3]

        program[param_3] = param_1 * param_2
        return 4
    elif op_code == 3:
        # Input
        address = program[position+1]
        value = input()
        program[address] = value
        return 2
    elif op_code == 4:
        # Output
        address = program[position+1]
        # print(program[address])
        print('PRINT: %d' % program[address])
        return 2
    elif op_code == 99:
        # Finish
        return 99
    else:
        # Error
        print('Received Code %s' % operation)
        return -1

    # Should never reach
    return None

def run_program(file_name):
    program = load_program(file_name)
    # print('Running: %s' % program)

    pos = 0
    running = True
    while running:
        result = execute_opcode(pos, program)
        if result == 99:
            running = False
        elif result == -1:
            print('Error: Stopping program')
            return None
        pos += result

if __name__ == '__main__':
    input_file = './input.txt'
    run_program(input_file)
