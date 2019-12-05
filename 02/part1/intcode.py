def load_opcode(file_name):
    with open(file_name) as file:
        opcode = file.readline()
        opcode = opcode.rstrip('\n')
        opcode = opcode.split(',')
        opcode = [int(op) for op in opcode]
        return opcode

def execute_opcode(position, opcode):
    op = opcode[position]
    # print('Executing opcode %d' % op)

    if op == 1:
        arg1 = opcode[position+1]
        arg2 = opcode[position+2]
        arg3 = opcode[position+3]
        opcode[arg3] = opcode[arg1] + opcode[arg2]
        # print('%d + %d = %d. Stored at %d' % (arg1, arg2, arg1 + arg2, arg3))
        return 1
    elif op == 2:
        arg1 = opcode[position+1]
        arg2 = opcode[position+2]
        arg3 = opcode[position+3]
        opcode[arg3] = opcode[arg1] * opcode[arg2]
        # print('%d * %d = %d. Stored at %d' % (arg1, arg2, arg1 * arg2, arg3))
        return 2
    elif op == 99:
        return 99
    else:
        print('Error: Unknown opcode')
        return -1

def run_program(file_name):
    opcode = load_opcode(file_name)
    # print('Running: %s' % opcode)

    opcode[1] = 12
    opcode[2] = 2

    pos = 0
    running = True
    while running:
        result = execute_opcode(pos, opcode)
        if result == 99:
            running = False
        elif result == -1:
            print('Error: Stopping program')
        pos += 4

    print(opcode[0])
    return opcode

if __name__ == '__main__':
    input_file = './input.txt'
    test1_file = './test1.txt'
    test2_file = './test2.txt'

    result = run_program(input_file)
    print(result)
    print(result[0])
