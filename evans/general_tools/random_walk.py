from random import random, seed

from evans.general_tools.cyc import cyc
from evans.general_tools.reduce_mod import reduce_mod


def random_walk(random_seed, length, step_list, mapped_list):
    seed(random_seed)
    if step_list is not None:
        step = cyc(step_list)
    walk = []
    walk.append(-1 if random() < 0.5 else 1)
    for i in range(1, length):
        if step_list is not None:
            next_step = next(step)
            movement = -next_step if random() < 0.5 else next_step
        else:
            movement = -1 if random() < 0.5 else 1
        value = walk[i - 1] + movement
        walk.append(value)
    input_list = mapped_list
    list_ = len(input_list)
    final_list = [input_list[0]]
    final_list.extend([input_list[x] for x in reduce_mod(list_, walk)])
    return final_list
