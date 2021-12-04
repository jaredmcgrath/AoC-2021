#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2021
Day 4

Created on 2021-12-03T23:24:38.767525

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

    from helpers import get_input, get_input_lines, ints, floats

    data = get_input_lines()

    return data

# %% Part 1


def part1(data):
    from helpers import ints
    allNums = [int(x) for x in data[0].split(",")]
    data = "\n".join(data[2:])
    data = data.split("\n\n")
    boards = []
    rowSums = []
    colSums = []
    # Construct boards + row/column sums
    for boardStr in data:
        board = [list(ints(b)) for b in boardStr.split("\n")]
        boards.append(board)
        rowSums.append([0 for _ in range(5)])
        colSums.append([0 for _ in range(5)])
    for num in allNums:
        for iBoard in range(len(boards)):
            for row in range(5):
                try:
                    col = boards[iBoard][row].index(num)
                    rowSums[iBoard][row] += 1
                    colSums[iBoard][col] += 1
                    boards[iBoard][row][col] = 0
                    # If we found a winning board, return its score
                    if rowSums[iBoard][row] == 5 or colSums[iBoard][col] == 5:
                        total = 0
                        winnerBoard = boards[iBoard]
                        for row in range(5):
                            for col in range(5):
                                total += winnerBoard[row][col]
                        return total * num
                    break
                except ValueError:
                    continue

# %% Part 2


def part2(data):
    from helpers import ints
    allNums = [int(x) for x in data[0].split(",")]
    data = "\n".join(data[2:])
    data = data.split("\n\n")
    boards = []
    rowSums = []
    colSums = []
    # Construct boards + row/column sums
    for boardStr in data:
        board = [list(ints(b)) for b in boardStr.split("\n")]
        boards.append(board)
        rowSums.append([0 for _ in range(5)])
        colSums.append([0 for _ in range(5)])

    remain = list(range(len(boards)))
    won = []
    for num in allNums:
        for iBoard in remain:
            for row in range(5):
                try:
                    col = boards[iBoard][row].index(num)
                    rowSums[iBoard][row] += 1
                    colSums[iBoard][col] += 1
                    boards[iBoard][row][col] = -1
                    # If we found a winning board, keep track of it
                    if rowSums[iBoard][row] == 5 or colSums[iBoard][col] == 5:
                        won.append(iBoard)
                    break
                except ValueError:
                    continue
        remain = list(filter(lambda x: not (x in won), remain))
        # If all boards have been won, stop checking numbers
        if len(won) == len(boards):
            break
    # Calculate score of losing board
    loser = won[-1]
    loserBoard = boards[loser]
    total = 0
    for row in range(5):
        for col in range(5):
            total += 0 if loserBoard[row][col] == -1 else loserBoard[row][col]
    return total * num


# %% Run all
if __name__ == "__main__":
    data = load_data()

    print(part1(data))
    print(part2(data))

# %%
