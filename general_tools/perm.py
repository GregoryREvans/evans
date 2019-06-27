def perm(lst):
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return [lst]
    else:
        l = []
        for i in range(len(lst)):
            x = lst[i]
            ba = lst[:i] + lst[i + 1 :]
            for p in perm(ba):
                l.append([x] + p)
        return l
