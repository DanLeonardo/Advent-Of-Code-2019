from itertools import permutations

class IntcodeComputer:
    def __init__(self, file_name=None, echo=True):
        self.position = 0
        self.rel_base = 0
        self.last_value = None
        self.output_values = []
        self.input_list = []
        self.echo = echo
        self.finished = False
        self.paused = False

        if file_name is None:
            self.load_program('./input.txt')
        else:
            self.load_program(file_name)

    def load_program(self, file_name):
        with open(file_name) as file:
            self.program = file.read()
            self.program = self.program.rstrip('\n')
            self.program = self.program.split(',')
            self.program = [int(op) for op in self.program]

    def execute_program(self):
        if self.program is None:
            return

        self.paused = False

        while not self.finished and not self.paused:
            value = self.execute_opcode(self.position)

            if value == 99:
                self.finished = True
            elif value == -1:
                print('Error: Stopping Program')
                self.finished = True
            else:
                self.position += value

    def pause_program(self):
        # print('Pausing program at position %d' % self.position)
        self.paused = True

    def set_input(self, input):
        self.input_list = input

    def add_input(self, input):
        self.input_list.extend(input)

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
            param_3 = self.get_parameter_position(position+3, param_modes[2])
            # print('%s + %s = %s -> %s' % (param_1, param_2, param_1+param_2, param_3))
            self.set_value(param_3, param_1 + param_2)
            return 4
        elif op_code == 2:
            # Multiplication
            param_1 = self.get_parameter(position+1, param_modes[0])
            param_2 = self.get_parameter(position+2, param_modes[1])
            param_3 = self.get_parameter_position(position+3, param_modes[2])
            self.set_value(param_3, param_1 * param_2)
            # print('%s * %s = %s -> %s' % (param_1, param_2, param_1*param_2, param_3))
            return 4
        elif op_code == 3:
            # Input
            param_1 = self.get_parameter_position(position+1, param_modes[0])
            # Only run the program while there is input
            # If there is not input pause the program and resume it after input
            # is available
            if len(self.input_list) > 0:
                value = self.input_list.pop(0)
            else:
                self.pause_program()
                return 0

            self.set_value(param_1, value)
            # print('%s -> %s' % (value, param_1))
            return 2
        elif op_code == 4:
            # Output
            param_1 = self.get_parameter(position+1, param_modes[0])
            # track output values
            self.last_value = param_1
            self.output_values.append(param_1)
            # print('%s -> out' % param_1)
            if self.echo:
                print('PRINT-%d' % param_1)
            return 2
        elif op_code == 5:
            # Jump If True
            param_1 = self.get_parameter(position+1, param_modes[0])
            param_2 = self.get_parameter(position+2, param_modes[1])

            if param_1 is not 0:
                self.jump_to(param_2)
                return 0
            else:
                return 3
        elif op_code == 6:
            # Jump If False
            param_1 = self.get_parameter(position+1, param_modes[0])
            param_2 = self.get_parameter(position+2, param_modes[1])

            if param_1 is 0:
                self.jump_to(param_2)
                return 0
            else:
                return 3
        elif op_code == 7:
            # Less Than
            param_1 = self.get_parameter(position+1, param_modes[0])
            param_2 = self.get_parameter(position+2, param_modes[1])
            param_3 = self.get_parameter_position(position+3, param_modes[2])

            if param_1 < param_2:
                self.set_value(param_3, 1)
            else:
                self.set_value(param_3, 0)
            return 4
        elif op_code == 8:
            # Equal
            param_1 = self.get_parameter(position+1, param_modes[0])
            param_2 = self.get_parameter(position+2, param_modes[1])
            param_3 = self.get_parameter_position(position+3, param_modes[2])

            if param_1 == param_2:
                self.set_value(param_3, 1)
            else:
                self.set_value(param_3, 0)
            return 4
        elif op_code == 9:
            param_1 = self.get_parameter(position+1, param_modes[0])
            self.rel_base += param_1
            return 2
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
        elif mode == 2:
            # Relative
            value = self.get_value(self.get_value(position) + self.rel_base)
        else:
            print('Error: Mode %d undefined' % mode)
            return None

        return int(value)

    def get_parameter_position(self, position, mode):
        if mode == 0:
            # Position
            address = self.get_value(position)
        elif mode == 1:
            # Immediate
            address = position
        elif mode == 2:
            # Relative
            address = self.rel_base + self.get_value(position)
        else:
            print('Error: Mode %d undefined' % mode)
            return None

        return address

    def set_value(self, position, value):
        # print('Set Pos: %s to Val: %s' % (position, value))
        if position >= len(self.program):
            for _ in range(0, position - len(self.program) + 1):
                self.program.append(0)

        self.program[position] = value

    def get_value(self, position):
        if position >= len(self.program):
            for _ in range(0, position - len(self.program) + 1):
                self.program.append(0)

        # print('Get Pos: %s' % position)
        return self.program[position]

    def jump_to(self, position):
        self.position = position

    def get_last_value(self):
        return self.last_value

    def get_output_values(self):
        output = self.output_values.copy()
        self.output_values.clear()
        return output

if __name__ == '__main__':
    input_file = './input.txt'
    test1_file = './test1.txt'
    test2_file = './test2.txt'

    puter = IntcodeComputer(input_file)
    puter.set_input([2])
    puter.execute_program()
