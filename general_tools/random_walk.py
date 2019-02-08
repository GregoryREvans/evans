from random import random
from random import seed
from evans.general_tools.reduce_mod import reduceMod

def randomWalk(random_seed, length, mapped_list):
    seed(random_seed)
    walk = []
    walk.append(-1 if random() < 0.5 else 1)
    for i in range(1, length):
        movement = -1 if random() < 0.5 else 1
        value = walk[i-1] + movement
        walk.append(value)
    input_list = mapped_list
    l = len(input_list)
    final_list = [input_list[x] for x in reduceMod(l, walk)]
    return final_list
