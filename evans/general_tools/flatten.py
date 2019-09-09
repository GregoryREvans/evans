def flatten(lst):
    out = []
    for i in lst:
        if isinstance(i, int):
            out.append(i)
        else:
            out.extend(flatten(i))
    return out
