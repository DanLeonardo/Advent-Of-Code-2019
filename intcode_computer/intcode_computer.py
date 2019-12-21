class IntcodeComputer:
    def __init__(self, file_str, echo=True):
        self._base_program = None   # (list):   Original program. The values are never changed so the program can be 
                                    #           reset if needed
        self._program = None        # (list):   Current program. The values may be changed from the base program.
        self._position = 0          # (int):    Current opcode position in the program.
        self._rel_base = 0          # (int):    Current relative base of the program. This position acts as an offset 
                                    #           when an opcode is run in mode 4.
        self._last_value = None     # (int):    Last value the program has output (OPCODE 4).
        self._output_values = []    # (list):   All output (OPCODE 4) values since _get_output() has been called. Reset
                                    #           after function call.
        self._input_list = []       # (list):   A list of input (OPCODE 3) values so the program can be run automatically.
        self._echo = _echo          # (bool):   Boolean flag if output (OPCODE 4) should be printed to the console.
        self._finished = False      # (bool):   Boolean flag to see if the program has finished.
        self._paused = False        # (bool):   Boolean flag to see if the program has paused.

        self._load_program(file_str)

    def _load_program(self, file_str):
        '''
        @function:  _load_program
        @args:      file_str (str): Local path of the file to be read.
        @comment:   Loads the program from the given file.
                    Populates both ._program and _base_program.
        '''
        with open(file_str) as file:
            self._program = file.read()
            self._program = self._program.rstrip('\n')
            self._program = self._program.split(',')
            self._program = [int(op) for op in self._program]
            self._base_program = [op for op in self._program]

    def reset(self):
        '''
        @function:  reset
        @comment:   Resets the values of the program so it can be ran from its original state.
        '''
        if self._echo:
            print('Intcode: Reseting computer')
        self._program = [op for op in self._base_program]
        self._position = 0
        self._rel_base = 0
        self._input_list =[]
        self._output_values = []
        self._last_value = None
        self._finished = False
        self._paused = False

    def run(self):
        '''
        @function:  run
        @return:    (list): All values that were output from the program until it finished or paused.
        @comment:   Runs the program form its current state. If the program is paused it runs from _position.
        '''
        if self._base_program is None:
            print('IntcodeComputer: No program file given.')
            return None

        if self._finished:
            if self._echo:
                print('IntcodeComputer is finished. Resetting program to original state.')
            self.reset()

        self._paused = False

        while not self._finished and not self._paused:
            value = self._execute_opcode(self._position)

            if value == 99:
                self._finished = True
            elif value == -1:
                print('Error: Stopping Program')
                self._finished = True
            else:
                self._position += value

        return self._output_values

    def read_input(self, input):
        '''
        @function:  read_input
        @args:      input (list) or (int): A single or a list of integer values to be read as input.
        @return:    (list): All values that were output from the program until it finished or paused.
        @comments:  Reads a single or list of integers values and sets _input_list to those value(s). When inputting 
                    multiple input values they are read in the order of input. 
                    read_input also runs the program after inputting the values.
        '''
        if isinstance(input, list):
            self._input_list = input
        else:
            self._input_list = [input]
        return self.run()

    def read_ascii(self, input):
        '''
        @function:  read_ascii
        @args:      input (str): A string to be converted into ascii values and set as input.
        @return:    (list): All values that were output from the program until it finished or paused.
        @comments:  read_ascii also runs the program after inputting the values.
        '''
        self._input_list = [ord(char) for char in input]
        return self.run()

    def add_input(self, input):
        '''
        @function:  add_input
        @args:      input (list): A list of integer values to be added on to the current input values.
        @comments:  add_input extends _input_list instead of overwriting the current values.
                    This function does not run the program like the other read functions.
        '''
        self._input_list.extend(input)

    def _pause_program(self):
        '''
        @function:  _pause_program
        @comments:  A private function that sets the _paused flag to True stopping the program from executing more 
                    opcodes.
        '''
        # print('Pausing program at position %d' % self._position)
        self._paused = True

    def _execute_opcode(self, position):
        '''
        @function:  _execute_opcode
        @args:      position (int): The position in memory of the opcode to run.
        @comments:  Executes a single opcode at the given position.
        '''
        # Read full opcode
        operation = str(self._program[position])

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
            param_1 = self._get_parameter(position+1, param_modes[0])
            param_2 = self._get_parameter(position+2, param_modes[1])
            param_3 = self._get_parameter_position(position+3, param_modes[2])
            # print('%s + %s = %s -> %s' % (param_1, param_2, param_1+param_2, param_3))
            self._set_value(param_3, param_1 + param_2)
            return 4
        elif op_code == 2:
            # Multiplication
            param_1 = self._get_parameter(position+1, param_modes[0])
            param_2 = self._get_parameter(position+2, param_modes[1])
            param_3 = self._get_parameter_position(position+3, param_modes[2])
            self._set_value(param_3, param_1 * param_2)
            # print('%s * %s = %s -> %s' % (param_1, param_2, param_1*param_2, param_3))
            return 4
        elif op_code == 3:
            # Input
            param_1 = self._get_parameter_position(position+1, param_modes[0])
            # Only run the program while there is input
            # If there is not input pause the program and resume it after input
            # is available
            if len(self._input_list) > 0:
                value = self._input_list.pop(0)
            else:
                self._pause_program()
                return 0

            self._set_value(param_1, value)
            # print('%s -> %s' % (value, param_1))
            return 2
        elif op_code == 4:
            # Output
            param_1 = self._get_parameter(position+1, param_modes[0])
            # track output values
            self._last_value = param_1
            self._output_values.append(param_1)
            # print('%s -> out' % param_1)
            if self._echo:
                print('PRINT-%d' % param_1)
            return 2
        elif op_code == 5:
            # Jump If True
            param_1 = self._get_parameter(position+1, param_modes[0])
            param_2 = self._get_parameter(position+2, param_modes[1])

            if param_1 is not 0:
                self._jump_to(param_2)
                return 0
            else:
                return 3
        elif op_code == 6:
            # Jump If False
            param_1 = self._get_parameter(position+1, param_modes[0])
            param_2 = self._get_parameter(position+2, param_modes[1])

            if param_1 is 0:
                self._jump_to(param_2)
                return 0
            else:
                return 3
        elif op_code == 7:
            # Less Than
            param_1 = self._get_parameter(position+1, param_modes[0])
            param_2 = self._get_parameter(position+2, param_modes[1])
            param_3 = self._get_parameter_position(position+3, param_modes[2])

            if param_1 < param_2:
                self._set_value(param_3, 1)
            else:
                self._set_value(param_3, 0)
            return 4
        elif op_code == 8:
            # Equal
            param_1 = self._get_parameter(position+1, param_modes[0])
            param_2 = self._get_parameter(position+2, param_modes[1])
            param_3 = self._get_parameter_position(position+3, param_modes[2])

            if param_1 == param_2:
                self._set_value(param_3, 1)
            else:
                self._set_value(param_3, 0)
            return 4
        elif op_code == 9:
            # Add to Relative Base
            param_1 = self._get_parameter(position+1, param_modes[0])
            self._rel_base += param_1
            return 2
        elif op_code == 99:
            # Finish
            return 99
        else:
            # Error
            print('Error: Received code %s' % op_code)
            return -1

    def _get_parameter(self, position, mode):
        '''
        @function:  _get_parameter
        @args:      position (int): The position in memory of the parameter to get.
                    mode (int): The mode to get the parameter in. E.g. Position, Immediate, Relative
        @return:    The value of the parameter.
        @comments:  A private function to simplify retrieving parameters. Gets the wanted value given the memory 
                    position and mode.
        '''
        if mode == 0:
            # Position
            address = self._get_value(position)
            value = self._get_value(address)
        elif mode == 1:
            # Immediate
            value = self._get_value(position)
        elif mode == 2:
            # Relative
            value = self._get_value(self._get_value(position) + self._rel_base)
        else:
            print('Error: Mode %d undefined' % mode)
            return None

        return int(value)

    def _get_parameter_position(self, position, mode):
        '''
        @function:  _get_parameter_position
        @args:      position (int): The position in memory of the parameter to get.
                    mode (int): The mode to get the parameter in. E.g. Position, Immediate, Relative
        @return:    The value of the parameter.
        @comments:  A private function similar to _get_parameter. Instead this function returns the position in memory 
                    of the parameter given the memory position and mode.
        '''
        if mode == 0:
            # Position
            address = self._get_value(position)
        elif mode == 1:
            # Immediate
            address = position
        elif mode == 2:
            # Relative
            address = self._rel_base + self._get_value(position)
        else:
            print('Error: Mode %d undefined' % mode)
            return None

        return address

    def _set_value(self, position, value):
        '''
        @function:  _set_value
        @args:      position (int): The position in memory to set.
                    value (int): The value to set to.
        @comments:  A private functino that sets the memory at position to value.
        '''
        # print('Set Pos: %s to Val: %s' % (position, value))
        if position >= len(self._program):
            for _ in range(0, position - len(self._program) + 1):
                self._program.append(0)

        self._program[position] = value

    def _get_value(self, position):
        '''
        @function:  _get_value
        @args:      position (int): The position in memory to get.
        @return:    (int): The value in memory at position.
        @comments:  A private function that returns the value in memory at position.
        '''
        if position >= len(self._program):
            for _ in range(0, position - len(self._program) + 1):
                self._program.append(0)

        # print('Get Pos: %s' % position)
        return self._program[position]

    def _jump_to(self, position):
        '''
        @function:  _jump_to
        @args:      position (int): The point in memory to set _position to
        @comments:  A private function that sets _position to a new point in memory.
        '''
        self._position = position

    def get_last_value(self):
        '''
        @function:  get_last_value
        @return:    (int): The last value printed (OPCODE 4)
        @comments:  Returns the last value that was printed (OPCODE 4).
                    _last_value persists even after _output_values is cleared.
        '''
        return self._last_value

    def get_output(self):
        '''
        @function:  get_output
        @return:    (list): All values printed (OPCODE 4) since the program began or get_output was last called.
        @comments:  Returns all values printed (OPCODE 4) since the program begain or get_output was last called.
                    _output_values is cleared after this functions is called to not confused outputs if the program 
                    pauses and outputs several times.
        '''
        output = self._output_values.copy()
        self._output_values.clear()
        return output

if __name__ == '__main__':
    computer = IntcodeComputer('./input.txt')
    output = computer.read_input(5)
    print(output)