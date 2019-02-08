def flatten(lst):
    out = []
    for i in lst:
        for x in i:
            out.extend([x])
    return out
