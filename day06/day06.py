#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2021
Day 6

Created on 2021-12-07T01:03:01.416524

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
        from ..helpers import get_input, ints
    else:
        from helpers import get_input, ints

    data = ints(get_input())

    return data

# %% Part 1


def nextDay(fishDict):
    updated = {x: 0 for x in range(9)}
    newFish = 0
    for day, count in fishDict.items():
        if day == 0:
            updated[6] += count
            newFish = count
        else:
            updated[day - 1] += count
    # Add new fish
    updated[8] += newFish
    return updated


def part1(data):
    # Don't simulate every fish. Instead, create dict with # of days as each key, num fish as values
    fish = {x: data.count(x) for x in range(9)}
    for day in range(80):
        fish = nextDay(fish)
    total = sum(fish.values())
    return total

# %% Part 2


def part2(data):
    fish = {x: data.count(x) for x in range(9)}
    for day in range(256):
        fish = nextDay(fish)
    total = sum(fish.values())
    return total


# %% Run all
if __name__ == "__main__":
    data = load_data()

    print(part1(data))
    print(part2(data))

# %%
