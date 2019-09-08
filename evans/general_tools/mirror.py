def mirror(lst, sequential_duplicates):
    if sequential_duplicates is False:
        return lst + lst[-2:0:-1]
    else:
        return lst + lst[::-1]
