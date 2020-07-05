"""
Low Ink Set Generator

Initial Design and Implementation by .jpg
Integrated by Vincent Lee
"""
import random

all_modes = ['Splat Zones', 'Tower Control', 'Rainmaker', 'Clam Blitz']


def get_bias_list(inputList: list, bias, modes=all_modes) -> list:
    if modes is None:
        modes = all_modes
    l_copy = inputList.copy()
    random.shuffle(l_copy)
    if type(bias) == str:
        l_copy.remove(bias)
    elif type(bias) == int:
        l_copy.remove(modes[bias])
    return l_copy


def generate_swiss(bestOf: int, rounds: int, maps: list, modes: list = all_modes) -> list:
    """
    Since swiss is play all 3, I implemented an algorithm inspired by the modern Tetris piece algorithm.
    All maps will appear once in a random order, once they've all appeared once, then it'll repeat the process.
    Since its play all 3, with 4 modes to choose from, whatever mode didn't appear in a round will always appear in the
    next round.

    Parameters
    NumOfGames: int
        The number of games per round
    rounds: int
        The number of rounds in this swiss bracket
    maps: list
        The list of maps that can appear in this bracket
    modes: list
        The list of modes that can appear in this bracket
    """

    mode_bias_index = random.randint(0, 3)
    map_bias, map_index = random.choice(maps), 0

    current_maps = get_bias_list(maps, map_bias).copy()

    swissReturn = []

    for gameNum in range(rounds):

        roundSet = ""

        round_modes = get_bias_list(modes, mode_bias_index).copy()
        mode_bias_index += 1
        if mode_bias_index >= len(modes):
            mode_bias_index = 0

        for game in range(bestOf):
            roundSet += "{}: {} on {}\n".format(str(game + 1), round_modes[game], current_maps[map_index])

            map_index += 1
            if map_index >= len(current_maps):
                map_index = 0
                map_bias = current_maps[-1]
                current_maps = get_bias_list(maps, map_bias).copy()

        swissReturn.append(roundSet)
    return swissReturn


def generate_top_cut(rounds: int, best_of: int, maps: list, modes: list = all_modes) -> list:
    """
    Each round will randomly choose individual maps from the map list to ensure repeats don't occur.
    For each round, the mode is selected randomly for the first game. The following games will follow a set
    mode order (SZ -> TC -> RM -> CB). The next round shouldn't share the first mode with the last round.

    Parameters
    info: str
        String will be placed at the start of the returned string. Intended for bracket titles and rules.
    rounds: int
        The number of rounds in this swiss bracket
    best_of: int
        The number of games in a round
    maps: list
        The list of maps that can appear in this bracket
    modes: list
        The list of modes that can appear in this bracket
    """

    map_bias, map_index = random.choice(maps), 0
    mode_bias = -1

    topCutReturn = []

    for gameNum in range(rounds):
        current_maps = get_bias_list(maps, map_bias).copy()

        roundSet = ""

        mode_index = random.randint(0, 3)
        while mode_index == mode_bias:
            mode_index = random.randint(0, 3)
        first_mode_index = mode_index

        for game in range(best_of):
            roundSet += "{}: {} on {}\n".format(str(game + 1), modes[mode_index], current_maps[map_index])

            map_index += 1
            if map_index >= len(current_maps):
                map_index = 0
                map_bias = current_maps[-1]
                current_maps = get_bias_list(maps, map_bias).copy()

            mode_index += 1
            if mode_index >= len(modes):
                mode_index = 0

        mode_bias = first_mode_index
        topCutReturn.append(roundSet)

    return topCutReturn
