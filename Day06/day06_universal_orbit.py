# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 17:27:59 2019

@author: ahenders

Advent of Code, 2019, Day 6
https://adventofcode.com/2019/day/6

PART 1
========
Visually, the above map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I
In this visual representation, when two objects are connected by a line, the
one on the right directly orbits the one on the left.

Here, we can count the total number of orbits as follows:

D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7
orbits.
COM orbits nothing.
The total number of direct and indirect orbits in this example is 42.

What is the total number of direct and indirect orbits in your map data?

PART 2
========
Visually, the above map of orbits looks like this:

                          YOU
                         /
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
In this example, YOU are in orbit around K, and SAN is in orbit around I. To
move from K to I, a minimum of 4 orbital transfers are required:

K to J
J to E
E to D
D to I
Afterward, the map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
                 \
                  YOU
What is the minimum number of orbital transfers required to move from the
object YOU are orbiting to the object SAN is orbiting? (Between the objects
they are orbiting - not between YOU and SAN.)

"""

from typing import Dict, List

def make_tree(orbits: List[str]) -> Dict[str, str]:
    tree = {}
    
    for o in orbits:
        parent, child = o.split(')')
        tree[child] = parent
    
    return tree

def get_orbit_count(node: str, galaxy: Dict[str, str]) -> int:
    count = 0
    child = node
    
    while child != 'COM':
        count += 1
        child = galaxy[child]

    return count

EX1 = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L']
ex_tree = make_tree(EX1)

assert get_orbit_count('D', ex_tree) == 3
assert get_orbit_count('L', ex_tree) == 7
assert get_orbit_count('COM', ex_tree) == 0

def get_total_orbit_count(galaxy: Dict[str, str]) -> int:
    return sum(get_orbit_count(child, galaxy) for child in galaxy)

assert get_total_orbit_count(ex_tree) == 42

EX2 = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L','K)YOU','I)SAN']
ex_tree2 = make_tree(EX2)

def get_path_to_root(node: str, galaxy: Dict[str, str]) -> List[str]:
    path = []
    child = node
    
    while child != 'COM':
        path.append(galaxy[child])
        child = galaxy[child]
    
    return path

assert get_path_to_root('YOU', ex_tree2) == ['K','J','E','D','C','B','COM']
assert get_path_to_root('SAN', ex_tree2) == ['I','D','C','B','COM']

def get_transfer(node1: str, node2: str, galaxy: Dict[str, str]) -> int:
    p1 = get_path_to_root(node1, galaxy)
    p2 = get_path_to_root(node2, galaxy)

    while p1 and p2 and p1[-1] == p2[-1]:
        p1.pop()
        p2.pop()
    
    return len(p1) + len(p2)

assert get_transfer('YOU','SAN', ex_tree2) == 4

if __name__ == '__main__':
    with open ('day06_input.txt', 'r') as inp:
        raw = [line.strip() for line in inp]
        
    orbits = make_tree(raw)
    
    # Part 1
    print(f'Part 1 Output: {get_total_orbit_count(orbits)} total orbits')
    
    # Part 2
    print(f'Part 2 Output: {get_transfer("YOU","SAN", orbits)} total tranfers')
