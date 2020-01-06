# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 09:47:32 2019

@author: ahenders

Advent of Code, 2019, Day 1
https://adventofcode.com/2019/day/1

PART 1
=======
Fuel required to launch a given module is based on its mass. Specifically, to
find the fuel required for a module, take its mass, divide by three, round down,
and subtract 2.

For example:

For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel
required is also 2.
For a mass of 1969, the fuel required is 654.
For a mass of 100756, the fuel required is 33583.

The Fuel Counter-Upper needs to know the total fuel requirement. To find it,
individually calculate the fuel needed for the mass of each module (your puzzle
input), then add together all the fuel values.

PART 2
========
Fuel itself requires fuel just like a module - take its mass, divide by three,
round down, and subtract 2. However, that fuel also requires fuel, and that fuel
requires fuel, and so on. Any mass that would require negative fuel should
instead be treated as if it requires zero fuel; the remaining mass, if any, is
instead handled by wishing really hard, which has no mass and is outside the
scope of this calculation.

So, for each module mass, calculate its fuel and add it to the total. Then,
treat the fuel amount you just calculated as the input mass and repeat the
process, continuing until a fuel requirement is zero or negative. For example:

A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2
divided by 3 and rounded down is 0, which would call for a negative fuel), so
the total fuel required is still just 2.
At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216
more fuel (654 / 3 - 2). 216 then requires 70 more fuel, which requires 21 fuel,
which requires 5 fuel, which requires no further fuel. So, the total fuel
required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 +
3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.

What is the sum of the fuel requirements for all of the modules on your
spacecraft when also taking into account the mass of the added fuel? (Calculate
the fuel requirements for each module separately, then add them all up at the
end.)
"""
from typing import Callable, List

def calculate_fuel(mass: int) -> int:
    return (mass // 3) - 2

def calculate_fuel_recursive(mass: int) -> int:
    if (mass // 3) - 2 <= 0:
        return 0
    else:
        return(((mass // 3) - 2) + calculate_fuel_recursive((mass // 3) - 2))

def calculate_total_fuel(calc: Callable, module_list: List[int]) -> int:
    total = 0
    
    for m in module_list:
        total += calc(m)
        
    return total

assert (calculate_fuel(12) == 2)
assert (calculate_fuel(14) == 2)
assert (calculate_fuel(1969) == 654)
assert (calculate_fuel(100756) == 33583)

assert (calculate_fuel_recursive(14) == 2)
assert (calculate_fuel_recursive(1969) == 966)
assert (calculate_fuel_recursive(100756) == 50346)

if __name__ == '__main__':
    with open ('day01_input.txt', 'r') as inp:
        modules = [int(line.strip()) for line in inp]
    
    # Part 1
    print('Part 1 = ' + str(calculate_total_fuel(calculate_fuel, modules)))
    
    # Part 2
    print('Part 2 = ' + str(calculate_total_fuel(calculate_fuel_recursive, modules)))
    