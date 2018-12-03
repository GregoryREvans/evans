from random import random
from random import seed

def reduceMod(x, rw):
    return [(y % x) for y in rw]

seed(1)
sopranino_random_walk = []
sopranino_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = sopranino_random_walk[i-1] + movement
    sopranino_random_walk.append(value)
sopranino_random_walk = [abs(x) for x in sopranino_random_walk]
sopranino_walk_chord = [8, 14, 23, 27, 28, 30, 37, 30, 28, 27, 23, 14, ]
l = len(sopranino_walk_chord)
sopranino_random_walk_notes = [sopranino_walk_chord[x] for x in reduceMod(l, sopranino_random_walk)]
print(sopranino_random_walk_notes)
