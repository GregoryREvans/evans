import itertools


def set_net(set, group_size, filter_depth):
    r"""
    >>> filter_depth_ = 7
    >>> set_ = "ABCDEFG"
    >>> group_size_ = 3
    >>> net = evans.set_net(set=set_, group_size=group_size_, filter_depth=filter_depth_)
    >>> print(net)
    [('A', 'B', 'C'), ('A', 'D', 'E'), ('A', 'F', 'G'), ('B', 'D', 'F'), ('B', 'E', 'G'), ('C', 'D', 'G'), ('C', 'E', 'F')]

    >>> filter_depth_ = 3
    >>> set_ = "ABCDEFGHI"
    >>> group_size_ = 4
    >>> net = evans.set_net(set=set_, group_size=group_size_, filter_depth=filter_depth_)
    >>> print(net)
    [('A', 'B', 'C', 'D'), ('A', 'E', 'F', 'G'), ('B', 'E', 'H', 'I')]

    >>> filter_depth_ = 2
    >>> set_ = "ABCDE"
    >>> group_size_ = 3
    >>> net = evans.set_net(set=set_, group_size=group_size_, filter_depth=filter_depth_)
    >>> print(net)
    [('A', 'B', 'C'), ('A', 'D', 'E')]

    """

    combination_sets = [_ for _ in itertools.combinations(set, group_size)]
    for i, letter in enumerate(range(filter_depth)):
        reference_set = combination_sets[i]
        for index, item in enumerate(reference_set):
            for set_class in combination_sets[i + 1 :]:
                if item in set_class:
                    checkable_set = [_ for _ in reference_set]
                    checkable_set.remove(item)
                    for check in checkable_set:
                        if set_class in combination_sets:
                            if check in set_class:
                                combination_sets.remove(set_class)
                            else:
                                continue
                        else:
                            continue
                else:
                    continue
    return combination_sets
