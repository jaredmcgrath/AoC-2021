#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2021
Day 3

Created on 2021-12-02T23:57:38.374552

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
        from ..helpers import get_input, ints, floats, get_input_lines
    else:
        from helpers import get_input, ints, floats, get_input_lines

    data = get_input_lines()

    return data

# %% Part 1


def part1(data):
    least = ""
    most = ""

    for pos in range(len(data[0])):
        val = ""
        for line in data:
            val += line[pos]
        if val.count("1") > val.count("0"):
            most += "1"
            least += "0"
        else:
            most += "0"
            least += "1"

    val1 = eval("0b"+most)
    val2 = eval("0b"+least)

    return val1 * val2

# %% Part 2


def part2(data):
    code1 = None
    code2 = None
    filtered_1 = data.copy()
    filtered_2 = data.copy()

    # for x in range
    for pos in range(len(data[0])):

        val1 = ""
        val2 = ""
        for line in filtered_1:
            val1 += line[pos]
        for line in filtered_2:
            val2 += line[pos]

        most_common1 = "1" if val1.count("1") > val1.count("0") else "0"
        least_common2 = "1" if val2.count("1") < val2.count("0") else "0"
        eq1 = val1.count("1") == val1.count("0")
        eq2 = val2.count("1") == val2.count("0")
        if eq1:
            filtered_1 = list(filter(lambda x: x[pos] == "1", filtered_1))
        else:
            filtered_1 = list(
                filter(lambda x: x[pos] == most_common1, filtered_1))

        if eq2:
            filtered_2 = list(filter(lambda x: x[pos] == "0", filtered_2))
        else:
            filtered_2 = list(
                filter(lambda x: x[pos] == least_common2, filtered_2))

        if len(filtered_1) == 1:
            code1 = filtered_1[0]
        if len(filtered_2) == 1:
            code2 = filtered_2[0]
        if code1 != None and code2 != None:
            break

    val1 = eval("0b"+code1)
    val2 = eval("0b"+code2)

    return val1 * val2


    # %% Run all
if __name__ == "__main__":
    data = load_data()

    print(part1(data))
    print(part2(data))

# %%
