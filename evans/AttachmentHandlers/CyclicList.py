class CyclicList:
    r"""
    >>> _cyc_count = -1
    >>> _non_cyc_count = -1
    >>> cyc_generator = CyclicList(lst=[1, 2, 3], continuous=True, count=_cyc_count)
    >>> non_cyc_generator = CyclicList(lst=[1, 2, 3], continuous=False, count=_non_cyc_count)

    >>> cyc_generator(r=2)
    [1, 2]

    >>> cyc_generator(r=7)
    [3, 1, 2, 3, 1, 2, 3]

    >>> non_cyc_generator(r=2)
    [1, 2]

    >>> non_cyc_generator(r=7)
    [1, 2, 3, 1, 2, 3, 1]

    >>> print((cyc_generator.state(), non_cyc_generator.state()))
    (8, 6)

    """

    def __init__(self, lst=None, continuous=False, count=-1):
        self.lst = lst
        self.continuous = continuous
        self.count = count

    def state_cyc(self, lst, r):
        returned_material = []
        for x in range(r):
            self.count += 1
            returned_material.append(lst[self.count % len(lst)])
        return returned_material

    def non_state_cyc(self, lst, r):
        returned_material = []
        self.count = -1
        for x in range(r):
            self.count += 1
            returned_material.append(lst[self.count % len(lst)])
        return returned_material

    def __call__(self, r):
        if self.continuous is True:
            return self.state_cyc(self.lst, r)
        else:
            return self.non_state_cyc(self.lst, r)

    def state(self):
        return self.count
