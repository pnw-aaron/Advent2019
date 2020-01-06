# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:46:36 2019

@author: ahenders

Advent of Code, 2019, Day 5
https://adventofcode.com/2019/day/5

PART 1
========
First, you'll need to add two new instructions:

Opcode 3 takes a single integer as input and saves it to the position given by
its only parameter. For example, the instruction 3,50 would take an input value
and store it at address 50.
Opcode 4 outputs the value of its only parameter. For example, the instruction
4,50 would output the value at address 50.

PART 2
========
Your computer is only missing a few opcodes:

Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the
instruction pointer to the value from the second parameter. Otherwise, it does
nothing.
Opcode 6 is jump-if-false: if the first parameter is zero, it sets the
instruction pointer to the value from the second parameter. Otherwise,
it does nothing.
Opcode 7 is less than: if the first parameter is less than the second parameter,
it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
Opcode 8 is equals: if the first parameter is equal to the second parameter, it
stores 1 in the position given by the third parameter. Otherwise, it stores 0.

Like all instructions, these instructions need to support parameter modes as
described above.

Normally, after an instruction is finished, the instruction pointer increases
by the number of values in that instruction. However, if the instruction modifies
the instruction pointer, that value is used and the instruction pointer is not
automatically increased.
"""
from typing import List, NamedTuple
from collections import namedtuple

Instruction = namedtuple('Instruction', 'opcode p1_mode p2_mode p3_mode length')

def parse_instruction(inst:int) -> NamedTuple:
    # Opcode
    opcode = inst % 100
    if opcode == 8:
        print(inst)
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
    elif (opcode == 3 or opcode == 4):
        length = 2
    elif (opcode == 5 or opcode == 6):
        length = 3
    elif (opcode == 99):
        length = 0
    else:
        raise RuntimeError()
    
    return Instruction(opcode, p1_mode, p2_mode, p3_mode, length)

def run_intcode(prog: List[int], input_value: int) -> List[int]:
    address = 0
    p1 = p2 = p3 = 0
    
    prog_length = len(prog)
    instruction = parse_instruction(prog[address])
    
    while instruction[0] != 99:
        # print(address, instruction,prog[address:address+4])
        
        # Make sure address is not too close to end of program
        if address + instruction.length >= prog_length:
            raise RuntimeError(1)
            break
        
        # Opcode
        opcode = instruction.opcode

        # Add or Multiply
        if (instruction.opcode == 1 or instruction.opcode == 2 or
            instruction.opcode == 7 or instruction.opcode == 8):
            # P1
            if instruction.p1_mode:
                p1 = prog[address + 1]
            else:
                p1 = prog[prog[address + 1]]
            # P2
            if instruction.p2_mode:
                p2 = prog[address + 2]
            else:
                p2 = prog[prog[address + 2]]
            # P3
            p3 = prog[address + 3]
            
            if p3 > prog_length - 1 and not instruction.p3_mode:
                raise RuntimeError()
                break
        # Input or Output
        elif (instruction.opcode == 3 or instruction.opcode == 4):
            # P1
            p1 = prog[address + 1]
            
            if p1 > prog_length - 1 and not instruction.p1_mode:
                raise RuntimeError()
                break
        # Jump-If-False or Jump-If-True
        elif (instruction.opcode == 5 or instruction.opcode == 6):
            # P1
            if instruction.p1_mode:
                p1 = prog[address + 1]
            else:
                p1 = prog[prog[address + 1]]
            
            # P2
            if instruction.p2_mode:
                p2 = prog[address + 2]
            else:
                p2 = prog[prog[address + 2]]
        
        # Add
        if (opcode == 1):
            prog[p3] = p1 + p2
        # Multiply
        elif (opcode == 2):
            prog[p3] = p1 * p2
        # Input
        elif (opcode == 3):
            prog[p1] = input_value
        # Output
        elif (opcode == 4):
            print(prog[p1])
        # Jump-If-True
        elif (opcode == 5):
            if not (p1 == 0):
                address = p2
                # Make sure address is within bounds of program list
                if address > prog_length - 1 :
                    raise RuntimeError()
            
                instruction = parse_instruction(prog[address])
                continue
        # Jump-If-False
        elif (opcode == 6):
            if (p1 == 0):
                address = p2
                # Make sure address is within bounds of program list
                if address > prog_length - 1 :
                    raise RuntimeError()
            
                instruction = parse_instruction(prog[address])
                continue
        # Less-Than
        elif (opcode == 7):
            if (p1 < p2):
                prog[p3] = 1
            else:
                prog[p3] = 0
        elif (opcode == 8):
            if (p1 == p2):
                prog[p3] = 1
            else:
                prog[p3] = 0
        else:
            raise RuntimeError()
            break
    
        address += instruction.length
        
        # Make sure address is within bounds of program list
        if address > prog_length - 1 :
            raise RuntimeError()
        
        instruction = parse_instruction(prog[address])
    
    return prog

assert (parse_instruction(1002) == Instruction(2, 0, 1, 0, 4))

if __name__ == '__main__':
    with open ('day05_input.txt', 'r') as inp:
        initial = [int(x) for x in inp.read().strip().split(',')]

    P1_INPUT = 1
    P2_INPUT = 5
    
    # Part 1
    print(f'Part 1 Output:')
    p1_prog = run_intcode(initial.copy(), P1_INPUT)

    
    # Part 2
    print(f'Part 2 Output:')
    p2_prog = run_intcode(initial.copy(), P2_INPUT)