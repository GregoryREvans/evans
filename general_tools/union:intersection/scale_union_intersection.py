def scale(start, step, reps):
    list = [start, ]
    for _ in range(reps):
        new = [list[-1] + step]
        list.extend(new)
    return list

def intersect(a, b):
    intersection = list(set(a) & set(b))
    intersection = sorted(intersection)
    return intersection

def union(a, b):
    union = list(set(a) | set(b))
    union = sorted(union)
    return union

scale_1 = scale(-12, 1.5, 20)
scale_2 = scale(-12, 3.5, 20)
print('scales')
print(scale_1)
print(scale_2)
print(' ')
print('intersection')
print(intersect(scale_1, scale_2))
print(' ')
print('union')
print(union(scale_1, scale_2))
