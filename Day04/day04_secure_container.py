# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 08:43:27 2019

@author: ahenders

Advent of Code, 2019, Day 4
https://adventofcode.com/2019/day/4

PART 1
========
The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or
stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet
these criteria?


PART 2
========
An Elf just remembered one more important detail: the two adjacent matching
digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the
following are now true:

112233 meets these criteria because the digits never decrease and all repeated
digits are exactly two digits long.
123444 no longer meets the criteria (the repeated 44 is part of a larger group
of 444).
111122 meets the criteria (even though 1 is repeated more than twice, it still
contains a double 22).

How many different passwords within the range given in your puzzle input meet
all of the criteria?

"""
from typing import Set
from collections import Counter

# This turns out to be slower than match_adjacent_not_group
# Though, it is more "Pythonic"
def match2(num_str: str) -> bool:
    counts = Counter(num_str)
    return any(v == 2 for v in counts.values())

def match_adjacent_not_group(num_str: str) -> bool:
    match = False
    in_group = False
    
    for i in range(1, len(num_str)):
        if num_str[i] == num_str[i - 1]:
            if match or in_group:
                in_group = True
                match = False
            else:
                match = True
        else:
            if match:
                return True
            in_group = False
                
    return match

def is_increasing(num_str: str) -> bool:
    nums = [int(d) for d in num_str]
    return all(x <= y for x, y in zip(nums, nums[1:]))

def has_match(num_str: str) -> bool:
    return any(x == y for x, y in zip(num_str, num_str[1:]))

def is_valid(number: int, r1: int, r2: int, strict: bool, length: int = 6) -> bool:
    i_str = str(number)
    if not (len(i_str) == length):
        return False
    if not ((r1 <= number) and (number <= r2)):
        return False
    if strict and not match_adjacent_not_group(i_str):
        return False
    else:
        if not has_match(i_str):
            return False
    if not is_increasing(i_str):
        return False
    
    return True
    
def get_all_valid_pwd(begin: int, end: int, strict: bool) -> Set[int]:
    valid = set([])
    
    for i in range(begin, end + 1):
        if is_valid(i, begin, end, strict):
            valid.add(i)
        
    return valid

# Part 1 asserts
assert is_valid(111111, 100000, 300000, False) == True
assert is_valid(223450, 100000, 300000, False) == False
assert is_valid(123789, 100000, 300000, False) == False

# Part 2 asserts
assert is_valid(112233, 100000, 300000, True) == True
assert is_valid(123444, 100000, 300000, True) == False
assert is_valid(111122, 100000, 300000, True) == True
    
if __name__ == '__main__':
    [low,high] = [int(x) for x in '264793-803935'.split('-')]
    
    # Part 1
    all_valid = get_all_valid_pwd(low, high, False)
    print(f'Part 1 = There are {len(all_valid)} valid passwords in INPUT range.')
    
    # Part 2
    all_valid = get_all_valid_pwd(low, high, True)
    print(f'Part 2 = There are {len(all_valid)} valid passwords in INPUT range.')