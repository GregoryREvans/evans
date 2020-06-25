def scale(start, step, reps):
    list = [start]
    for _ in range(reps):
        new = [list[-1] + step]
        list.extend(new)
    return list


scale_1 = scale(0, 2, 5)
scale_2 = scale(-2, 1.5, 7)
print(scale_1)
print(scale_2)
