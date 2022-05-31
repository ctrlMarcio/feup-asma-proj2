from argparse import ArgumentError
import random

DIRECTIONS = [
    ("up", (0, 1)),
    ("down", (0, -1)),
    ("left", (-1, 0)),
    ("right", (1, 0))
]


def get_random_direction(exclude_directions=[]):
    if len(exclude_directions) == len(DIRECTIONS):
        raise ArgumentError("All directions are excluded")

    directions = DIRECTIONS.copy()
    directions = [
        direction for direction in directions if direction[0] not in exclude_directions]

    return random.choice(directions)


def scale_position(position, scale):
    return (position[0] * scale, position[1] * scale)


def add_to_position(position, increment):
    return (position[0] + increment[0], position[1] + increment[1])
