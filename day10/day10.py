#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2021
Day 10

Created on 2021-12-09T23:57:53.338574

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
        from ..helpers import get_input_lines
    else:
        from helpers import get_input_lines

    data = get_input_lines()

    return data

# %% Part 1


def part1(data):
    opens = ["(", "<", "{", "["]
    closes = [")", ">", "}", "]"]
    values = {")": 3, "]": 57, "}": 1197, ">": 25137}
    score = 0
    for line in data:
        chunks = []
        for c in line:
            if c in opens:
                chunks.append(c)
            else:
                top = chunks.pop()
                idx = closes.index(c)
                if top != opens[idx]:
                    score += values[c]
                    break

    return score

# %% Part 2


def part2(data):
    opens = ["(", "<", "{", "["]
    closes = [")", ">", "}", "]"]
    # Find all the non-corrupt lines
    nonCorrupt = []
    for line in data:
        chunks = []
        corrupt = False
        for c in line:
            # If it's an opening bracket
            if c in opens:
                chunks.append(c)
            # If it's a closing bracket
            else:
                top = chunks.pop()
                idx = closes.index(c)
                if top != opens[idx]:
                    corrupt = True
                    break
        if not corrupt:
            nonCorrupt.append(line)

    # Values of missing closing brackets
    values = {")": 1, "]": 2, "}": 3, ">": 4}
    scores = []
    for line in nonCorrupt:
        chunks = []
        for c in line:
            if c in opens:
                chunks.append(c)
            else:
                top = chunks.pop()
        score = 0
        # Add a new closing bracket for every non-closed bracket
        while len(chunks):
            openC = chunks.pop()
            idx = opens.index(openC)
            closeC = closes[idx]
            score *= 5
            score += values[closeC]
        if score:
            scores.append(score)

    scores.sort()
    return scores[len(scores) // 2]


# %% Run all
if __name__ == "__main__":
    data = load_data()

    print(part1(data))
    print(part2(data))

# %%
