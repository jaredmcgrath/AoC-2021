#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2021
Day 9

Created on 2021-12-08T23:13:42.056916

@author: jaredmcgrath
"""
# %% Data loading


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
        from ..helpers import get_input_lines, ints
    else:
        from helpers import get_input_lines, ints

    data = [[int(y) for y in x] for x in get_input_lines()]

    return data

# %% Part 1


def isMin(x, vals):
    return x < min(vals)


def part1(data):
    h = len(data)
    w = len(data[0])
    lows = []
    for i in range(h):
        for j in range(w):
            adjs = []
            if i != 0:
                adjs.append(data[i-1][j])
            if i != h - 1:
                adjs.append(data[i+1][j])
            if j != 0:
                adjs.append(data[i][j-1])
            if j != w - 1:
                adjs.append(data[i][j+1])
            if isMin(data[i][j], adjs):
                lows.append(data[i][j])
    total = sum([x + 1 for x in lows])
    return total

# %% Part 2


# This was recursive, until I hit the maximum recursion depth. oops
def non9AdjCount(data, i0, j0):
    pts = 0
    toExplore = [(i0, j0)]
    used = [[0 for _ in range(len(data[0]))] for _ in range(len(data))]
    used[i0][j0] = 1
    while len(toExplore):
        i, j = toExplore.pop()

        if i != 0 and (not used[i-1][j]) and data[i-1][j] != 9:
            used[i-1][j] = 1
            pts += 1
            toExplore.append((i-1, j))
        if i != len(data) - 1 and (not used[i+1][j]) and data[i+1][j] != 9:
            used[i+1][j] = 1
            pts += 1
            toExplore.append((i+1, j))
        if j != 0 and (not used[i][j-1]) and data[i][j-1] != 9:
            used[i][j-1] = 1
            pts += 1
            toExplore.append((i, j-1))
        if j != len(data[0]) - 1 and (not used[i][j+1]) and data[i][j+1] != 9:
            used[i][j+1] = 1
            pts += 1
            toExplore.append((i, j+1))

    return pts


def makeBasins(data, lows):
    basins = []
    for start in lows:
        _, iStart, jStart = start
        count = 1 + non9AdjCount(data, iStart, jStart)
        basins.append(count)
    return basins


def part2(data):
    h = len(data)
    w = len(data[0])
    lows = []
    for i in range(h):
        for j in range(w):
            adjs = []
            if i != 0:
                adjs.append(data[i-1][j])
            if i != h - 1:
                adjs.append(data[i+1][j])
            if j != 0:
                adjs.append(data[i][j-1])
            if j != w - 1:
                adjs.append(data[i][j+1])
            if isMin(data[i][j], adjs):
                lows.append((data[i][j], i, j))
    basins = makeBasins(data, lows)
    basins.sort(reverse=True)
    top3 = basins[:3]
    total = top3[0] * top3[1] * top3[2]
    return total


# %% Run all
if __name__ == "__main__":
    data = load_data()

    print(part1(data))
    print(part2(data))

# %%
