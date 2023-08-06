# Gets value for dict key provided as list ordered list of keys
def get_dict_value(dictionary, keys):
    for key_index, key in enumerate(keys):
        if not key in dictionary.keys():
            return None
        if key_index == len(keys) - 1:
            return dictionary[key]
        dictionary = dictionary[key]

def update_dict(current, new):
    levels = [(current, new)]
    while len(levels) > 0:
        level = levels.pop(0)
        for level_key in level[1].keys():
            if not level_key in level[0].keys():
                level[0][level_key] = level[1][level_key]
            elif not type(level[1][level_key]) == dict:
                level[0][level_key] = level[1][level_key]
            elif not type(level[0][level_key]) == dict:
                level[0][level_key] = level[1][level_key]
            else:
                levels.append((level[0][level_key], level[1][level_key]))
    return current
