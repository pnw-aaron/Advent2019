# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 16:11:58 2019

@author: ahenders

Advent of Code, 2019, Day 8
https://adventofcode.com/2019/day/8

PART 1
========
Images are sent as a series of digits that each represent the color of a single
pixel. The digits fill each row of the image left-to-right, then move downward
to the next row, filling rows top-to-bottom until every pixel of the image is
filled.

Each image actually consists of a series of identically-sized layers that are
filled in this way. So, the first digit corresponds to the top-left pixel of the
first layer, the second digit corresponds to the pixel to the right of that on
the same layer, and so on until the last digit, which corresponds to the
bottom-right pixel of the last layer.

For example, given an image 3 pixels wide and 2 pixels tall, the image data
123456789012 corresponds to the following image layers:

Layer 1: 123
         456

Layer 2: 789
         012
The image you received is 25 pixels wide and 6 pixels tall.

To make sure the image wasn't corrupted during transmission, the Elves would like
you to find the layer that contains the fewest 0 digits. On that layer, what is
the number of 1 digits multiplied by the number of 2 digits?

PART 2
========

"""

from typing import List
import numpy as np

def make_image_layers(raw_data: List[int], w: int, h: int) -> 'np.ndarray':
    return np.reshape(np.asarray(raw_data), (len(raw_data)//(w*h), h, w))

def get_part1(input_image: 'np.ndarray') -> int:
    # Get the zero-count per layer
    zero_counts_by_layer = np.count_nonzero(image == 0, axis=(1,2))
    # Get the minimum amount of zeros
    min_zeros = np.amin(zero_counts_by_layer)
    # Get the index of the layer with the minimum amount of zeros
    layer = np.where(zero_counts_by_layer == min_zeros)[0][0]
    # Get the layer with the minimum amount of zeros
    min_zeros_layer = image[layer,:,:]
    # Get the count of ones in the layer with the min zeros
    ones = np.count_nonzero(min_zeros_layer == 1)
    # Get the count of twos in the layer with the min zeros
    twos = np.count_nonzero(min_zeros_layer == 2)
    
    return ones * twos

def get_final_image(input_image: 'np.ndarray') -> 'np.ndarray':
    raw = []
    
    layers, height, width = input_image.shape
    
    for h in range(height):
        for w in range(width):
            for l in range(layers):
                pixel = image[l, h, w]
                if pixel == 2:
                    continue
                else:
                    raw.append(pixel)
                    break
    
    return np.reshape(np.asarray(raw), (height, width))

def render_image(input_image: 'np.ndarray') -> None:
    height, width = input_image.shape
    
    for h in range(height):
        line = ''
        for w in range(width):
            if input_image[h][w] == 1:
                line += '#'
            else:
                line += ' '
        print(f'{line}')

if __name__ == '__main__':
    with open ('day08_input.txt', 'r') as inp:
        raw_pixels = [int(p) for p in inp.read().strip()]

    IMAGE_WIDTH = 25
    IMAGE_HEIGHT = 6

    image = make_image_layers(raw_pixels.copy(), IMAGE_WIDTH, IMAGE_HEIGHT)
    
    # Part 1
    print(f'Part 1 Output: {get_part1(image)}')
    
    # Part 2
    final_image = get_final_image(image)
    print(f'Part 2 Output: \n')
    render_image(final_image)