import itertools


def guerrero_morales(set, group_size):
    combination_sets = [_ for _ in itertools.combinations(set, group_size)]
    set_groups = []
    matrix = []
    for i, letter in enumerate(set[:group_size]):
        set_group = []
        for trio in combination_sets:
            if trio[0] is letter:
                set_group.append(trio)
        set_groups.append(set_group)

    return set_groups


###DEMO###
set_ = "ABCDEFG"
group_size_ = 3
net = guerrero_morales(set=set_, group_size=group_size_)
for _ in net:
    print(_)
