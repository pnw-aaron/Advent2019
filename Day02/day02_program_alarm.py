# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 10:31:12 2019

@author: ahenders

Advent of Code, 2019, Day 2
https://adventofcode.com/2019/day/2

(Intcode)
Here are the initial and final states of a few more small programs:

1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.

PART 1
=======
Once you have a working computer, the first step is to restore the gravity
assist program (your puzzle input) to the "1202 program alarm" state it had just
before the last computer caught fire. To do this, before running the program,
replace position 1 with the value 12 and replace position 2 with the value 2.
What value is left at position 0 after the program halts?

PART 2
=======
The inputs should still be provided to the program by replacing the values at
addresses 1 and 2, just like before. In this program, the value placed in
address 1 is called the noun, and the value placed in address 2 is called the
verb. Each of the two input values will be between 0 and 99, inclusive.

Once the program has halted, its output is available at address 0, also just
like before. Each time you try a pair of inputs, make sure you first reset the
computer's memory to the values in the program (your puzzle input) - in other
words, don't reuse memory from a previous attempt.

Find the input noun and verb that cause the program to produce the output
19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2, the
answer would be 1202.)

"""

from typing import List, Tuple
# import sys

OUTPUT = 19690720

def run_intcode(prog: List[int]) -> List[int]:
    address = 0
    
    length = len(prog)
    
    while prog[address] != 99:
        
        # Make sure address is not too close to end of program
        if address > length - 3:
            prog[0] = -1
            break
        
        opcode = prog[address]
        p1 = prog[prog[address + 1]]
        p2 = prog[prog[address + 2]]
        dest = prog[address + 3]
        
        # Make sure dest is within bounds of program list
        if dest > length - 1:
            prog[0] = -1
            break
        
        # Add
        if (opcode == 1):
            prog[dest] = p1 + p2
        elif (opcode == 2):
            prog[dest] = p1 * p2
        else:
            # sys.exit('Error: Invalid instruction code\n')
            prog[0] = -1
            break
    
        address += 4
        
        # Make sure address is within bounds of program list
        if address > length - 1 :
            prog[0] = -1
            break
    
    return prog

def find_output(prog: List[int], match:int) -> Tuple[int, int]:
    noun = -1
    verb = -1
    result = 0
    length = len(prog)
    
    while result != match:
        noun += 1
        verb = -1
        while result != match and verb < length - 1:
            verb += 1
            temp_prog = prog.copy()
            temp_prog[1] = noun
            temp_prog[2] = verb
            result = run_intcode(temp_prog)[0]
        if result == match:
            break
    
    return (noun, verb)

assert run_intcode([1,0,0,0,99]) == [2,0,0,0,99]
assert run_intcode([2,3,0,3,99]) == [2,3,0,6,99]
assert run_intcode([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
assert run_intcode([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

if __name__ == '__main__':
    with open ('day02_input.txt', 'r') as inp:
        initial = [int(x) for x in inp.read().strip().split(',')]
    
    # Part 1
    p1_initial = initial.copy()
    p1_initial[1] = 12
    p1_initial[2] = 2
    print('Part 1 = ' + str(run_intcode(p1_initial)[0]))
    
    # Part 2
    n, v = find_output(initial, OUTPUT)
    print('Part 2 = ' + str((100 * n) + v))
    