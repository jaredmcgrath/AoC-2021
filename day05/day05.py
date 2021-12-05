#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2021
Day 5

Created on 2021-12-05T12:25:59.281529

@author: jaredmcgrath
"""
# %% Data loading

import itertools


def find_path_to_helpers(target_folder="helpers", quiet=False):
    # Skip path finding if we successfully import the dummy file
    try:
        from helpers.dummy import dummy_func
        dummy_func()
        return
    except ImportError:
        not quiet and print("", "Couldn't find helpers directory!",
                            "Searching for path...", sep="\n")

    import os
    import sys
    # Figure out where this file is located so we can work backwards to find the target folder
    file_directory = os.path.dirname(os.path.abspath(__file__))
    path_check = []

    # Check parent directories to see if we hit the main project directory containing the target folder
    prev_working_path = working_path = file_directory
    while True:

        # If we find the target folder in the given directory, add it to the python path (if it's not already there)
        if target_folder in os.listdir(working_path):
            if working_path not in sys.path:
                tilde_swarm = "~"*(4 + len(working_path))
                not quiet and print("\n{}\nPython path updated:\n  {}\n{}".format(
                    tilde_swarm, working_path, tilde_swarm))
                sys.path.append(working_path)
            break

        # Stop if we hit the filesystem root directory (parent directory isn't changing)
        prev_working_path, working_path = working_path, os.path.dirname(
            working_path)
        path_check.append(prev_working_path)
        if prev_working_path == working_path:
            not quiet and print("\nTried paths:", *path_check, "", sep="\n  ")
            raise ImportError(
                "Can't find '{}' directory!".format(target_folder))


def load_data(quiet=True):
    find_path_to_helpers(quiet=quiet)
    if __package__:
        from ..helpers import get_input_lines
    else:
        from helpers import get_input_lines

    data = get_input_lines()

    return data

# %% Part 1


def dToTuple(d):
    return tuple(tuple(int(x) for x in p.split(",")) for p in d.split(" -> "))


def isVert(l): return l[0][0] == l[1][0]
def isHoriz(l): return l[0][1] == l[1][1]


def lineRange(line):
    if isVert(line):
        x = line[0][0]
        yMin = min(line[0][1], line[1][1])
        yMax = max(line[0][1], line[1][1])
        return ((x, y) for y in range(yMin, yMax + 1))
    elif isHoriz(line):
        y = line[0][1]
        xMin = min(line[0][0], line[1][0])
        xMax = max(line[0][0], line[1][0])
        return ((x, y) for x in range(xMin, xMax + 1))
    else:
        # Diagonal line
        pLeft = min(line, key=lambda x: x[0])
        pRight = max(line, key=lambda x: x[0])
        # Case 1: down-left
        if pLeft[1] < pRight[1]:
            # Start at top-left point
            x, y = pLeft
            delta = pRight[0] - pLeft[0]
            # x and y both increase
            return ((x + i, y + i) for i in range(delta + 1))
        # Case 2: up-right
        else:
            # Start at bottom-left point
            x, y = pLeft
            delta = pRight[0] - pLeft[0]
            # x increases, y decreases
            return ((x + i, y - i) for i in range(delta + 1))


def part1(data):
    lines = tuple(map(dToTuple, data))
    maxX = max(map(lambda l: max(l[0][0], l[1][0]), lines))
    maxY = max(map(lambda l: max(l[0][1], l[1][1]), lines))
    grid = [[0 for _ in range(maxX)] for _ in range(maxY)]
    for line in lines:
        if not (isHoriz(line) or isVert(line)):
            continue
        pts = lineRange(line)
        for x, y in pts:
            grid[y][x] += 1
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] >= 2:
                count += 1
    return count

# %% Part 2


def part2(data):
    lines = tuple(map(dToTuple, data))
    maxX = max(map(lambda l: max(l[0][0], l[1][0]), lines))
    maxY = max(map(lambda l: max(l[0][1], l[1][1]), lines))
    grid = [[0 for _ in range(maxX + 1)] for _ in range(maxY + 1)]
    for line in lines:
        pts = lineRange(line)
        for x, y in pts:
            grid[y][x] += 1
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] >= 2:
                count += 1
    return count


# %% Run all
if __name__ == "__main__":
    data = load_data()

    print(part1(data))
    print(part2(data))

# %%
