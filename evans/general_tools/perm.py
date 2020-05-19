def perm(lst):
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return [lst]
    else:
        list_ = []
        for i in range(len(lst)):
            x = lst[i]
            ba = lst[:i] + lst[i + 1 :]
            for p in perm(ba):
                list_.append([x] + p)
        return list_
