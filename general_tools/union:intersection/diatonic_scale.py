#according to Xenakis
def scale(start, step, reps):
    list = [start, ]
    for _ in range(reps):
        new = [list[-1] + step]
        list.extend(new)
    return list

def intersect(a, b):
    intersect = list(set(a) & set(b))
    intersect = sorted(intersect)
    return intersect

def union(a, b):
    union = list(set(a) | set(b))
    union = sorted(union)
    return union

base = scale(0, 1, 12)
def complement(collection, scale):
    second = set(scale)
    return [item for item in collection if item not in scale]

scale_1 = scale(0, 3, 4)
complement_1 = complement(base, scale_1)
scale_2 = scale(1, 4, 4)
scale_9 = intersect(complement_1, scale_2)

scale_3 = scale(2, 3, 4)
complement_2 = complement(base, scale_3)
scale_4 = scale(2, 4, 4)
scale_10 = intersect(complement_2, scale_4)

scale_5 = scale(0, 3, 4)
scale_6 = scale(3, 4, 4)
scale_11 = intersect(scale_5, scale_6)

scale_7 = scale(1, 3, 4)
complement_3 = complement(base, scale_7)
scale_8 = scale(0, 4, 4)
scale_12 = intersect(complement_3, scale_8)

union_1 = union(scale_9, scale_10)
union_2 = union(scale_11,  scale_12)

diatonic_scale = union(union_1, union_2)

print('scales')
print(scale_1)
print(scale_2)
print(scale_3)
print(scale_4)
print(scale_5)
print(scale_6)
print(scale_7)
print(scale_8)
print(' ')
print('intersections')
print(scale_9)
print(scale_10)
print(scale_11)
print(scale_12)
print(' ')
print('union')
print(union_1)
print(union_2)
print(' ')
print('final scale')
print(diatonic_scale)
#seems wrong
