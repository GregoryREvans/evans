import abjad


def select_measures(
    index_list, leaf=None, leaves=None, logical_ties=None, note=None, notes=None
):
    if leaf is not None:

        def selector(selections):
            sel_1 = abjad.select.leaves(selections)
            sel_2 = abjad.select.group_by_measure(sel_1)
            sel_3 = abjad.select.get(sel_2, index_list)
            sel_4 = abjad.select.leaf(sel_3, leaf)
            return sel_4

        return selector
    elif isinstance(leaves, list):

        def selector(selections):
            sel_1 = abjad.select.leaves(selections)
            sel_2 = abjad.select.group_by_measure(sel_1)
            sel_3 = abjad.select.get(sel_2, index_list)
            sel_4 = abjad.select.leaves(sel_3)
            sel_5 = abjad.select.get(sel_4, leaves)
            return sel_5

        return selector
    elif leaves is True:

        def selector(selections):
            sel_1 = abjad.select.leaves(selections)
            sel_2 = abjad.select.group_by_measure(sel_1)
            sel_3 = abjad.select.get(sel_2, index_list)
            sel_4 = abjad.select.leaves(sel_3)
            return sel_4

        return selector
    elif logical_ties is True:

        def selector(selections):
            sel_1 = abjad.select.leaves(selections)
            sel_2 = abjad.select.group_by_measure(sel_1)
            sel_3 = abjad.select.get(sel_2, index_list)
            sel_4 = abjad.select.logical_ties(sel_3)
            return sel_4

        return selector
    elif note is not None:

        def selector(selections):
            sel_1 = abjad.select.leaves(selections)
            sel_2 = abjad.select.group_by_measure(sel_1)
            sel_3 = abjad.select.get(sel_2, index_list)
            sel_4 = abjad.select.note(sel_3, note)
            return sel_4

        return selector
    elif notes is True:

        def selector(selections):
            sel_1 = abjad.select.leaves(selections)
            sel_2 = abjad.select.group_by_measure(sel_1)
            sel_3 = abjad.select.get(sel_2, index_list)
            sel_4 = abjad.select.notes(sel_3)
            return sel_4

        return selector
    else:

        def selector(selections):
            sel_1 = abjad.select.leaves(selections)
            sel_2 = abjad.select.group_by_measure(sel_1)
            sel_3 = abjad.select.get(sel_2, index_list)
            return sel_3

        return selector


def select_all_first_leaves(selections):
    runs = abjad.select.runs(selections)
    run_ties = abjad.select.logical_ties(runs, pitched=True)
    ties_first_leaves = [_[0] for _ in run_ties]
    return ties_first_leaves


def select_runs_first_leaves(selections):
    runs = abjad.select.runs(selections)
    first_ties = [abjad.select.logical_tie(run, 0) for run in runs]
    first_leaves = [abjad.select.leaf(tie, 0) for tie in first_ties]
    return first_leaves


def select_untupleted_leaves(argument):
    result = [_ for _ in argument if not isinstance(_, abjad.Tuplet)]
    return result


def select_outer_ties(argument):
    sel_1 = abjad.select.logical_ties(argument)
    sel_2 = abjad.select.get(sel_1, [0, -1])
    return sel_2


def select_ties_final_leaves(argument):
    sel_1 = abjad.select.logical_ties(argument)[:-1]
    result = [abjad.select.leaf(_, -1) for _ in sel_1]
    return result


def select_divisions_final_leaves(argument):
    sel_1 = abjad.select.tuplets(argument)[:-1]
    result = [abjad.select.leaf(_, -1) for _ in sel_1]
    return result


def select_alternate_divisions_final_leaves(argument, start=0):
    sel_1 = abjad.select.tuplets(argument)
    sel_2 = abjad.select.get(sel_1, [start], 2)
    result = [abjad.select.leaf(_, -1) for _ in sel_2]
    return result


def select_alternate_leaves(argument, start=0):
    sel_1 = abjad.select.logical_ties(argument)
    sel_2 = abjad.select.get(sel_1, [start], 2)
    return sel_2


def select_periodic_tuplets(argument, indices, period):
    sel_1 = abjad.select.tuplets(argument)
    sel_2 = abjad.select.get(sel_1, indices, period)
    return sel_2


def select_periodic_ties(argument, indices, period):
    sel_1 = abjad.select.logical_ties(argument)
    sel_2 = abjad.select.get(sel_1, indices, period)
    return sel_2


def select_all_but_final_leaf(argument):
    sel_1 = abjad.select.logical_ties(argument)
    result = [_[-1] for _ in sel_1]
    sel_2 = abjad.select.leaves(result)
    sel_3 = abjad.select.exclude(sel_2, [-1])
    return sel_3


def get_top_level_components_from_leaves(leaves):  # TODO:
    out = []
    for leaf in leaves:
        parent = abjad.get.parentage(leaf).parent
        if isinstance(parent, (abjad.Voice, abjad.Staff)):
            if leaf not in out:
                out.append(leaf)
        else:
            sub_out = get_top_level_components_from_leaves([parent])
            for sub_leaf in sub_out:
                if sub_leaf not in out:
                    out.append(sub_leaf)
    return out
