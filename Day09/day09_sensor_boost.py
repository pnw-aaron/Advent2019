# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 10:55:05 2019

@author: ahenders

Advent of Code, 2019, Day 9
https://adventofcode.com/2019/day/9

PART 1
========
Your existing Intcode computer is missing one key feature: it needs support for
parameters in relative mode.

Parameters in mode 2, relative mode, behave very similarly to parameters in
position mode: the parameter is interpreted as a position. Like position mode,
parameters in relative mode can be read from or written to.

The important difference is that relative mode parameters don't count from
address 0. Instead, they count from a value called the relative base. The
relative base starts at 0.

The address a relative mode parameter refers to is itself plus the current
relative base. When the relative base is 0, relative mode parameters and
position mode parameters with the same value refer to the same address.

For example, given a relative base of 50, a relative mode parameter of -7 refers
to memory address 50 + -7 = 43.

The relative base is modified with the relative base offset instruction:

Opcode 9 adjusts the relative base by the value of its only parameter. The
relative base increases (or decreases, if the value is negative) by the value
of the parameter.
For example, if the relative base is 2000, then after the instruction 109,19,
the relative base would be 2019. If the next instruction were 204,-34, then the
value at address 1985 would be output.

Your Intcode computer will also need a few other capabilities:

The computer's available memory should be much larger than the initial program.
Memory beyond the initial program starts with the value 0 and can be read or
written like any other memory. (It is invalid to try to access memory at a
negative address, though.)
The computer should have support for large numbers. Some instructions near the
beginning of the BOOST program will verify this capability.
Here are some example programs that use these features:

109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input and
produces a copy of itself as output.
1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
104,1125899906842624,99 should output the large number in the middle.

The BOOST program will ask for a single input; run it in test mode by providing
it the value 1. It will perform a series of checks on each opcode, output any
opcodes (and the associated parameter modes) that seem to be functioning
incorrectly, and finally output a BOOST keycode.

Once your Intcode computer is fully functional, the BOOST program should report
no malfunctioning opcodes when run in test mode; it should only output a single
value, the BOOST keycode. What BOOST keycode does it produce?

PART 2
========
You now have a complete Intcode computer.

Finally, you can lock on to the Ceres distress signal! You just need to boost
your sensors using the BOOST program.

The program runs in sensor boost mode by providing the input instruction the
value 2. Once run, it will boost the sensors automatically, but it might take
a few seconds to complete the operation on slower hardware. In sensor boost
mode, the program will output a single value: the coordinates of the distress
signal.

Run the BOOST program in sensor boost mode. What are the coordinates of the
distress signal?
"""

from typing import List, NamedTuple, Dict
from collections import namedtuple, defaultdict

Instruction = namedtuple('Instruction', 'opcode p1_mode p2_mode p3_mode length')

def parse_instruction(inst:int) -> NamedTuple:
    # Opcode
    opcode = inst % 100
    inst = inst // 100
    
    # P1
    p1_mode = inst % 10
    inst = inst // 10
    
    # P2, if exists
    if inst > 0:
        p2_mode = inst % 10
        inst = inst // 10
    else:
        p2_mode = 0
    
    # P3, if exists
    if inst > 0:
        p3_mode = inst
    else:
        p3_mode = 0
        
    if (opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8):
        length = 4
    elif (opcode == 3 or opcode == 4 or opcode == 9):
        length = 2
    elif (opcode == 5 or opcode == 6):
        length = 3
    elif (opcode == 99):
        length = 0
    else:
        raise ValueError(f'Invalid opcode: {opcode}')
    
    return Instruction(opcode, p1_mode, p2_mode, p3_mode, length)

def dict_to_list(mydict: Dict[int, int]) -> List[int]:
    temp = []
    
    for k in range(max(mydict.keys()) + 1):
        temp.append(mydict[k])
    
    return temp

def run_intcode(program: List[int], input_value: int) -> List[int]:
    address = 0
    # in1_used = False
    relative_base = 0
    
    prog = defaultdict(int)
    prog.update({i: value for i, value in enumerate(program)})
    
    prog_length = len(prog)
    instruction = parse_instruction(prog[address])
    
    while instruction.opcode != 99:
        p1 = p2 = p3 = None
        
        # myprog = dict_to_list(prog)
        # print(address, instruction, relative_base, myprog[:16])
        # if (len(myprog) > 100):
        #      print(myprog[100:102])
        # print(address, instruction, relative_base, prog[:9])
        
        # Add or Multiply or Less-Than or Equals
        if (instruction.opcode == 1 or instruction.opcode == 2 or
            instruction.opcode == 7 or instruction.opcode == 8):
            # P1
            p1 = prog[address + 1]

            # P2
            p2 = prog[address + 2]

            # P3
            p3 = prog[address + 3]

        # Input or Output or Adjust-Relative-Base
        elif (instruction.opcode == 3 or instruction.opcode == 4 or
              instruction.opcode == 9):
            # P1
            p1 = prog[address + 1]
            
        # Jump-If-False or Jump-If-True
        elif (instruction.opcode == 5 or instruction.opcode == 6):
            # P1
            p1 = prog[address + 1]
            
            # P2
            p2 = prog[address + 2]

        # Set args[1,2,3] by parameter modes
        if not p1 == None:
            if (instruction.length > 2):
                if (instruction.p1_mode == 2):
                    arg1 = prog[relative_base + p1]
                elif (instruction.p1_mode == 1):
                    arg1 = p1
                elif (instruction.p1_mode == 0):
                    arg1 = prog[p1]
                else:
                    raise ValueError(f'Invalid P1 mode: {instruction.p1_mode}')
            else:
                if (instruction.p1_mode == 2):
                    arg1 = relative_base + p1
                elif (instruction.p1_mode == 1):
                    arg1 = address + 1
                elif (instruction.p1_mode == 0):
                    arg1 = p1
                else:
                    raise ValueError(f'Invalid P1 mode: {instruction.p1_mode}') 
        if not p2 == None:
            if (instruction.length > 3):
                if (instruction.p2_mode == 2):
                    arg2 = prog[relative_base + p2]
                elif (instruction.p2_mode == 1):
                    arg2 = p2
                elif (instruction.p2_mode == 0):
                    arg2 = prog[p2]
                else:
                    raise ValueError(f'Invalid P2 mode: {instruction.p2_mode}')
            else:
                if (instruction.p2_mode == 2):
                    arg2 = relative_base + p2
                elif (instruction.p2_mode == 1):
                    arg2 = address + 2
                elif (instruction.p2_mode == 0):
                    arg2 = p2
                else:
                    raise ValueError(f'Invalid P2 mode: {instruction.p2_mode}') 
        if not p3 == None:
            if (instruction.p3_mode == 2):
                arg3 = relative_base + p3
            elif (instruction.p3_mode == 1):
                arg3 = address + 3
            elif (instruction.p3_mode == 0):
                arg3 = p3
            else:
                raise ValueError(f'Invalid P3 mode: {instruction.p3_mode}')        
        
        # Add
        if (instruction.opcode == 1):
            prog[arg3] = arg1 + arg2

        # Multiply
        elif (instruction.opcode == 2):
            prog[arg3] = arg1 * arg2

        # Input
        elif (instruction.opcode == 3):
            prog[arg1] = input_value

        # Output
        elif (instruction.opcode == 4):
            prog_output = prog[arg1]
            # print(f'  OUTPUT --> {prog_output}')

        # Jump-If-True
        elif (instruction.opcode == 5):
            if not (arg1 == 0):
                address = prog[arg2]
            
                instruction = parse_instruction(prog[address])
                continue

        # Jump-If-False
        elif (instruction.opcode == 6):
            if (arg1 == 0):
                address = prog[arg2]

                instruction = parse_instruction(prog[address])
                continue

        # Less-Than
        elif (instruction.opcode == 7):
            if (arg1 < arg2):
                prog[arg3] = 1
            else:
                prog[arg3] = 0

        # Equals
        elif (instruction.opcode == 8):
            if (arg1 == arg2):
                prog[arg3] = 1
            else:
                prog[arg3] = 0

        # Adjust-Relative-Base
        elif (instruction.opcode == 9):
                relative_base += prog[arg1]

        else:
            raise ValueError(f'Invalid opcode: {instruction.opcode}')
    
        address += instruction.length
        
        instruction = parse_instruction(prog[address])
    
    return prog_output

# run_intcode([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], 0)
# assert len(str((run_intcode([1102,34915192,34915192,7,4,7,99,0], 0)))) == 16
# assert (run_intcode([104,1125899906842624,99],0) == 1125899906842624)

if __name__ == '__main__':
    with open ('day09_input.txt', 'r') as inp:
        initial = [int(i) for i in inp.read().strip().split(',')]
    
    p1_out = p2_out = None
    
    # Part 1
    p1_out = run_intcode(initial.copy(), 1)
    print(f'Part 1 Output: {p1_out}')
    
    # Part 2
    p2_out = run_intcode(initial.copy(), 2)
    print(f'Part 2 Output: {p2_out}')