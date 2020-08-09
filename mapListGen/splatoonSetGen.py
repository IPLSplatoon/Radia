"""
Map generation created by .jpg and Radia. Final implementation assisted by Vincent Lee.
Lets hope it doesn't suck this time.

"""

import random
import discord
import discord.ext
from .errors import NotEnoughMapsException, InvalidInputException, InvalidFormatException


def build_map_pool(sz: str, tc: str, rm: str, cb: str):
    """
    Convert multiple strings into a useable list for the map generator.
    Returns a list if inputs are ok, otherwise, it'll return a string describing a problem.
    :param sz:
    :param tc:
    :param rm:
    :param cb:
    :return:
    """
    pool = [sz.split(','), tc.split(','), rm.split(','), cb.split(',')]

    for i in pool:
        if len(i) <= 6:
            raise NotEnoughMapsException("Needs to be 8 or more maps")

    return pool


def build_brackets_from_string(brackets: str):
    bracketList = brackets.split(",")
    returnList = []
    if (len(bracketList) % 2) != 0:
        raise ValueError
    bracketCount = 0
    bestOfCount = 1
    for x in range(int(len(bracketList) / 2)):
        returnList.append([int(bracketList[bracketCount]), int(bracketList[bestOfCount])])
        bracketCount += 2
        bestOfCount += 2
    return returnList


def build_brackets(brackets: list):
    """
    Convert a list of strings into a useable list for the map generator.
    Returns a list if inputs are ok, otherwise it'll return a string describing the problem.
    """
    if len(brackets) <= 0:
        raise InvalidInputException

    new_brackets = []
    for bracket in brackets:
        bracket_info = bracket.split(',')
        try:
            new_brackets.append((int(bracket_info[0]), int(bracket_info[1])))
        except ValueError:
            raise InvalidFormatException
    return new_brackets


def generate_maps(map_pool: list, brackets: list, seed: int) -> list:
    """
    map_pool: A 2d list of strings containing the maps. First list being for zones, then tc, rm, and cb. [[sz maps],[tc maps],[rm maps],[cb maps]]
    brackets: A 2d list containing data for each bracket to generate. [[rounds,best of], [""]]
    seed: Seed used for randomization

    returns: A 3d list containing bracket and map data formatted as such: [ bracket [ round [ game ] ] ]
    """
    modes = ["Splat Zones", "Tower Control", "Rainmaker", "Clam Blitz"]

    new_random = random.Random(seed)
    final_list, recent_modes = [], []
    recent_maps = [[], [], [], []]  # Store the recently used maps for each mode
    current_mode = new_random.choice(modes)

    for bracket in brackets:
        bracket_list = []

        for round in range(bracket[0]):
            round_recent_maps = []  # ensure the same map (even if its a different mode) does not appear within the same round
            round_list = []

            for game in range(bracket[1]):
                pool_index = modes.index(current_mode)
                
                while True:
                    try:
                        # choose a random map from a list containing maps in the pool minus the maps that have been used
                        current_map = new_random.choice(
                            list(set(map_pool[pool_index]) - set(recent_maps[pool_index]) - set(round_recent_maps)))
                    except IndexError:
                        # if no maps are available, remove the oldest element from the recently used maps and try again
                        del recent_maps[pool_index][len(recent_maps[pool_index]) - 1:]
                        continue
                    break

                recent_maps[pool_index].insert(0, current_map)
                round_recent_maps.insert(0, current_map)
                recent_modes.insert(0, current_mode)
                round_list.append((current_map, current_mode))

                del recent_modes[3:]  # delete the oldest element from the recently used modes
                current_mode = new_random.choice(list(set(modes) - set(
                    recent_modes)))  # choose a mode by taking a list of all modes minus recently used modes.

            bracket_list.append(round_list)

        recent_modes = []
        final_list.append(bracket_list)

    return final_list


def generate_mapsV2(map_pool: list, brackets: list, seed: int) -> list:
    modes = ["Splat Zones", "Tower Control", "Rainmaker", "Clam Blitz"]
    new_random = random.Random(seed)
    final_list, recent_modes = [], []
    recent_maps = [[], [], [], []]
    last_maps = []
    for bracket in brackets:
        bracket_list = []  # Stores the sets for each bracket.
        for SET in range(bracket[0]):
            set_maps = []  # ensure the same map (even if its a different mode) does not appear within the same round
            set_list = []  # Holds the map/modes for a set
            for game in range(bracket[1]):  # For the number of games in a set
                if len(recent_modes) == 4:  # if the recent_mode is 4, aka all modes gone through
                    recent_modes = []  # we reset the list
                # Get the mode and it's index number
                game_mode = new_random.choice(list(set(modes) - set(recent_modes)))
                game_mode_no = modes.index(game_mode)
                game_map = None
                while game_map is None:
                    # If the maps in the recent_maps of the mode is at the count, reset it to zero
                    if len(recent_maps[game_mode_no]) == len(map_pool[game_mode_no]):
                        recent_maps[game_mode_no] = []
                    # Get the map list valid for this mode @ this time
                    game_map_list = list(set(map_pool[game_mode_no]) - set(recent_maps[game_mode_no]))
                    # Choose a random map from the list of maps for a mode
                    map_choice = new_random.choice(game_map_list)
                    # while/if the map_choice is in set_maps, we keep choosing one till we get one that isn't
                    while map_choice in set_maps or map_choice in last_maps:
                        map_choice = new_random.choice(game_map_list)
                    game_map = map_choice  # Assign to get out of while loop
                set_list.append((game_map, game_mode))
                set_maps.append(game_map)
                recent_modes.append(game_mode)
            bracket_list.append(set_list)
            last_maps = set_maps
        recent_modes = []
        final_list.append(bracket_list)
    return final_list


def get_map_list_dict(map_list: list) -> dict:
    map_dict = {}
    for brackets in map_list:
        bracketHold = []
        for rounds in brackets:
            roundHold = []
            for games in rounds:
                roundHold.append({
                    "map": games[0].strip(),
                    "mode": games[1].strip()
                })
            bracketHold.append(roundHold)
        map_dict["{}".format(map_list.index(brackets))] = bracketHold
    return map_dict


def get_map_list_embed(map_list: list) -> discord.Embed:
    embed = discord.Embed(title='Maps')
    for bracket in map_list:
        field_title = "Bracket " + str(map_list.index(bracket) + 1)
        field_content = ''
        for round in bracket:
            field_content += "`Round " + str(bracket.index(round) + 1) + "`\n```"
            for game in round:
                field_content += str(round.index(game) + 1) + ":  " + game[1] + " on " + game[0].strip() + ".\n"
            field_content += "```\n"
        embed.add_field(name=field_title, value=field_content, inline=False)
    return embed
