
class IntcodeComputer:
    def __init__(self):
        self.position = 0
        self.program = None

    def load_program(self, file_name):
        with open(file_name) as file:
            self.program = file.readline()
            self.program = self.program.rstrip('\n')
            self.program = self.program.split(',')
            self.program = [int(op) for op in self.program]

    def execute_program(self):
        if self.program is None:
            return

        self.position = 0
        finished = False
        while not finished:
            value = self.execute_opcode(self.position)

            if value == 99:
                finished = True
            elif value == -1:
                print('Error: Stopping Program')
                finished = True
            else:
                self.position += value

    def execute_opcode(self, position):
        # Read full opcode
        operation = str(self.program[position])

        # Break opcode into opcode and param mods
        op_code = int(operation[-2:]) if len(operation) > 1 else int(operation[0])
        param_modes = [int(mode) for mode in str(operation[:-2])]
        param_modes.reverse()
        while len(param_modes) < 3:
            param_modes.append(0)

        # print('%s: %s' % (position, operation))
        # print('-%s' % param_modes)
        
        # Execute opcode
        if op_code == 1:
            # Addition
            param_1 = self.get_parameter(position+1, param_modes[0])
            param_2 = self.get_parameter(position+2, param_modes[1])
            param_3 = self.get_parameter(position+3, 1)
            # print('%s + %s = %s -> %s' % (param_1, param_2, param_1+param_2, param_3))
            self.set_value(param_3, param_1 + param_2)
            return 4
        elif op_code == 2:
            # Multiplication
            param_1 = self.get_parameter(position+1, param_modes[0])
            param_2 = self.get_parameter(position+2, param_modes[1])
            param_3 = self.get_parameter(position+3, 1)
            self.set_value(param_3, param_1 * param_2)
            # print('%s * %s = %s -> %s' % (param_1, param_2, param_1*param_2, param_3))
            return 4
        elif op_code == 3:
            # Input
            param_1 = self.get_parameter(position+1, 1)
            value = input()
            self.set_value(param_1, value)
            # print('%s -> %s' % (value, param_1))
            return 2
        elif op_code == 4:
            # Output
            param_1 = self.get_parameter(position+1, param_modes[0])
            # print('%s -> out' % param_1)
            print('PRINT-%d' % param_1)
            return 2
        elif op_code == 5:
            # Jump If True
            pass
        elif op_code == 6:
            # Jump If False
            pass
        elif op_code == 7:
            # Less Than
            pass
        elif op_code == 8:
            # Equal
            pass
        elif op_code == 99:
            # Finish
            return 99
        else:
            # Error
            print('Error: Received code %s' % op_code)
            return -1

    def get_parameter(self, position, mode):
        if mode == 0:
            # Position
            address = self.get_value(position)
            value = self.get_value(address)
        elif mode == 1:
            # Immediate
            value = self.get_value(position)
        else:
            print('Error: Mode %d undefined' % mode)
            return None

        return int(value)

    def set_value(self, position, value):
        # print('Set Pos: %s to Val: %s' % (position, value))
        self.program[position] = value

    def get_value(self, position):
        # print('Get Pos: %s' % position)
        return self.program[position]

    def jump_to(self, position):
        self.position = position

if __name__ == '__main__':
    input_file = './input.txt'
    puter = IntcodeComputer()
    puter.load_program(input_file)
    puter.execute_program()
