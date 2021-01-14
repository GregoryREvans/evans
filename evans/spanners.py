import functools

import abjad


@functools.total_ordering
class BowAnglePoint:
    """
    Bow Angle Point
    """

    def __init__(
        self,
        degrees=None,
    ):
        if degrees is not None:
            self._degrees = abjad.NonreducedFraction(degrees, 90)
        else:
            self._degrees = degrees

    def __lt__(self, argument) -> bool:
        self_degrees = self.degrees or 0
        argument_degrees = argument.degrees or 0
        return self_degrees < argument_degrees

    def __repr__(self):
        return abjad.StorageFormatManager(self).get_repr_format()

    def __str__(self):
        return str(self.markup)

    @property
    def degrees(self):
        return self._degrees

    @property
    def markup(self):
        if self._degrees is None:
            degrees = 0
        else:
            degrees = self.degrees.numerator
        symbol = (
            r"\concat { \translate #'(0 . 0) "
            + f"{degrees}"
            + r" \translate #'(0 . 1) \teeny o \hspace #0.5 }"
        )
        string = rf"\vcenter {symbol}"
        markup = abjad.Markup(string)
        return markup


def bow_angle_spanner(
    argument,
    *,
    omit_bow_changes=True,
    tag=None,
):
    """
    bow angle spanner
    """

    def _get_indicators(leaf):
        bow_contact_point = None
        prototype = BowAnglePoint
        if leaf._has_indicator(prototype):
            bow_contact_point = leaf._get_indicators(prototype)[0]
        bow_motion_technique = None
        prototype = abjad.BowMotionTechnique
        if leaf._has_indicator(prototype):
            bow_motion_technique = leaf._get_indicators(prototype)[0]
        return (bow_contact_point, bow_motion_technique)

    def _make_bow_contact_point_tweaks(leaf, bow_contact_point):
        if bow_contact_point is None:
            return
        abjad.tweak(leaf.note_head).stencil = "ly:text-interface::print"
        abjad.tweak(leaf.note_head).text = bow_contact_point.markup
        y_offset = float((4 * bow_contact_point.degrees) - 2)
        abjad.tweak(leaf.note_head).Y_offset = y_offset

    def _make_bow_change_contributions(leaf, leaves, bow_contact_point):
        cautionary_change = False
        direction_change = None
        next_leaf = abjad.get.leaf(leaf, 1)
        this_contact_point = bow_contact_point
        if this_contact_point is None:
            return
        next_contact_point = abjad.get.indicator(next_leaf, BowAnglePoint)
        if next_contact_point is None:
            return
        previous_leaf = abjad.get.leaf(leaf, -1)
        previous_contact_point = None
        if previous_leaf is not None:
            previous_contact_points = previous_leaf._get_indicators(BowAnglePoint)
            if previous_contact_points:
                previous_contact_point = previous_contact_points[0]
        if (
            leaf is leaves[0]
            or previous_contact_point is None
            or previous_contact_point.degrees is None
        ):
            if this_contact_point < next_contact_point:
                direction_change = abjad.Down
            elif next_contact_point < this_contact_point:
                direction_change = abjad.Up
        else:
            previous_leaf = abjad.get.leaf(leaf, -1)
            previous_contact_point = abjad.get.indicator(previous_leaf, BowAnglePoint)
            if (
                previous_contact_point < this_contact_point
                and next_contact_point < this_contact_point
            ):
                direction_change = abjad.Up
            elif (
                this_contact_point < previous_contact_point
                and this_contact_point < next_contact_point
            ):
                direction_change = abjad.Down
            elif this_contact_point == previous_contact_point:
                if this_contact_point < next_contact_point:
                    cautionary_change = True
                    direction_change = abjad.Down
                elif next_contact_point < this_contact_point:
                    cautionary_change = True
                    direction_change = abjad.Up
        if direction_change is None:
            return
        if direction_change == abjad.Up:
            string = r"\evans-counterclockwise-arc \translate #'(0.2 . 0.75) \scale #'(0.7 . 0.7)"
        else:
            string = (
                r"\evans-clockwise-arc \translate #'(0.2 . 0.75) \scale #'(0.7 . 0.7)"
            )
        if cautionary_change:
            string = rf"\parenthesize {string}"
        string = "^ " + string
        literal = abjad.LilyPondLiteral(string, "after")
        abjad.attach(literal, leaf)

    def _next_leaf_is_bowed(leaf, leaves):
        if leaf is leaves[-1]:
            return False
        silent_prototype = (abjad.MultimeasureRest, abjad.Rest, abjad.Skip)
        next_leaf = abjad.get.leaf(leaf, 1)
        if next_leaf is None or isinstance(next_leaf, silent_prototype):
            return False
        next_contact_point = abjad.get.indicator(next_leaf, BowAnglePoint)
        if next_contact_point is None:
            return False
        elif next_contact_point.degrees is None:
            return False
        return True

    def _format_leaf(leaf, leaves):
        indicators = abjad.get.indicators(leaf)
        bow_contact_point = indicators[0]
        bow_motion_technique = indicators[1]
        if bow_contact_point is None:
            return
        if bow_contact_point.degrees is None:
            abjad.tweak(leaf.note_head).style = "cross"
            return
        if len(leaves) == 1:
            return
        _make_bow_contact_point_tweaks(leaf, bow_contact_point)
        if not _next_leaf_is_bowed(leaf, leaves):
            return
        glissando = abjad.Glissando()
        if bow_motion_technique is not None:
            style = abjad.SchemeSymbol(bow_motion_technique.glissando_style)
            abjad.tweak(glissando).style = style
        abjad.attach(glissando, leaf, tag=tag)
        if not omit_bow_changes:
            _make_bow_change_contributions(leaf, leaves, bow_contact_point)

    leaves = abjad.Selection(argument).leaves()
    assert isinstance(leaves, abjad.Selection), repr(leaves)
    for leaf in leaves:
        _format_leaf(leaf, leaves)


class StringDampComponent(abjad.Markup):
    def __init__(self, contents, *, direction=None):
        self._contents = contents
        if contents[0] == "(" and contents[-1] == ")":
            self.parens = (contents[0], contents[-1])
            self.parts = [_ for _ in contents[1:-1]]
        else:
            self.parens = False
            self.parts = [_ for _ in contents]
        self.column = self._interpret_components()
        self._direction = direction

    def __repr__(self):
        return abjad.StorageFormatManager(self.column).get_repr_format()

    def __str__(self):
        return self.column._get_lilypond_format()

    def _get_lilypond_format(self):
        return self.column._get_lilypond_format()

    char_to_note_head = {
        "o": abjad.Markup.musicglyph("noteheads.s0harmonic"),
        "*": abjad.Markup.musicglyph("noteheads.s2harmonic"),
        "x": abjad.Markup.musicglyph("noteheads.s2cross"),
        ".": abjad.Markup.musicglyph("noteheads.s2"),
    }

    length_to_paren_scale = {
        1: [
            abjad.Markup("(").general_align("Y", 0),
            abjad.Markup(")").general_align("Y", 0),
        ],
        2: [
            abjad.Markup("(").scale((1, 1.5)).general_align("Y", 0.5),
            abjad.Markup(")").scale((1, 1.5)).general_align("Y", 0.5),
        ],
        3: [
            abjad.Markup("(").scale((1, 2.4)).general_align("Y", 0.5),
            abjad.Markup(")").scale((1, 2.4)).general_align("Y", 0.5),
        ],
        4: [
            abjad.Markup("(").scale((1, 3.2)).general_align("Y", 0.65),
            abjad.Markup(")").scale((1, 3.2)).general_align("Y", 0.65),
        ],
    }

    def _interpret_components(self):
        heads = [self.char_to_note_head[_] for _ in self.parts]
        column = abjad.Markup.center_column(heads)
        column = column.scale((0.75, 0.75))
        column = column.override(("baseline-skip", 1.75))
        if self.parens:
            column_length = len(heads)
            paren_markups = self.length_to_paren_scale[column_length]
            column = abjad.Markup.concat(
                [
                    paren_markups[0],
                    abjad.Markup.hspace(-0.1),
                    column,
                    abjad.Markup.hspace(-0.15),
                    paren_markups[1],
                ],
            )
        return column

    def markup(self):
        return self.column


class StringDampSequence(abjad.Markup):
    def __init__(self, components, *, direction=None):
        self._components = [StringDampComponent(_).markup() for _ in components]
        self._direction = direction
        self.column = self._make_column()

    def __repr__(self):
        return abjad.StorageFormatManager(self.column).get_repr_format()

    def __str__(self):
        return self.column._get_lilypond_format()

    def _get_lilypond_format(self):
        return self.column._get_lilypond_format()

    def _get_format_pieces(self):
        return self.column._get_format_pieces()

    def _get_format_specification(self):
        return self.column._get_format_specification()

    def _make_column(self):
        m = abjad.Markup.center_column(self._components, direction=self._direction)
        m = m.override(("baseline-skip", 1.75))
        return m

    def markup(self):
        return self.column
