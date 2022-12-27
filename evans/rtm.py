"""
Rhythm tree functions.
"""
from fractions import Fraction

import abjad
from abjadext import rmakers

from .sequence import CyclicList, Sequence, flatten

# from abjadext import rmakers


def flatten_tree_level(rtm, recurse=False):
    r"""

    .. container:: example

        >>> string = "(1 (1 (1 ((2 (1 1 1)) 2 2 1))))"
        >>> rhythm_tree_container_ = evans.flatten_tree_level(
        ...     string,
        ...     recurse=False,
        ... )
        >>> strings = [string, rhythm_tree_container_]
        >>> durations = [abjad.Duration(1, 1), abjad.Duration(1, 1)]
        >>> h = evans.RhythmHandler(evans.RTMMaker(strings), forget=False)
        >>> selections = h(durations)
        >>> staff = abjad.Staff()
        >>> staff.extend(selections)
        >>> abjad.show(staff) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'2
                \times 4/7
                {
                    \times 2/3
                    {
                        c'8
                        c'8
                        c'8
                    }
                    c'4
                    c'4
                    c'8
                }
                c'8
                \times 2/3
                {
                    c'8
                    c'8
                    c'8
                }
                c'4
                c'4
                c'8
            }

    .. container:: example

        >>> string = "(1 (1 (1 ((2 (1 1 1)) 2 2 1))))"
        >>> rhythm_tree_container_ = evans.flatten_tree_level(
        ...     string,
        ...     recurse=True,
        ... )
        >>> strings = [string, rhythm_tree_container_]
        >>> durations = [abjad.Duration(1, 1), abjad.Duration(1, 1)]
        >>> h = evans.RhythmHandler(evans.RTMMaker(strings), forget=False)
        >>> selections = h(durations)
        >>> staff = abjad.Staff()
        >>> staff.extend(selections)
        >>> abjad.show(staff) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'2
                \times 4/7
                {
                    \times 2/3
                    {
                        c'8
                        c'8
                        c'8
                    }
                    c'4
                    c'4
                    c'8
                }
                \times 8/9
                {
                    c'8
                    c'8
                    c'8
                    c'8
                    c'4
                    c'4
                    c'8
                }
            }

    """
    parser = abjad.rhythmtrees.RhythmTreeParser()
    rhythm_tree_list = parser(rtm)
    rhythm_tree = rhythm_tree_list[0]
    out = []
    for item in rhythm_tree:
        if isinstance(item, abjad.rhythmtrees.RhythmTreeContainer):
            if recurse:
                temp = flatten_tree_level(item.rtm_format)
                temp_tree_list = parser(temp)
                temp_tree = temp_tree_list[0]
                for _ in temp_tree:
                    out.append(_)
            else:
                for item_ in item:
                    out.append(item_)
        else:
            out.append(item)
    out = abjad.rhythmtrees.RhythmTreeContainer(out)
    return out.rtm_format


def nested_list_to_rtm(nested_list):
    r"""

    ..  container:: example

        >>> nested_list = [1, [1, 1, [1, [1, 1]], 1]]
        >>> rtm_string = evans.nested_list_to_rtm(nested_list)
        >>> print(rtm_string)
        (1 (1 1 (1 (1 1)) 1))

        >>> rtm_list = [rtm_string]
        >>> maker = evans.RTMMaker(rtm=rtm_list)
        >>> divisions = [abjad.Duration(1, 1)]
        >>> selections = maker(divisions)
        >>> staff = abjad.Staff()
        >>> staff.extend(selections)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/abjad/scm/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'4
                c'4
                c'8
                c'8
                c'4
            }

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
    r"""

    ..  container:: example

        >>> rtm = "(1 (2 (1 (1 2)) 1))"
        >>> for x in range(6):
        ...     new_rtm = evans.rotate_tree(rtm, x)
        ...     print(new_rtm)
        ...
        (1 (2 (1 (1 2)) 1))
        (1 (1 (1 (2 1)) 2))
        (1 (1 (2 (1 2)) 1))
        (1 (2 (1 (2 1)) 1))
        (1 (1 (2 (1 1)) 2))
        (1 (2 (1 (1 2)) 1))

        >>> rtm_list = [evans.rotate_tree(rtm, x) for x in range(6)]
        >>> maker = evans.RTMMaker(rtm=rtm_list)
        >>> divisions = [abjad.Duration(1, 1) for _ in rtm_list]
        >>> selections = maker(divisions)
        >>> staff = abjad.Staff()
        >>> staff.extend(selections)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/abjad/scm/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'2
                \times 2/3 {
                    c'8
                    c'4
                }
                c'4
                c'4
                \times 2/3 {
                    c'4
                    c'8
                }
                c'2
                c'4
                \times 2/3 {
                    c'4
                    c'2
                }
                c'4
                c'2
                \times 2/3 {
                    c'4
                    c'8
                }
                c'4
                \times 4/5 {
                    c'4
                    c'4
                    c'4
                    c'2
                }
                c'2
                \times 2/3 {
                    c'8
                    c'4
                }
                c'4
            }

    >>> divisions = [
    ...     abjad.Duration(1, 2),
    ...     abjad.Duration(1, 4),
    ...     abjad.Duration(1, 4),
    ...     abjad.Duration(1, 1),
    ...     abjad.Duration(1, 4),
    ...     abjad.Duration(3, 4),
    ...     abjad.Duration(2, 1),
    ...     abjad.Duration(5, 8),
    ...     abjad.Duration(3, 8),
    ... ]
    >>> selections = maker(divisions)
    >>> staff = abjad.Staff()
    >>> staff.extend(selections)
    >>> score = abjad.Score([staff])
    >>> moment = "#(ly:make-moment 1 25)"
    >>> abjad.setting(score).proportional_notation_duration = moment
    >>> file = abjad.LilyPondFile(
    ...     items=[
    ...         "#(set-default-paper-size \"a4\" \'portrait)",
    ...         r"#(set-global-staff-size 16)",
    ...         "\\include \'Users/gregoryevans/abjad/abjad/scm/abjad.ily\'",
    ...         score,
    ...     ],
    ... )
    ...
    >>> abjad.show(file) # doctest: +SKIP

    .. docs::

        >>> print(abjad.lilypond(staff))
        \new Staff
        {
            c'4
            \times 2/3 {
                c'16
                c'8
            }
            c'8
            c'16
            \times 2/3 {
                c'16
                c'32
            }
            c'8
            c'16
            \times 2/3 {
                c'16
                c'8
            }
            c'16
            c'2
            \times 2/3 {
                c'4
                c'8
            }
            c'4
            \times 4/5 {
                c'16
                c'16
                c'16
                c'8
            }
            \tweak text #tuplet-number::calc-fraction-text
            \times 3/4 {
                c'2
                \times 2/3 {
                    c'8
                    c'4
                }
                c'4
            }
            c'1
            \times 2/3 {
                c'4
                c'2
            }
            c'2
            \tweak text #tuplet-number::calc-fraction-text
            \times 5/8 {
                c'4
                \times 2/3 {
                    c'4
                    c'8
                }
                c'2
            }
            \tweak text #tuplet-number::calc-fraction-text
            \times 3/4 {
                c'8
                \times 2/3 {
                    c'8
                    c'4
                }
                c'8
            }
        }

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
    r"""

    ..  container:: example

        >>> rtm = '(1 (3 (2 (1 2 1 1)) 3))'
        >>> for x in evans.funnel_inner_tree_to_x(rtm_string=rtm, x=5):
        ...     print(x)
        ...
        (1 (3 (2 (1 2 1 1)) 3))
        (1 (4 (3 (2 3 2 2)) 4))
        (1 (5 (4 (3 4 3 3)) 5))
        (1 (5 (5 (4 5 4 4)) 5))
        (1 (5 (5 (5 5 5 5)) 5))

        >>> rtm_list = evans.funnel_inner_tree_to_x(rtm_string=rtm, x=5)
        >>> maker = evans.RTMMaker(rtm=rtm_list)
        >>> divisions = [abjad.Duration(1, 1) for _ in rtm_list]
        >>> selections = maker(divisions)
        >>> staff = abjad.Staff()
        >>> staff.extend(selections)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/abjad/scm/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'4.
                \times 4/5 {
                    c'16
                    c'8
                    c'16
                    c'16
                }
                c'4.
                \times 8/11 {
                    c'2
                    \times 2/3 {
                        c'8
                        c'8.
                        c'8
                        c'8
                    }
                    c'2
                }
                \times 4/7 {
                    c'2
                    ~
                    c'8
                    \times 8/13 {
                        c'8.
                        c'4
                        c'8.
                        c'8.
                    }
                    c'2
                    ~
                    c'8
                }
                \times 8/15 {
                    c'2
                    ~
                    c'8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/17 {
                        c'4
                        c'4
                        ~
                        c'16
                        c'4
                        c'4
                    }
                    c'2
                    ~
                    c'8
                }
                \times 8/15 {
                    c'2
                    ~
                    c'8
                    c'8
                    ~
                    c'32
                    c'8
                    ~
                    c'32
                    c'8
                    ~
                    c'32
                    c'8
                    ~
                    c'32
                    c'2
                    ~
                    c'8
                }
            }

    ..  container:: example

            >>> rtm_list = evans.funnel_inner_tree_to_x(rtm_string="(1 ((4 (1 1 (2 (3 1)))) 1))", x=1)
            >>> maker = evans.RTMMaker(rtm=rtm_list)
            >>> divisions = [abjad.Duration(1, 1) for _ in rtm_list]
            >>> selections = maker(divisions)
            >>> staff = abjad.Staff()
            >>> staff.extend(selections)
            >>> score = abjad.Score([staff])
            >>> moment = "#(ly:make-moment 1 25)"
            >>> abjad.setting(score).proportional_notation_duration = moment
            >>> file = abjad.LilyPondFile(
            ...     items=[
            ...         "#(set-default-paper-size \"a4\" \'portrait)",
            ...         r"#(set-global-staff-size 16)",
            ...         "\\include \'Users/gregoryevans/abjad/abjad/scm/abjad.ily\'",
            ...         score,
            ...     ],
            ... )
            ...
            >>> abjad.show(file) # doctest: +SKIP

            ..  docs::

                >>> print(abjad.lilypond(staff))
                \new Staff
                {
                    \times 4/5 {
                        c'4
                        c'4
                        c'4.
                        c'8
                        c'4
                    }
                    c'4
                    c'4
                    \times 2/3 {
                        c'4
                        c'8
                    }
                    c'4
                    \times 2/3 {
                        \times 2/3 {
                            c'2
                            c'2
                            c'4
                            c'4
                        }
                        c'2
                    }
                    \times 2/3 {
                        c'4
                        c'4
                        c'8
                        c'8
                    }
                    c'2
                }

    """
    opening = rtm_string[:3]
    middle = rtm_string[3:-1]
    closing = rtm_string[-1]
    funnel_list = []
    for _ in funnel_tree_to_x(rtm=middle, x=x):
        funnel_list.append(opening + _ + closing)
    return funnel_list


# WAS: class RTMMaker(rmakers.RhythmMaker):
class RTMMaker:
    r"""

    .. container:: example

        >>> rtm = ['(1 (1 1))', '(1 (1 1 1))', '(1 (1 1 1 1))']
        >>> maker = evans.RTMMaker(rtm=rtm)
        >>> divisions = [abjad.Duration(1, 1), abjad.Duration(1, 1), abjad.Duration(1, 1)]
        >>> selections = maker(divisions)
        >>> staff = abjad.Staff()
        >>> staff.extend(selections)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/abjad/scm/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
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

    def __str__(self):
        return f"<{type(self).__name__}()>"

    def __repr__(self):
        return f"<{type(self).__name__}()>"

    def __call__(self, divisions, previous_state=-1, state=None):
        starting_index = -1

        if previous_state is not None:
            starting_index = previous_state + 1

        selections = self._rtm_maker(divisions, starting_index=starting_index)

        if previous_state is not None:
            self.state += len(selections)
            self.state %= len(self.rtm)
            state = self.state
        else:
            state = -1
        return flatten(selections)  # WARNING: was not previously flattened

    @staticmethod
    def _rhythm_cell(duration, rtm):
        rtm_parser = abjad.rhythmtrees.RhythmTreeParser()
        selection = rtm_parser(rtm)[0](
            duration
        )  # WARNING: was previously wrapped in selection
        return selection

    def _rtm_maker(self, divisions, starting_index=0):
        rtm = self.rtm[starting_index : starting_index + len(divisions)]

        selections = []
        for rtm_string, division in zip(rtm, divisions):
            selection = self._rhythm_cell(division, rtm_string)
            selections.append(selection)
        for selection_ in selections[:-1]:
            if self.tie_across_divisions is True:
                last_leaf = abjad.select.leaves(selection_)[-1]
                abjad.attach(abjad.Tie(), last_leaf)
        return selections

    # def state(self):
    #     return self.state


class RhythmTreeQuantizer:
    def __init__(self):
        pass

    def __call__(self, string):
        parsed_string = self._parse_tree(string)
        self._quantize_rhythm_tree(parsed_string)
        return parsed_string.rtm_format

    def _operation(self, nodes):
        numerators = []
        for node in nodes:
            numerators.append(node.preprolated_duration.numerator)
        numerators_sum = sum(numerators)
        if 4 < numerators_sum:
            normalized = Sequence(numerators).normalize_to_sum(4)
            new_numerators = [round(_) for _ in normalized if round(_) != 0]
            for numerator, node in zip(new_numerators, nodes):
                node.preprolated_duration = abjad.Duration(numerator, 1)

    def _parse_tree(self, string):
        parser = abjad.rhythmtrees.RhythmTreeParser()
        rhythm_tree_list = parser(string)
        rhythm_tree_container = rhythm_tree_list[0]
        return rhythm_tree_container

    def _recursive_operation(self, layers):
        temp = []
        for layer in layers:
            if isinstance(layer, list):
                self._recursive_operation(layer)
            else:
                temp.append(layer)
        self._operation(temp)

    def _return_layers(self, parsed_tree):
        layers = []
        for node in parsed_tree:
            if isinstance(node, abjad.rhythmtrees.RhythmTreeContainer):
                layers.append(node)
                layers.append(self._return_layers(node))
            else:
                layers.append(node)
        return layers

    def _quantize_rhythm_tree(self, rtm_container):
        layers = self._return_layers(rtm_container)
        self._recursive_operation(layers)


def helianthated_rtm(divisions, beats):
    s = Sequence(divisions).helianthate(-1, 1)
    s_ = Sequence(flatten(Sequence(beats).helianthate(-1, 1)))

    c_s_ = CyclicList(s_, forget=False)
    beats = c_s_(r=len(s))

    out_ = []

    for x, y in zip(beats, s):
        temp = [x, y]
        out_.append(temp)

    out = Sequence(out_).partition_by_counts(
        [len(divisions)], cyclic=True, overhang=True
    )

    final_out = []

    for rtm_list in out:
        final_temp = [1, rtm_list]
        final_out.append(final_temp)

    rtm_out = []

    for _ in final_out:
        rtm = nested_list_to_rtm(_)
        rtm_out.append(rtm)

    return rtm_out


def find_smallest(selections):
    leaves = abjad.select.leaves(selections)
    multipliers = [leaf.multiplier for leaf in leaves]
    minimum = min(multipliers)
    index = multipliers.index(minimum)
    return index


def find_largest(selections):
    multipliers = [leaf.multiplier for leaf in selections]
    maximum = max(multipliers)
    index = multipliers.index(maximum)
    return index


def variable_feather_beam(selections, number_of_extra_beams=1):
    leaves = abjad.select.leaves(selections)
    min_index = find_smallest(leaves)
    max_index = find_largest(leaves)
    if leaves[0].multiplier < leaves[-1].multiplier:
        literal = abjad.LilyPondLiteral(
            rf"\once \override Beam.grow-direction = #LEFT",
            site="before",
        )
    if leaves[-1].multiplier < leaves[0].multiplier:
        literal = abjad.LilyPondLiteral(
            rf"\once \override Beam.grow-direction = #RIGHT",
            site="before",
        )
    if 0 < min_index < (len(leaves) - 1):
        literal = abjad.LilyPondLiteral(
            rf"\once \override Beam.stencil = #(grow-beam-var {min_index} {number_of_extra_beams})",
            site="before",
        )
    if 0 < max_index < (len(leaves) - 1):
        literal = abjad.LilyPondLiteral(
            rf"\once \override Beam.stencil = #(grow-beam-var {0 - max_index} {number_of_extra_beams})",
            site="before",
        )
    first_leaf = leaves[0]
    abjad.attach(literal, first_leaf)
    abjad.beam(selections)


def return_interpolations(duration, divisions, direction, switch_index):
    integers = [_ + 1 for _ in range(divisions)]
    if direction is abjad.RIGHT:
        integers.reverse()
    if switch_index is not None:
        first_part = integers[: switch_index + 1]
        desired_continuation_length = len(integers[switch_index + 1 :])
        reference_integer = first_part[-1]
        if direction is abjad.LEFT:
            second_part = [reference_integer - 1]
        if direction is abjad.RIGHT:
            second_part = [reference_integer + 1]
        for i in range(desired_continuation_length - 1):
            if direction is abjad.LEFT:
                new_point = second_part[-1] - 1
            if direction is abjad.RIGHT:
                new_point = second_part[-1] + 1
            second_part.append(new_point)
        integers = first_part + second_part
        smallest_integer = min(integers)
        if smallest_integer < 1:
            difference = 1 - smallest_integer
            integers = [_ + difference for _ in integers]
        if 1 < smallest_integer:
            difference = smallest_integer - 1
            integers = [_ - difference for _ in integers]
    total = sum(integers)
    smallest_piece = duration / total
    sizes = [i * smallest_piece for i in integers]
    assert sum(sizes) == duration
    return sizes


def return_multipliers(interpolations, written_duration=Fraction(1, 8)):
    multipliers = [_ / written_duration for _ in interpolations]
    assert [_ * written_duration for _ in multipliers] == interpolations
    return multipliers


def make_exponential_leaves(
    total_duration,
    written_duration,
    number_of_divisions,
    direction=abjad.LEFT,
    switch_index=None,
):
    if isinstance(written_duration, Fraction):
        pass
    else:
        written_duration = Fraction(written_duration[0], written_duration[1])
    if isinstance(total_duration, Fraction):
        pass
    elif isinstance(total_duration, abjad.Duration):
        written_duration = Fraction(
            total_duration.numerator, written_duration.denominator
        )
    else:
        written_duration = Fraction(total_duration[0], written_duration[1])
    i = return_interpolations(
        total_duration,
        number_of_divisions,
        direction=direction,
        switch_index=switch_index,
    )
    m = return_multipliers(i, written_duration)
    tuplet = abjad.Tuplet(
        "1:1",
        [
            abjad.Note(
                "c'",
                abjad.Duration(
                    written_duration.numerator, written_duration.denominator
                ),
                multiplier=abjad.Multiplier(_),
            )
            for _ in m
        ],
    )
    assert abjad.get.duration(tuplet) == abjad.Duration(total_duration)
    rmakers.duration_bracket(tuplet)
    variable_feather_beam(tuplet)
    return [tuplet]


def exponential_leaf_maker(
    written_durations, numbers_of_attacks, directions, switch_indices
):
    written_durations = CyclicList(written_durations, forget=False)
    numbers_of_attacks = CyclicList(numbers_of_attacks, forget=False)
    directions = CyclicList(directions, forget=False)
    switch_indices = CyclicList(switch_indices, forget=False)

    def make_leaves(divisions, state=None, previous_state=None):
        out = []
        for division in divisions:
            tup = make_exponential_leaves(
                division,
                written_durations(r=1)[0],
                numbers_of_attacks(r=1)[0],
                directions(r=1)[0],
                switch_indices(r=1)[0],
            )
            out.extend(tup)
        return out

    return make_leaves


class BeforeGraceContainer(abjad.BeforeGraceContainer):
    def __init__(
        self,
        components=None,
        *,
        position=6,
        language="english",
        tag=None,
    ) -> None:
        if isinstance(components, str):
            new_str = "{" + components + "}"
            container = abjad.parse(new_str)
            components = abjad.mutate.eject_contents(container)
        component_count = len(components)
        if 1 < component_count:
            self._command = r"\appoggiatura"
            new_components = components
        else:
            temp = [abjad.Rest("r8")]
            new_components = temp + components
            abjad.attach(abjad.StartSlur(), new_components[-1])
            stop_slur_literal = abjad.LilyPondLiteral(r"<> )", site="after")
            abjad.attach(stop_slur_literal, new_components[-1])
            self._command = r"\acciaccatura"
        abjad.attach(abjad.StartBeam(), new_components[0])
        abjad.attach(abjad.StopBeam(), new_components[-1])
        abjad.override(
            new_components[0]
        ).Beam.positions = rf"#'({position} . {position})"
        self._main_leaf = None
        abjad.BeforeGraceContainer.__init__(
            self, new_components, command=self._command, language=language, tag=tag
        )


def before_grace_container(
    argument,
    counts,
    *,
    position=6,
):
    _do_grace_container_command(
        argument,
        counts=counts,
        class_=BeforeGraceContainer,
        talea=rmakers.Talea([1], 8),
        position=position,
    )


class AfterGraceContainer(abjad.AfterGraceContainer):
    def __init__(
        self,
        components=None,
        *,
        position=6,
        with_glissando=False,
        language="english",
        tag=None,
    ) -> None:
        if isinstance(components, str):
            new_str = "{" + components + "}"
            container = abjad.parse(new_str)
            components = abjad.mutate.eject_contents(container)
        component_count = len(components)
        # _main_leaf must be initialized before container initialization
        if 1 < component_count:
            if with_glissando is True:
                copy = abjad.mutate.copy(components[0])
                temp = [copy]
                new_components = temp + components
                abjad.attach(abjad.StartBeam(), new_components[1])
                start_literal = abjad.LilyPondLiteral(
                    r"\start-multi-grace", site="before"
                )
                abjad.attach(start_literal, new_components[0])
                start_literal_ = abjad.LilyPondLiteral(
                    r"\start-multi-grace", site="before"
                )
                abjad.attach(start_literal_, new_components[1])
                abjad.override(
                    new_components[1]
                ).Beam.positions = rf"#'({position} . {position})"
                abjad.override(new_components[0]).Flag.stencil = "##f"
                abjad.override(new_components[0]).Stem.stencil = rf"##f"
                abjad.override(new_components[0]).NoteHead.transparent = rf"##t"
                heads = []
                non_last_leaves = abjad.select.leaves(new_components)[:-1]
                for leaf in non_last_leaves:
                    if isinstance(leaf, abjad.Note):
                        heads.append(leaf.note_head)
                    elif isinstance(leaf, abjad.Chord):
                        heads.extend(leaf.note_heads)
                    for head in heads:
                        abjad.tweak(head, r"\tweak X-extent #'(0 . 0)")
                    for leaf in non_last_leaves:
                        abjad.override(leaf).NoteHead.transparent = "##t"
                        abjad.override(leaf).Glissando.layer = 3
                    abjad.glissando(new_components, zero_padding=True)
            else:
                new_components = components
                abjad.attach(abjad.StartBeam(), new_components[0])
                start_literal = abjad.LilyPondLiteral(
                    r"\start-multi-grace", site="before"
                )
                abjad.attach(start_literal, new_components[0])
                abjad.override(new_components[1]).Flag.stencil = "##f"
                abjad.override(
                    new_components[0]
                ).Beam.positions = rf"#'({position} . {position})"
            abjad.attach(abjad.StopBeam(), new_components[-1])
            stop_literal = abjad.LilyPondLiteral(r"\stop-multi-grace", site="after")
            abjad.attach(stop_literal, new_components[-1])
        else:
            copy = abjad.mutate.copy(components[0])
            temp = [copy]
            new_components = temp + components
            abjad.attach(abjad.StartBeam(), new_components[0])
            abjad.attach(abjad.StopBeam(), new_components[-1])
            abjad.override(new_components[0]).Beam.stencil = "##f"
            abjad.override(new_components[0]).Flag.stencil = "##f"
            start_literal = abjad.LilyPondLiteral(r"\start-single-grace", site="before")
            abjad.attach(start_literal, new_components[0])
            start_literal = abjad.LilyPondLiteral(r"\stop-single-grace", site="after")
            abjad.attach(start_literal, new_components[-1])
            abjad.override(
                new_components[0]
            ).Beam.positions = rf"#'({position} . {position})"
            abjad.override(new_components[0]).Stem.stencil = rf"##f"
            abjad.override(new_components[0]).NoteHead.transparent = rf"##t"
            if isinstance(new_components[0], abjad.Note):
                heads = [new_components[0].note_head]
            elif isinstance(new_components[0], abjad.Chord):
                heads = new_components[0].note_heads
            for head in heads:
                abjad.tweak(head, r"\tweak X-extent #'(0 . 0)")
            if with_glissando is True:
                abjad.override(new_components[1]).NoteHead.transparent = "##t"
                if isinstance(new_components[1], abjad.Note):
                    heads = [new_components[1].note_head]
                elif isinstance(new_components[1], abjad.Chord):
                    heads = new_components[1].note_heads
                for head in heads:
                    abjad.tweak(head, r"\tweak X-extent #'(0 . 0)")
                abjad.glissando(new_components, zero_padding=True)

        self._main_leaf = None
        abjad.AfterGraceContainer.__init__(
            self, new_components, language=language, tag=tag
        )


def after_grace_container(
    argument,
    counts,
    *,
    talea=rmakers.Talea([1], 8),
    position=6,
    with_glissando=False,
):
    _do_grace_container_command(
        argument,
        counts=counts,
        class_=AfterGraceContainer,
        talea=talea,
        position=position,
        with_glissando=with_glissando,
    )


def _do_grace_container_command(
    argument,
    counts,
    class_=None,
    talea=None,
    position=6,
    with_glissando=False,
):
    leaves = abjad.select.leaves(argument, grace=False)
    assert all(isinstance(_, int) for _ in counts), repr(counts)
    cyclic_counts = abjad.CyclicTuple(counts)
    start = 0
    for i, leaf in enumerate(leaves):
        count = cyclic_counts[i]
        if not count:
            continue
        stop = start + count
        durations = talea[start:stop]
        notes = abjad.makers.make_leaves([0], durations)
        if class_ == AfterGraceContainer:
            if with_glissando is True:
                abjad.attach(abjad.Glissando(zero_padding=True), leaf)
            container = class_(notes, position=position, with_glissando=with_glissando)
            abjad.attach(container, leaf)
        else:
            container = class_(notes, position=position)
            abjad.attach(container, leaf)
