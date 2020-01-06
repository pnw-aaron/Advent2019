# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 21:13:54 2019

@author: ahenders

Advent of Code, 2019, Day 7
https://adventofcode.com/2019/day/7

PART 1
========
For example, suppose you want to try the phase setting sequence 3,1,2,4,0,
which would mean setting amplifier A to phase setting 3, amplifier B to setting
1, C to 2, D to 4, and E to 0. Then, you could determine the output signal that
gets sent from amplifier E to the thrusters with the following steps:

Start the copy of the amplifier controller software that will run on amplifier
A. At its first input instruction, provide it the amplifier's phase setting, 3.
At its second input instruction, provide it the input signal, 0. After some
calculations, it will use an output instruction to indicate the amplifier's
output signal.
Start the software for amplifier B. Provide it the phase setting (1) and then
whatever output signal was produced from amplifier A. It will then produce a new
output signal destined for amplifier C.
Start the software for amplifier C, provide the phase setting (2) and the value
from amplifier B, then collect its output signal.
Run amplifier D's software, provide the phase setting (4) and input value, and
collect its output signal.
Run amplifier E's software, provide the phase setting (0) and input value, and
collect its output signal.

The final output signal from amplifier E would be sent to the thrusters.
However, this phase setting sequence may not have been the best one; another
sequence might have sent a higher signal to the thrusters.

Here are some example programs:

Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):

3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):

3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0
Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):

3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0

Try every combination of phase settings on the amplifiers. What is the highest
signal that can be sent to the thrusters?

PART 2
========
In feedback loop mode, the amplifiers need totally different phase settings: integers
from 5 to 9, again each used exactly once. These settings will cause the Amplifier
Controller Software to repeatedly take input and produce output many times before
halting. Provide each amplifier its phase setting at its first input instruction;
all further input/output instructions are for signals.

Don't restart the Amplifier Controller Software on any amplifier during this
process. Each one should continue receiving and sending signals until it halts.

All signals sent or received in this process will be between pairs of amplifiers
except the very first signal and the very last signal. To start the process, a 0
signal is sent to amplifier A's input exactly once.

Eventually, the software on the amplifiers will halt after they have processed
the final loop. When this happens, the last output signal from amplifier E is
sent to the thrusters. Your job is to find the largest output signal that can be
sent to the thrusters using the new phase settings and feedback loop arrangement.

Here are some example programs:

Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):

3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5

Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):

3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10

Try every combination of the new phase settings on the amplifier feedback loop.
What is the highest signal that can be sent to the thrusters?
"""

from typing import List, NamedTuple, Tuple
from collections import namedtuple
from itertools import permutations

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
        raise RuntimeError(f'Invalid opcode: {opcode}')
    
    return Instruction(opcode, p1_mode, p2_mode, p3_mode, length)

def run_intcode(prog: List[int], in1: int, in2: int) -> List[int]:
    address = 0
    in1_used = False
    p1 = p2 = p3 = 0
    
    prog_length = len(prog)
    instruction = parse_instruction(prog[address])
    
    while instruction.opcode != 99:
        # print(address, instruction,prog[address:address+4])
        
        # Make sure address is not too close to end of program
        if address + instruction.length >= prog_length:
            raise RuntimeError(f'Address (will be) out of program bounds: \
                                 {address + instruction.length}')
            break

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
                raise RuntimeError(f'Address (will be) out of program bounds: \
                                     {address + instruction.length}')
                break
        # Input or Output
        elif (instruction.opcode == 3 or instruction.opcode == 4):
            # P1
            p1 = prog[address + 1]
            
            if p1 > prog_length - 1 and not instruction.p1_mode:
                raise RuntimeError(f'Address (will be) out of program bounds: \
                                     {address + instruction.length}')
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
        if (instruction.opcode == 1):
            prog[p3] = p1 + p2
        # Multiply
        elif (instruction.opcode == 2):
            prog[p3] = p1 * p2
        # Input
        elif (instruction.opcode == 3):
            if in1_used:
                prog[p1] = in2
            else:
                prog[p1] = in1
                in1_used = True
            # prog[p1] = input_value
        # Output
        elif (instruction.opcode == 4):
            prog_output = prog[p1]
        # Jump-If-True
        elif (instruction.opcode == 5):
            if not (p1 == 0):
                address = p2
                # Make sure address is within bounds of program list
                if address > prog_length - 1 :
                    raise RuntimeError(f'Address out of program bounds: {address}')
            
                instruction = parse_instruction(prog[address])
                continue
        # Jump-If-False
        elif (instruction.opcode == 6):
            if (p1 == 0):
                address = p2
                # Make sure address is within bounds of program list
                if address > prog_length - 1 :
                    raise RuntimeError(f'Address out of program bounds: {address}')
            
                instruction = parse_instruction(prog[address])
                continue
        # Less-Than
        elif (instruction.opcode == 7):
            if (p1 < p2):
                prog[p3] = 1
            else:
                prog[p3] = 0
        elif (instruction.opcode == 8):
            if (p1 == p2):
                prog[p3] = 1
            else:
                prog[p3] = 0
        else:
            raise RuntimeError(f'Invalid opcode: {instruction.opcode}')
            break
    
        address += instruction.length
        
        # Make sure address is within bounds of program list
        if address > prog_length - 1 :
            raise RuntimeError(f'Address out of program bounds: {address}')
        
        instruction = parse_instruction(prog[address])
    
    return prog_output

def get_thrust_signal(start: int, seq: Tuple[int], program: List[int]) -> int:
    signal = start
    
    for phase in seq:
        signal = run_intcode(program.copy(), phase, signal)
    
    return signal

p1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
s1 = (4,3,2,1,0)
assert get_thrust_signal(0, s1, p1.copy()) == 43210

p2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
s2 = (0,1,2,3,4)
assert get_thrust_signal(0, s2, p2.copy()) == 54321

p3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
s3 = (1,0,4,3,2)
assert get_thrust_signal(0, s3, p3.copy()) == 65210

def get_max_thrust(start: int, program: List[int], feedback_mode: bool) -> Tuple[int, List[int]]:
    max_thrust = start
    max_seq = []
    
    if feedback_mode:
        for perm in permutations(range(5,10)):
            pass
    else:
        for perm in permutations(range(5)):
            this_thrust = get_thrust_signal(start, perm, program.copy())
            if this_thrust > max_thrust:
                max_thrust = this_thrust
                max_seq = []
                for p in perm:
                    max_seq.append(p)

    return max_thrust, max_seq

t1, os1 = get_max_thrust(0, p1.copy(), False)
assert t1 == 43210 and os1 == [4,3,2,1,0]

t2, os2 = get_max_thrust(0, p2.copy(), False)
assert t2 == 54321 and os2 == [0,1,2,3,4]

t3, os3 = get_max_thrust(0, p3.copy(), False)
assert t3 == 65210 and os3 == [1,0,4,3,2]

if __name__ == '__main__':
    with open ('day07_input.txt', 'r') as inp:
        initial = [int(x) for x in inp.read().strip().split(',')]

    INPUT = 0
        
    # Part 1
    thrust1, m_seq1 = get_max_thrust(INPUT, initial.copy(), False)
    print(f'Part 1 Output: The max thrust is {thrust1}.')
    
    # Part 2
    thrust2, m_seq2 = get_max_thrust(INPUT, initial.copy(), True)
    print(f'Part 2 Output: The max thrust is {thrust2}.')