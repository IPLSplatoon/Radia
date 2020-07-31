#Map generation created by .jpg for IPL and Radia. Final implimention assisted by Vincent Lee.
#Lets hope it doesn't suck this time.

import random
import discord
import discord.ext

def build_map_pool(sz: str, tc: str, rm: str, cb: str):
    '''
    Convert multiple strings into a useable list for the map generator.
    Returns a list if inputs are ok, otherwise, it'll return a string describing a problem.
    '''
    pool = []
    pool.append(sz.split(','))
    pool.append(tc.split(','))
    pool.append(rm.split(','))
    pool.append(cb.split(','))

    for i in pool:
        if len(i) <= 6:
            return 'One or more of your map pools seems to contain a small amount of maps. Please add more maps and/or confirm that you are seperating each map with a comma.'

    return pool

def build_brackets(brackets:list):
    '''
    Convert a list of strings into a useable list for the map generator.
    Returns a list if inputs are ok, otherwise it'll return a string describing the problem.
    '''
    if len(brackets) <= 0:
        return 'There is no bracket data. Please add bracket data to generate a map list.'

    new_brackets = []
    for bracket in brackets:
        bracket_info = bracket.split(',')
        try:
            new_brackets.append((int(bracket_info[0]), int(bracket_info[1])))
        except ValueError:
            return 'One of the brackets could not interpret your input. Please confirm that you are entering bracket info correctly.'
    return new_brackets

def generate_maps(map_pool: list, brackets: list, seed: int) -> list:
    '''
    map_pool: A 2d list of strings containing the maps. First list being for zones, then tc, rm, and cb. [[sz maps],[tc maps],[rm maps],[cb maps]]
    brackets: A 2d list containing data for each bracket to generate. [[rounds,best of], [""]]
    seed: Seed used for randomization

    returns: A 3d list containing bracket and map data formatted as such: [ bracket [ round [ game ] ] ]
    '''
    modes = ("Splat Zones", "Tower Control", "Rainmaker", "Clam Blitz")

    new_random = random.Random(seed)
    final_list, recent_modes = [], []
    recent_maps = [ [],[],[],[] ] #Store the recently used maps for each mode
    current_mode = new_random.choice(modes)

    for bracket in brackets:
        bracket_list = []

        for round in range(bracket[0]):
            round_recent_maps = [] #ensure the same map (even if its a different mode) does not appear within the same round
            round_list = []
            pool_index = modes.index(current_mode)

            for game in range(bracket[1]):

                while True:
                    try:
                        #choose a random map from a list containing maps in the pool minus the maps that have been used
                        current_map = new_random.choice( list(set(map_pool[pool_index]) - set(recent_maps[pool_index]) - set(round_recent_maps)) )
                    except IndexError:
                        #if no maps are available, remove the oldest element from the recently used maps and try again
                        del recent_maps[pool_index][len(recent_maps[pool_index])-1:]
                        continue
                    break
                
                recent_maps[pool_index].insert(0, current_map)
                round_recent_maps.insert(0, current_map)
                recent_modes.insert(0, current_mode)
                round_list.append((current_map, current_mode))

                del recent_modes[3:] #delete the oldest element from the recently used modes
                current_mode = new_random.choice( list(set(modes) - set(recent_modes)) ) #choose a mode by taking a list of all modes minus recently used modes.

            bracket_list.append(round_list)
        
        recent_modes = []
        final_list.append(bracket_list)
    
    return final_list

def get_map_list_json(map_list: list) -> str:
    json = '{'
    for bracket in map_list:
        json += "\"Bracket " + str(map_list.index(bracket) + 1) + "\":{"

        for round in bracket:
            json += "\"Round " + str(bracket.index(round) + 1) + "\":["

            for game in round:
                json += "[\"{0}\", \"{1}\"]".format(game[0].strip(), game[1].strip())
                if round.index(game) < len(round)-1:
                    json += ","

            json += "]"
            if bracket.index(round) < len(bracket)-1:
                json += ","

        json += "}"
        if map_list.index(bracket) < len(map_list)-1:
            json += ","

    json += "}"
    return json

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