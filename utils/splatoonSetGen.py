"""
Low Ink Set Generator

Initial Design and Implementation by .jpg
Integrated by Vincent Lee
"""
import random

all_modes = ['Splat Zones', 'Tower Control', 'Rainmaker', 'Clam Blitz']


async def get_bias_list(inputList: list, bias, modes=all_modes) -> list:
    if modes is None:
        modes = all_modes
    l_copy = inputList.copy()
    random.shuffle(l_copy)
    if type(bias) == str:
        l_copy.remove(bias)
    elif type(bias) == int:
        l_copy.remove(modes[bias])
    return l_copy


async def generate_swiss(info: str, rounds: int, maps: list, modes: list = all_modes) -> list:
    '''
    Since swiss is play all 3, I implimented an algorithm inspired by the modern tetris piece algorithm.
    All maps will appear once in a random order, once they've all appeared once, then it'll repeat the process.
    Since its play all 3, with 4 modes to choose from, whatever mode didn't appear in a round will always appear in the next round.

    Parameters
    info: str
        String will be placed at the start of the returned string. Intended for bracket titles and rules.
    rounds: int
        The number of rounds in this swiss bracket
    maps: list
        The list of maps that can appear in this bracket
    modes: list
        The list of modes that can appear in this bracket
    '''

    final_list = [info]

    mode_bias_index = random.randint(0, 3)
    map_bias, map_index = random.choice(maps), 0

    current_maps = (await get_bias_list(maps, map_bias)).copy()
    
    for round in range(rounds):
        round_str = "`Round " + str(round+1) + "`"

        round_modes = (await get_bias_list(modes, mode_bias_index)).copy()
        mode_bias_index += 1
        if mode_bias_index >= len(modes):
            mode_bias_index = 0

        for game in range(3):
            round_str += "\n" + str(game+1) + ": " + round_modes[game] + " on " + current_maps[map_index]

            map_index += 1
            if map_index >= len(current_maps):
                map_index = 0
                map_bias = current_maps[-1]
                current_maps = (await get_bias_list(maps, map_bias)).copy()

        final_list.append(round_str)

    return final_list


async def generate_top_cut(info: str, rounds: int, best_of: int, maps: list, modes: list = all_modes) -> list:
    '''
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
    '''

    final_list = [info]

    map_index = 0
    mode_bias = -1
    current_maps = (await get_bias_list(maps, random.choice(maps))).copy()

    for round in range(rounds):
        round_str = "`Round " + str(round+1) + "`"

        mode_index, mode_list  = 0, modes.copy()
        random.shuffle(mode_list)

        for game in range(best_of):
            round_str += "\n" + str(game+1) + ": " + mode_list[mode_index] + " on " + current_maps[map_index]

            map_index += 1
            if map_index >= len(current_maps):
                map_index = 0
                map_bias = current_maps[-1]
                current_maps = (await get_bias_list(maps, map_bias)).copy()

            mode_index += 1
            if mode_index >= len(mode_list):
                mode_index = 0
                mode_list = (await get_bias_list(modes, mode_list[-1])).copy()

        final_list.append(round_str)
    
    return final_list
