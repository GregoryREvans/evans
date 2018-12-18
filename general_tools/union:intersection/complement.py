
def scale(start, step, reps):
    list = [start, ]
    for _ in range(reps):
        new = [list[-1] + step]
        list.extend(new)
    return list

base = scale(0, 1, 12)

def complement(collection, scale):
    second = set(scale)
    return [item for item in collection if item not in scale]

list = complement(base, [0, 3, 6])
print(list)
