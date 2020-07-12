import abjad


def nested_list_to_rtm(nested_list):
    """
    >>> nested_list = [1, 1, [1, [1, 1]], 1]
    >>> print(evans.nested_list_to_rtm(nested_list))
    (1 1 (1 (1 1)) 1)

    """
    out_string = ""
    for item in str(nested_list):
        if item == "[":
            out_string += "("
        if item == "]":
            out_string += ")"
        if str.isdigit(item):
            out_string += item
        if item == "-":
            out_string += item
        if item == " ":
            out_string += item
    return out_string


def rotate_tree(rtm_string, n=1):
    """
    >>> rtm = '(1 (2 1 (1 2) 1))'
    >>> for x in range(6):
    ...     new_rtm = evans.rotate_tree(rtm, x)
    ...     print(new_rtm)
    ...
    (1 (2 1 (1 2) 1))
    (1 (1 1 (2 1) 2))
    (1 (1 2 (1 2) 1))
    (1 (2 1 (2 1) 1))
    (1 (1 2 (1 1) 2))
    (1 (2 1 (1 2) 1))

    """
    opening = rtm_string[:3]
    middle = rtm_string[3:-1]
    closing = rtm_string[-1]
    digits = [_ for _ in middle if str.isdigit(_)]
    digits = (_ for _ in digits[n:] + digits[:n])
    new_middle = ""
    for item in middle:
        if str.isdigit(item):
            new_middle += next(digits)
            continue
        new_middle += item
    return opening + new_middle + closing


def funnel_tree_to_x(rtm, x):
    list_out = [rtm]
    out = rtm
    digits = [int(_) for _ in out if _.isdigit()]
    if x < max(digits):
        for _ in range(abs(x - max(digits))):
            if not all(digit == x for digit in digits):
                new_out = ""
                for i, _ in enumerate(out):
                    if _.isdigit():
                        if int(_) == x:
                            new_out = new_out + _
                        elif int(_) > x:
                            new_out = new_out + f"{int(_) - 1}"
                        else:
                            new_out = new_out + f"{int(_) + 1}"
                    else:
                        new_out = new_out + _
                    out = new_out
                digits = [int(_) for _ in out if _.isdigit()]
                list_out.append(out)
    else:
        for _ in range(abs(x - min(digits))):
            if not all(digit == x for digit in digits):
                new_out = ""
                for i, _ in enumerate(out):
                    if _.isdigit():
                        if int(_) == x:
                            new_out = new_out + _
                        elif int(_) > x:
                            new_out = new_out + f"{int(_) - 1}"
                        else:
                            new_out = new_out + f"{int(_) + 1}"
                    else:
                        new_out = new_out + _
                    out = new_out
                digits = [int(_) for _ in out if _.isdigit()]
                list_out.append(out)
    return list_out


def funnel_inner_tree_to_x(rtm_string, x=1):
    """
    >>> rtm = '(1 (3 (2 (1 2 1 1)) 3))'
    >>> for x in evans.funnel_inner_tree_to_x(rtm_string=rtm, x=5):
    ...     print(x)
    ...
    (1 (3 (2 (1 2 1 1)) 3))
    (1 (4 (3 (2 3 2 2)) 4))
    (1 (5 (4 (3 4 3 3)) 5))
    (1 (5 (5 (4 5 4 4)) 5))
    (1 (5 (5 (5 5 5 5)) 5))

    """
    opening = rtm_string[:3]
    middle = rtm_string[3:-1]
    closing = rtm_string[-1]
    funnel_list = []
    for _ in funnel_tree_to_x(rtm=middle, x=x):
        funnel_list.append(opening + _ + closing)
    return funnel_list


class RTMMaker(object):
    r"""
    >>> rtm = ['(1 (1 1))', '(1 (1 1 1))', '(1 (1 1 1 1))']
    >>> maker = evans.RTMMaker(rtm=rtm)
    >>> divisions = [abjad.Duration(1, 1), abjad.Duration(1, 1), abjad.Duration(1, 1)]
    >>> selections = maker(divisions)
    >>> staff = abjad.Staff()
    >>> staff.extend(selections)
    >>> abjad.f(staff)
    \new Staff
    {
        c'2
        c'2
        \times 2/3 {
            c'2
            c'2
            c'2
        }
        c'4
        c'4
        c'4
        c'4
    }

    """

    def __init__(self, rtm, tie_across_divisions=False):
        self.rtm = abjad.CyclicTuple(rtm)
        self.tie_across_divisions = tie_across_divisions
        self.state = -1

    def __call__(self, divisions, previous_state=-1):
        starting_index = -1

        if previous_state is not None:
            starting_index = previous_state + 1

        selections = self._rtm_maker(divisions, starting_index=starting_index)

        if previous_state is not None:
            self.state += len(selections)
            self.state %= len(self.rtm)

        return selections

    @staticmethod
    def _rhythm_cell(duration, rtm):
        rtm_parser = abjad.rhythmtrees.RhythmTreeParser()
        selection = abjad.select(rtm_parser(rtm)[0](duration))
        return selection

    def _rtm_maker(self, divisions, starting_index=0):
        rtm = self.rtm[starting_index : starting_index + len(divisions)]

        selections = []
        for rtm_string, division in zip(rtm, divisions):
            selection = self._rhythm_cell(division, rtm_string)
            selections.append(selection)
        for selection_ in selections[:-1]:
            if self.tie_across_divisions is True:
                last_leaf = abjad.select(selection_).leaves()[-1]
                abjad.attach(abjad.Tie(), last_leaf)
        return selections
