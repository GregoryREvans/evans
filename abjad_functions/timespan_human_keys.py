def to_digit(string):
    return int(string) if string.isdigit() else string


def human_sorted_keys(pair):
    key, timespan = pair
    values = [to_digit(_) for _ in key.split()]
    hashable_key = tuple(values)
    return hashable_key
