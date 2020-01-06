# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 14:16:21 2019

@author: ahenders

Advent of Code, 2019, Day 3
https://adventofcode.com/2019/day/3

PART 1
========
For example, if the first wire's path is R8,U5,L5,D3, then starting from the
central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........
Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4,
and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
These wires cross at two locations (marked X), but the lower-left one is closer
to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

What is the Manhattan distance from the central port to the closest intersection?

PART 2
========


"""
from typing import List, Tuple, Set, Dict

class Wire:
    def __init__ (self, route: List[str]):
        self.nodes = set([])
        self.node_dict = {}
        self.x = 0
        self.y = 0
        self.steps = 0
        self.addRoute(route)
        
    def __str__(self):
        return f'There are {self.steps} in this Wire.'
        
    def getSize(self) -> int:
        return self.steps
        
    def addRoute(self, route):
        for r in route:
            direction = r[0]
            distance = int(r[1:])
            for _ in range(distance):
                self.steps += 1
                if direction == 'R':
                    self.x += 1
                elif direction == 'L':
                    self.x -= 1
                elif direction == 'U':
                    self.y += 1
                elif direction == 'D':
                    self.y -= 1
                
                self.nodes.add((self.x, self.y))
                self.node_dict[(self.x, self.y)] = self.steps                
                    
    def getNodes(self) -> Set[Tuple[int, int]]:
        return self.nodes
    
    def getCollisions(self, other: any) -> Tuple[Set[Tuple[int, int]], Dict[Tuple[int,int],int]]:
        colls = set([])
        coll_dict = {}
        
        colls = self.nodes.intersection(other.getNodes())
        
        for n in other.getNodes():
            if n in self.nodes:
                # colls.add(n)
                coll_dict[n] = self.node_dict[n] + other.node_dict[n]
                
        return colls, coll_dict
                    

if __name__ == '__main__':
    with open ('day03_input.txt', 'r') as inp:
        w1 = inp.readline().strip().split(',')
        w2 = inp.readline().strip().split(',')
        
    wire1 = Wire(w1)
    wire2 = Wire(w2)
    
    collisions, colls_w_steps = wire1.getCollisions(wire2)
    
    # Part 1
    smallest = min(wire1.getSize(), wire2.getSize())
    for c in collisions:
        manhattan_dist = abs(c[0]) + abs(c[1])
        if smallest > manhattan_dist:
            smallest = manhattan_dist
    print(f'Part 1 = {smallest} is the closest Manhattan distance to a collision.')
    
    # Part 2
    print(f'Part 2 = {min(colls_w_steps.values())} is the lowest latency to a collision.')