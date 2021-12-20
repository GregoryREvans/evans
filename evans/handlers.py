"""
Handler classes.
"""
import statistics

import abjad
import quicktions
from abjadext import microtones

from . import sequence
from .pitch import JIPitch, return_cent_markup, tune_to_ratio


class Handler:
    """
    Handler Base Class
    """

    def __repr__(self):
        return abjad.StorageFormatManager(self).get_repr_format()


class ArticulationHandler(Handler):
    r"""
    Articulation Handler

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c'4 c'4 r4 c'4 c'4 c'4 c'4 c'4")
        >>> art_lst = [
        ...     "staccato",
        ...     "tenuto",
        ...     "staccatissimo",
        ...     "open",
        ...     "halfopen",
        ...     "stopped",
        ...     "portato",
        ...     "tremolo"
        ... ]
        >>> handler = evans.ArticulationHandler(
        ...     articulation_list=art_lst,
        ...     articulation_boolean_vector=[1],
        ...     vector_forget=False,
        ...     forget=False,
        ... )
        >>> handler(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'4
                - \staccato
                c'4
                - \tenuto
                c'4
                - \staccatissimo
                r4
                c'4
                - \open
                c'4
                - \halfopen
                c'4
                - \stopped
                c'4
                - \portato
                c'4
                :32
            }

    """

    def __init__(
        self,
        articulation_list=None,
        articulation_boolean_vector=(1,),
        vector_forget=False,
        forget=True,
        count=-1,
        vector_count=-1,
        name="Articulation Handler",
    ):
        self.articulation_list = articulation_list
        self.vector_forget = vector_forget
        self.forget = forget
        self._count = count
        self._vector_count = vector_count
        self.articulation_boolean_vector = sequence.CyclicList(
            articulation_boolean_vector, self.vector_forget, self._vector_count
        )
        self._cyc_articulations = sequence.CyclicList(
            lst=articulation_list, forget=self.forget, count=self._count
        )
        self.name = name

    def __call__(self, selections):
        self.add_articulations(selections)

    def add_articulations(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        articulations = self._cyc_articulations(r=len(ties))
        vector = self.articulation_boolean_vector(r=len(ties))
        for tie, articulation, bool in zip(ties, articulations, vector):
            if bool == 1:
                if self.articulation_list is not None:
                    if articulation == "tremolo":
                        for leaf in tie:
                            if abjad.get.duration(leaf) <= abjad.Duration(1, 32):
                                continue
                            else:
                                abjad.attach(abjad.StemTremolo(32), leaf)
                    elif articulation == "default":
                        continue
                    else:
                        abjad.attach(abjad.Articulation(articulation), tie[0])
            else:
                continue

    def name(self):
        return self.name

    def state(self):
        return dict(
            [
                ("count", self._cyc_articulations.state()),
                ("vector_count", self.articulation_boolean_vector.state()),
            ]
        )


class BendHandler(Handler):
    r"""
    Bend Handler

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.BendHandler(
        ...     bend_amounts=[1, 1.5],
        ...     bend_forget=False,
        ...     boolean_vector=[1, 1, 0, 1],
        ...     vector_forget=False,
        ... )
        >>> handler(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'4
                - \bendAfter #'1
                c'4
                - \bendAfter #'1.5
                c'4
                c'4
                - \bendAfter #'1.5
            }

    """

    def __init__(
        self,
        bend_amounts=(1,),
        bend_forget=False,
        boolean_vector=(1,),
        vector_forget=False,
        bend_count=-1,
        vector_count=-1,
        name="Bend Handler",
    ):
        self._bend_count = bend_count
        self._vector_count = vector_count
        self.bend_forget = bend_forget
        self.vector_forget = vector_forget
        self.bend_amounts = sequence.CyclicList(
            bend_amounts, self.bend_forget, self._bend_count
        )
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.vector_forget, self._vector_count
        )
        self.name = name

    def __call__(self, selections):
        self.add_bend(selections)

    def add_bend(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        vector = self.boolean_vector(r=len(ties))
        amounts = self.bend_amounts(r=len(ties))
        for tie, bool, amount in zip(ties, vector, amounts):
            if bool == 1:
                abjad.attach(abjad.BendAfter(amount), tie[-1])
            else:
                continue

    def name(self):
        return self.name

    def state(self):
        return dict(
            [
                ("bend_count", self.bend_amounts.state()),
                ("vector_count", self.boolean_vector.state()),
            ]
        )


class BisbigliandoHandler(Handler):
    r"""
    Bisbigliando Handler

    ..  container:: example

        >>> s = abjad.Staff("c''4 c''4 c''4 c''4")
        >>> m = [
        ...     r"\markup {",
        ...     r"\lower #1.5",
        ...     r"\override #'(graphical . #t)",
        ...     r"\override #'(size . 0.4)",
        ...     r"\override #'(thickness . 0.25)",
        ...     r"\woodwind-diagram",
        ...     r"#'flute",
        ...     r"#'((cc . (one two three four five six)) (lh . (bes b gis)) (rh . (bes d dis ees cis c gz)))",
        ...     r"}",
        ... ]
        >>> handler = evans.BisbigliandoHandler(
        ...     fingering_list=[None, m],
        ...     boolean_vector=[1],
        ...     staff_padding=2,
        ... forget=False,
        ... )
        >>> handler(s[:-1])
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \new Staff
            {
                c''4
                - \tweak padding #2
                - \tweak staff-padding #2
                - \tweak bound-details.right.padding #2
                - \tweak bound-details.left.text
                \markup{ \raise #1 \teeny \musicglyph #"scripts.halfopenvertical" }
                \startTrillSpan
                c''4
                \stopTrillSpan
                - \tweak padding #2
                - \tweak staff-padding #2
                - \tweak bound-details.right.padding #2
                - \tweak bound-details.left.text
                \markup {
                \lower #1.5
                \override #'(graphical . #t)
                \override #'(size . 0.4)
                \override #'(thickness . 0.25)
                \woodwind-diagram
                #'flute
                #'((cc . (one two three four five six)) (lh . (bes b gis)) (rh . (bes d dis ees cis c gz)))
                }
                \startTrillSpan
                c''4
                \stopTrillSpan
                - \tweak padding #2
                - \tweak staff-padding #2
                - \tweak bound-details.right.padding #2
                - \tweak bound-details.left.text
                \markup{ \raise #1 \teeny \musicglyph #"scripts.halfopenvertical" }
                \startTrillSpan
                c''4
                \stopTrillSpan
            }

    """

    def __init__(
        self,
        *,
        bis_count=-1,
        bool_count=-1,
        boolean_vector=None,
        forget=False,  # forget=None
        fingering_list=None,
        name=None,
        padding=2,
        right_padding=2,
        staff_padding=2,
    ):
        self.bis_count = bis_count
        self.bool_count = bool_count
        if boolean_vector is None:
            boolean_vector = [1]
        self.boolean_vector = sequence.CyclicList(
            boolean_vector,
            forget=forget,
            count=bool_count,
        )
        self.forget = forget
        if fingering_list is None:
            fingering_list = [None]
        self.fingering_list = sequence.CyclicList(
            fingering_list,
            forget=forget,
            count=bis_count,
        )
        self.name = name
        self.padding = padding
        self.right_padding = right_padding
        self.staff_padding = staff_padding

    def __call__(self, selections):
        self.add_spanner(selections)

    def _make_start_literal(self):
        markup = r'\markup{ \raise #1 \teeny \musicglyph #"scripts.halfopenvertical" }'
        start_literal = abjad.LilyPondLiteral(
            [
                fr"- \tweak padding #{self.padding}",
                fr"- \tweak staff-padding #{self.staff_padding}",
                fr"- \tweak bound-details.right.padding #{self.right_padding}",
                fr"- \tweak bound-details.left.text {markup}",
                r"\startTrillSpan",
            ],
            format_slot="after",
        )
        return start_literal

    def _make_start_literal_pre(self):
        start_literal_pre = abjad.LilyPondLiteral(
            [
                fr"- \tweak padding #{self.padding}",
                fr"- \tweak staff-padding #{self.staff_padding}",
                fr"- \tweak bound-details.right.padding #{self.right_padding}",
                r"- \tweak bound-details.left.text",
            ],
            format_slot="after",
        )
        return start_literal_pre

    def _treat_tie(self, value, tie):
        if value != 1:
            return
        fingering = self.fingering_list(r=1)[0]
        if fingering is None:
            start_literal = self._make_start_literal()
            stop_literal = abjad.LilyPondLiteral(r"\stopTrillSpan", format_slot="after")
            abjad.attach(start_literal, tie[0])
            abjad.attach(stop_literal, abjad.get.leaf(tie[-1], 1))
            return
        start_literal_pre = self._make_start_literal_pre()
        start_literal = abjad.LilyPondLiteral(fingering, format_slot="after")
        start_literal_post = abjad.LilyPondLiteral(
            r"\startTrillSpan", format_slot="after"
        )
        stop_literal = abjad.LilyPondLiteral(r"\stopTrillSpan", format_slot="after")
        abjad.attach(start_literal_pre, tie[0])
        abjad.attach(start_literal, tie[0])
        abjad.attach(start_literal_post, tie[0])
        abjad.attach(stop_literal, abjad.get.leaf(tie[-1], 1))

    def add_spanner(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        values = self.boolean_vector(r=len(ties))
        for value, tie in zip(values, ties):
            self._treat_tie(value, tie)

    def state(self):
        state_dict = dict()
        state_dict["boolean_vector_count"] = self.boolean_vector.count
        state_dict["fingering_list_count"] = self.fingering_list.count
        return state_dict


class BowAngleHandler(Handler):
    r"""
    Bow Angle Handler: In Progress

    ..  container:: example

        >>> s = abjad.Staff("c'2 c'2 c'2 c'2 r2 r2")
        >>> handler = evans.BowAngleHandler([0, 45, 0, -45])
        >>> handler(s)
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         "\\include \'Users/gregoryevans/evans/lilypond/evans-markups.ily\'",
        ...         "\\include \'Users/gregoryevans/evans/lilypond/evans-spanners.ily\'",
        ...         score,
        ...     ],
        ... )
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \new Staff
            {
                c'2
                - \abjad-solid-line-with-arrow
                - \evans-clockwise-BAD-spanner-left-text #0
                - \tweak bound-details.right.padding 1.4
                - \tweak staff-padding #2
                \evansStartTextSpanBAD
                c'2
                \evansStopTextSpanBAD
                - \abjad-solid-line-with-arrow
                - \evans-counterclockwise-BAD-spanner-left-text #45
                - \tweak bound-details.right.padding 1.4
                - \tweak staff-padding #2
                \evansStartTextSpanBAD
                c'2
                \evansStopTextSpanBAD
                - \abjad-solid-line-with-arrow
                - \evans-counterclockwise-BAD-spanner-left-text #0
                - \tweak bound-details.right.padding 1.4
                - \tweak staff-padding #2
                \evansStartTextSpanBAD
                c'2
                \evansStopTextSpanBAD
                - \abjad-solid-line-with-arrow
                - \evans-clockwise-BAD-spanner-left-text #-45
                - \evans-BAD-spanner-right-text #0
                - \tweak bound-details.right.padding 1.4
                - \tweak staff-padding #2
                \evansStartTextSpanBAD
                r2
                \evansStopTextSpanBAD
                r2
            }

    """

    def __init__(
        self,
        angles=(0, 45),
    ):
        self.agles = angles
        self._cyc_angles = sequence.CyclicList(angles, forget=False)

    def __call__(self, selections):
        self._add_spanners(selections)

    def _return_arc_direction(self, left_number, right_number):
        if left_number < right_number:
            return "clockwise"
        else:
            return "counterclockwise"

    def _add_spanners(self, selections):
        for run in abjad.select(selections).runs():
            numbers = self._cyc_angles(r=len(run) + 1)
            first_leaf = abjad.select(run).leaf(0)
            start_literal = abjad.LilyPondLiteral(
                [
                    r"- \abjad-solid-line-with-arrow",
                    rf"- \evans-{self._return_arc_direction(numbers[0], numbers[1])}-BAD-spanner-left-text #{numbers[0]}",
                    r"- \tweak bound-details.right.padding 1.4",
                    r"- \tweak staff-padding #2",
                    r"\evansStartTextSpanBAD",
                ],
                format_slot="absolute_after",
            )
            abjad.attach(start_literal, first_leaf)
            for i, tie in enumerate(abjad.select(run).logical_ties()[1:-1]):
                literal = abjad.LilyPondLiteral(
                    [
                        r"\evansStopTextSpanBAD",
                        r"- \abjad-solid-line-with-arrow",
                        rf"- \evans-{self._return_arc_direction(numbers[i + 1], numbers[i + 2])}-BAD-spanner-left-text #{numbers[i + 1]}",
                        r"- \tweak bound-details.right.padding 1.4",
                        r"- \tweak staff-padding #2",
                        r"\evansStartTextSpanBAD",
                    ],
                    format_slot="absolute_after",
                )
                abjad.attach(literal, tie[0])
            terminating_literal = abjad.LilyPondLiteral(
                [
                    r"\evansStopTextSpanBAD",
                    r"- \abjad-solid-line-with-arrow",
                    rf"- \evans-{self._return_arc_direction(numbers[-2], numbers[-1])}-BAD-spanner-left-text #{numbers[-2]}",
                    rf"- \evans-BAD-spanner-right-text #{numbers[-1]}",
                    r"- \tweak bound-details.right.padding 1.4",
                    r"- \tweak staff-padding #2",
                    r"\evansStartTextSpanBAD",
                ],
                format_slot="absolute_after",
            )
            abjad.attach(terminating_literal, abjad.select(run).leaf(-1))
            last_leaf = abjad.get.leaf(abjad.select(run).leaf(-1), 1)
            stop_literal = abjad.LilyPondLiteral(
                r"\evansStopTextSpanBAD", format_slot="absolute_after"
            )
            abjad.attach(stop_literal, last_leaf)

    def state(self):
        return "State not yet maintained."


# add shelf for ottava to ensure that no notes in the bracket are illegible
class ClefHandler(Handler):
    r"""
    Clef Handler

    .. container:: example

        >>> s = abjad.Staff("c,4 c'4 c4 c''4 c''''8 r8")
        >>> handler = evans.ClefHandler(
        ...     clef="bass",
        ...     add_extended_clefs=True,
        ...     add_ottavas=True,
        ... )
        >>> handler(s)
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs

            >>> print(abjad.lilypond(s))
            \new Staff
            {
                \clef "bass"
                c,4
                c'4
                c4
                \clef "tenorvarC"
                c''4
                \ottava 1
                \clef "treble"
                c''''8
                \ottava 0
                r8
            }

    """

    _clef_groups_up = {
        "bass": ("bass", "tenorvarC", "treble"),  # "treble^8", "treble^15"),
        "tenor": ("tenorvarC", "treble"),  # "treble^8", "treble^15"),
        "alto": ("varC", "treble"),  # "treble^8", "treble^15"),
        "treble": ("treble",),  # "treble^8", "treble^15"),
    }

    _clef_groups_down = {
        "bass": ("bass", "bass_8", "bass_15"),
        "tenor": ("tenorvarC", "bass", "bass_8"),
        "alto": ("varC", "bass", "bass_8"),
        "treble": ("treble", "treble_8", "bass"),
    }

    _default_clef_shelves = {
        "bass": (-28, 6),
        "tenor": (-10, 12),
        "tenorvarC": (-10, 12),
        "alto": (-12, 18),
        "varC": (-12, 18),
        "treble": (-5, 24),
        "treble^8": (7, 36),
        "treble^15": (19, 48),
    }

    def __init__(
        self,
        clef=None,
        clef_shelf=None,
        allowable_clefs=None,
        add_extended_clefs=False,
        ottava_shelf=None,
        add_ottavas=False,
        extend_in_direction="up",
    ):
        self.clef = clef
        self.clef_shelf = clef_shelf
        self.allowable_clefs = allowable_clefs
        self.add_extended_clefs = add_extended_clefs
        self.ottava_shelf = ottava_shelf
        self.add_ottavas = add_ottavas
        self.extend_in_direction = extend_in_direction

        if self.clef_shelf is not None:
            self._default_clef_shelves[self.clef] = self.clef_shelf

    def __call__(self, voice):
        self._add_clefs(voice)
        self._add_ottavas(voice)

    def _extended_range_clefs(self, clef):
        if self.extend_in_direction == "down":
            return self._clef_groups_down[clef]
        else:
            return self._clef_groups_up[clef]

    def _extended_range_ottavas(self, clef):
        return self._default_clef_shelves[clef]

    def _add_clefs(self, voice):  # allow the beginning of a run to ignore active clef
        clef = self.clef
        if clef is not None:
            base_clef = self.clef
            first_clef_name = self._extended_range_clefs(clef)[0]
            clef_list = [abjad.Clef(first_clef_name)]
            abjad.attach(clef_list[0], abjad.select(voice).leaves()[0])
            if self.add_extended_clefs is True:
                allowable_clefs = None
                if self.allowable_clefs is not None:
                    allowable_clefs = self.allowable_clefs
                else:
                    allowable_clefs = self._extended_range_clefs(base_clef)
                for tie in abjad.select(voice).logical_ties(pitched=True):
                    pitches = []
                    for pitch in abjad.get.pitches(tie[0]):
                        pitches.append(pitch.number)
                    pitch = statistics.mean(pitches)
                    value = None
                    for count, allowed_clef in enumerate(allowable_clefs):
                        if clef_list[-1] == abjad.Clef(allowed_clef):
                            value = count
                        else:
                            continue
                    active_clef_in_list = clef_list[-1]
                    range_ = self._extended_range_ottavas(active_clef_in_list.name)
                    active_clef_in_list_shelf = range_
                    if pitch > active_clef_in_list_shelf[1]:
                        test_value = value + 1
                        if test_value < len(allowable_clefs):
                            temp_clef = allowable_clefs[test_value]
                            clef = abjad.Clef(temp_clef)
                            if clef == clef_list[-1]:
                                continue
                            if abjad.get.indicator(tie[0], abjad.Clef) is not None:
                                indicator = abjad.get.indicator(tie[0], abjad.Clef)
                                abjad.detach(indicator, tie[0])
                                abjad.attach(clef, tie[0])
                                clef_list.append(clef)
                            else:
                                abjad.attach(clef, tie[0])
                                clef_list.append(clef)
                            if pitch > self._extended_range_ottavas(temp_clef)[1]:
                                test_value = value + 2
                                if test_value < len(allowable_clefs):
                                    temp_clef = allowable_clefs[test_value]
                                    clef = abjad.Clef(temp_clef)
                                    if clef == clef_list[-1]:
                                        continue
                                    indicator = abjad.get.indicator(tie[0], abjad.Clef)
                                    if indicator is not None:
                                        abjad.detach(indicator, tie[0])
                                        abjad.attach(clef, tie[0])
                                        clef_list.append(clef)
                                    else:
                                        abjad.attach(clef, tie[0])
                                        clef_list.append(clef)
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue
                    elif pitch < active_clef_in_list_shelf[0]:
                        test_value = value - 2
                        if test_value > -1:
                            temp_clef = allowable_clefs[test_value]
                            clef = abjad.Clef(temp_clef)
                            if clef == clef_list[-1]:
                                continue
                            indicator = abjad.get.indicator(tie[0], abjad.Clef)
                            if indicator is not None:
                                abjad.detach(indicator, tie[0])
                                abjad.attach(clef, tie[0])
                                clef_list.append(clef)
                            else:
                                abjad.attach(clef, tie[0])
                                clef_list.append(clef)
                            if pitch > self._extended_range_ottavas(temp_clef)[1]:
                                test_value = value - 1
                                if test_value > -1:
                                    temp_clef = allowable_clefs[test_value]
                                    clef = abjad.Clef(temp_clef)
                                    if clef == clef_list[-1]:
                                        continue
                                    indicator = abjad.get.indicator(tie[0], abjad.Clef)
                                    if indicator is not None:
                                        abjad.detach(indicator, tie[0])
                                        abjad.attach(clef, tie[0])
                                        clef_list.append(clef)
                                    else:
                                        abjad.attach(clef, tie[0])
                                        clef_list.append(clef)
                                else:
                                    continue
                            else:
                                continue
                        else:
                            test_value = value - 1
                            if test_value > -1:
                                temp_clef = allowable_clefs[test_value]
                                clef = abjad.Clef(temp_clef)
                                if clef == clef_list[-1]:
                                    continue
                                indicator = abjad.get.indicator(tie[0], abjad.Clef)
                                if indicator is not None:
                                    abjad.detach(indicator, tie[0])
                                    abjad.attach(clef, tie[0])
                                    clef_list.append(clef)
                                else:
                                    abjad.attach(clef, tie[0])
                                    clef_list.append(clef)
                            else:
                                continue
                    else:
                        continue
            else:
                converted_clef = self._extended_range_clefs(clef)[0]
                clef = abjad.Clef(converted_clef)
                first_leaf = abjad.select(voice).leaves()[0]
                indicator = abjad.get.indicator(first_leaf, abjad.Clef)
                if indicator is not None:
                    abjad.detach(indicator, first_leaf)
                    abjad.attach(clef, first_leaf)
                else:
                    abjad.attach(clef, first_leaf)
        else:
            clef = abjad.Clef("treble")
            first_leaf = abjad.select(voice).leaves()[0]
            abjad.attach(clef, first_leaf)

    def _add_ottavas(self, voice):
        if self.add_ottavas is True:
            if self.allowable_clefs is not None:
                active_clef = self.allowable_clefs[-1]
            else:
                active_clef = self._extended_range_clefs(self.clef)[-1]
            for tie in abjad.select(voice).logical_ties(pitched=True):
                current_clef = active_clef
                if self.ottava_shelf is not None:
                    shelf = self.ottava_shelf
                    if self.extend_in_direction == "down":
                        for pitch in abjad.get.pitches(tie[0]):
                            if pitch < shelf[0]:
                                start = abjad.Ottava(n=-1)
                                stop = abjad.Ottava(n=0)
                                ottava_indicator = abjad.get.indicator(
                                    tie[0], abjad.Ottava
                                )
                                if ottava_indicator is not None:
                                    abjad.detach(ottava_indicator, tie[0])
                                    abjad.attach(stop, abjad.get.leaf(tie[-1], 1))
                                else:
                                    abjad.attach(start, tie[0])
                                    abjad.attach(stop, abjad.get.leaf(tie[-1], 1))
                    else:
                        for pitch in abjad.get.pitches(tie[0]):
                            if pitch > shelf[1]:
                                start = abjad.Ottava(n=1)
                                stop = abjad.Ottava(n=0)
                                ottava_indicator = abjad.get.indicator(
                                    tie[0], abjad.Ottava
                                )
                                if ottava_indicator is not None:
                                    abjad.detach(ottava_indicator, tie[0])
                                    abjad.attach(stop, abjad.get.leaf(tie[-1], 1))
                                else:
                                    abjad.attach(start, tie[0])
                                    abjad.attach(stop, abjad.get.leaf(tie[-1], 1))
                else:
                    shelf = self._extended_range_ottavas(current_clef)
                    if self.extend_in_direction == "down":
                        for pitch in abjad.get.pitches(tie[0]):
                            if pitch < shelf[0]:
                                start = abjad.Ottava(n=-1)
                                stop = abjad.Ottava(n=0)
                                ottava_indicator = abjad.get.indicator(
                                    tie[0], abjad.Ottava
                                )
                                if ottava_indicator is not None:
                                    abjad.detach(ottava_indicator, tie[0])
                                    abjad.attach(stop, abjad.get.leaf(tie[-1], 1))
                                else:
                                    abjad.attach(start, tie[0])
                                    abjad.attach(stop, abjad.get.leaf(tie[-1], 1))
                    else:
                        for pitch in abjad.get.pitches(tie[0]):
                            if pitch > shelf[1]:
                                start = abjad.Ottava(n=1)
                                stop = abjad.Ottava(n=0)
                                ottava_indicator = abjad.get.indicator(
                                    tie[0], abjad.Ottava
                                )
                                if ottava_indicator is not None:
                                    abjad.detach(ottava_indicator, tie[0])
                                    abjad.attach(stop, abjad.get.leaf(tie[-1], 1))
                                else:
                                    abjad.attach(start, tie[0])
                                    abjad.attach(stop, abjad.get.leaf(tie[-1], 1))
        else:
            pass


class CompositeHandler(Handler):
    r"""
    Composite Handler

    .. container:: example

        >>> durs = [abjad.Duration((4, 4))]
        >>> rh = evans.RhythmHandler(evans.RTMMaker(["(1 (1 1 1 1))"]))
        >>> ph = evans.PitchHandler([0, 1, 2, 3])
        >>> ah = evans.ArticulationHandler(["staccato", "tenuto"])
        >>> comp = evans.CompositeHandler(rhythm_handler=rh, attachment_handlers=[ph, ah])
        >>> n = comp(durations=durs)
        >>> st = abjad.Staff()
        >>> st.extend(n)
        >>> score = abjad.Score([st])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs

            >>> print(abjad.lilypond(st))
            \new Staff
            {
                c'4
                - \staccato
                cs'4
                - \tenuto
                d'4
                - \staccato
                ef'4
                - \tenuto
            }

    """

    def __init__(
        self,
        rhythm_handler=None,
        attachment_handlers=(None,),
        name="Composite Handler",
    ):
        self.rhythm_handler = rhythm_handler
        self.attachment_handlers = attachment_handlers
        self.name = name

    def __call__(
        self,
        durations=(None,),
        selections=None,
    ):
        if self.rhythm_handler is not None:
            selections = self._make_container(self.rhythm_handler, durations)
        for handler in self.attachment_handlers:
            handler(selections)
        return selections[:]

    def _make_container(self, handler, durations):
        selections = handler(durations)
        container = abjad.Container([])
        container.extend(selections)
        return container

    def return_state(self):
        return self.rhythm_handler.return_state()

    def state(self):
        state_dict = dict()
        for _ in self.attachment_handlers:
            state_dict[_.name] = _.state()
        return state_dict


# incorporate spanner anchors
class DynamicHandler(Handler):
    r"""
    Dynamic Handler

    .. container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4 r4 g'4 r2")
        >>> handler = evans.DynamicHandler(
        ...     dynamic_list=['f', 'niente', 'p', 'mf'],
        ...     flare_boolean_vector=[0, 0, 0, 1],
        ...     flare_forget=False,
        ...     hold_first_boolean_vector=[1, 0, 0,],
        ...     hold_first_forget=False,
        ...     hold_last_boolean_vector=[0, 1],
        ...     hold_last_forget=False,
        ...     effort_boolean_vector=[1, 0],
        ...     effort_forget=False,
        ...     forget=False,
        ... )
        >>> first_group = staff[0:3]
        >>> second_group = staff[2:]
        >>> handler(first_group)
        >>> handler(second_group)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'4
                _ #(make-dynamic-script
                    (markup
                        #:whiteout
                        #:line (
                            #:general-align Y -2 #:normal-text #:larger "“"
                            #:hspace -0.4
                            #:dynamic "f"
                            #:hspace -0.2
                            #:general-align Y -2 #:normal-text #:larger "”"
                            )
                        )
                    )
                - \tweak stencil #constante-hairpin
                \<
                d'4
                e'4
                - \tweak circled-tip ##t
                \<
                f'4
                <>
                _ #(make-dynamic-script
                    (markup
                        #:whiteout
                        #:line (
                            #:general-align Y -2 #:normal-text #:larger "“"
                            #:hspace -0.1
                            #:dynamic "p"
                            #:hspace -0.25
                            #:general-align Y -2 #:normal-text #:larger "”"
                            )
                        )
                    )
                r4
                g'4
                \mf
                - \tweak stencil #constante-hairpin
                \<
                r2
                \!
            }

    """

    def __init__(
        self,
        dynamic_list=None,
        flare_boolean_vector=[0],
        flare_forget=False,
        hold_first_boolean_vector=[0],
        hold_first_forget=False,
        hold_last_boolean_vector=[0],
        hold_last_forget=False,
        effort_boolean_vector=[0],
        effort_forget=False,
        with_constante_hairpins=True,
        forget=False,
        terminating_dynamic_markup=False,
        terminating_dynamic_markup_boolean_vector=[1],
        count_1=-1,
        count_2=-1,
        count_3=-1,
        count_4=-1,
        count_5=-1,
        name="Dynamic Handler",
    ):
        self.dynamic_list = dynamic_list
        self.flare_boolean_vector = flare_boolean_vector
        self.flare_forget = flare_forget
        self.hold_first_boolean_vector = hold_first_boolean_vector
        self.hold_first_forget = hold_first_forget
        self.hold_last_boolean_vector = hold_last_boolean_vector
        self.hold_last_forget = hold_last_forget
        self.effort_boolean_vector = effort_boolean_vector
        self.effort_forget = effort_forget
        self.with_constante_hairpins = with_constante_hairpins
        self.forget = forget
        self.terminating_dynamic_markup = terminating_dynamic_markup
        self.terminating_dynamic_markup_boolean_vector = (
            terminating_dynamic_markup_boolean_vector
        )
        self._count_1 = count_1
        self._count_2 = count_2
        self._count_3 = count_3
        self._count_4 = count_4
        self._count_5 = count_5
        self._cyc_dynamics = sequence.CyclicList(
            dynamic_list,
            self.forget,
            self._count_1,
        )
        self._cyc_flare_boolean_vector = sequence.CyclicList(
            flare_boolean_vector,
            self.flare_forget,
            self._count_2,
        )
        self._cyc_hold_first_boolean_vector = sequence.CyclicList(
            hold_first_boolean_vector,
            self.hold_first_forget,
            self._count_3,
        )
        self._cyc_hold_last_boolean_vector = sequence.CyclicList(
            hold_last_boolean_vector,
            self.hold_last_forget,
            self._count_4,
        )
        self._cyc_effort_boolean_vector = sequence.CyclicList(
            effort_boolean_vector,
            self.effort_forget,
            self._count_5,
        )
        self._terminating_dynamic_boolean_vector = sequence.CyclicList(
            terminating_dynamic_markup_boolean_vector,
            False,
            -1,
        )
        self.name = name

    def __call__(self, selections):
        self._apply_dynamics(selections)

    def _calculate_hairpin(self, start, stop, flared=0):
        if isinstance(start, str):
            start = abjad.Dynamic(start)
        elif isinstance(start, int):
            ord_to_name = abjad.Dynamic.dynamic_ordinal_to_dynamic_name(start)
            start = abjad.Dynamic(ord_to_name)
        else:
            pass
        if isinstance(stop, str):
            stop = abjad.Dynamic(stop)
        elif isinstance(stop, int):
            ord_to_name = abjad.Dynamic.dynamic_ordinal_to_dynamic_name(stop)
            stop = abjad.Dynamic(ord_to_name)
        else:
            pass
        if flared == 1:
            if start.ordinal < stop.ordinal:
                if start.name == "niente":  # carry these through instead?
                    start = abjad.Dynamic("niente", hide=True)
                    hairpin = "o<|"
                else:
                    hairpin = "<|"
            else:
                if stop.name == "niente":
                    stop = abjad.Dynamic("niente", command=r"\!")
                    hairpin = "|>o"
                else:
                    hairpin = "|>"
        else:
            if start.ordinal < stop.ordinal:
                if start.name == "niente":
                    start = abjad.Dynamic("niente", hide=True)
                    hairpin = "o<"
                else:
                    hairpin = "<"
            else:
                if stop.name == "niente":
                    stop = abjad.Dynamic("niente", command=r"\!")
                    hairpin = ">o"
                else:
                    hairpin = ">"
        return hairpin  # , start, stop?

    def _make_effort_dynamics(self, dyn):
        conversion = {
            "ppppp": '"ppppp"',
            "pppp": '"pppp"',
            "ppp": '"ppp"',
            "pp": '"pp"',
            "p": '"p"',
            "mp": '"mp"',
            "mf": '"mf"',
            "f": '"f"',
            "ff": '"ff"',
            "fff": '"fff"',
            "ffff": '"ffff"',
            "fffff": '"fffff"',
            "fp": '"fp"',
            "sf": '"sf"',
            "sff": '"sff"',
            "sp": '"sp"',
            "spp": '"spp"',
            "sfz": '"sfz"',
            "sffz": '"sffz"',
            "sfffz": '"sfffz"',
            "sffp": '"sffp"',
            "sffpp": '"sffpp"',
            "sfp": '"sfp"',
            "sfpp": '"sfpp"',
            "rfz": '"rfz"',
            "niente": "niente",
        }
        return conversion[dyn]

    def _apply_dynamics(self, selections):
        for run in abjad.select(selections).runs():
            hold_first = self._cyc_hold_first_boolean_vector(r=1)[0]
            if hold_first == 0:
                if len(run) > 1:
                    if abjad.get.has_indicator(run[0], abjad.Dynamic):
                        current_dynamic = abjad.get.indicator(run[0], abjad.Dynamic)
                        start = abjad.Dynamic(current_dynamic, hide=True)
                        stop = self._cyc_dynamics(r=1)[0]
                    else:
                        items = self._cyc_dynamics(r=2)
                        start = items[0]
                        stop = items[1]
                    flare_value = self._cyc_flare_boolean_vector(r=1)[0]
                    calculated_hairpin = self._calculate_hairpin(
                        start, stop, flared=flare_value
                    )
                    hairpin = abjad.StartHairpin(calculated_hairpin)
                    hold_last = self._cyc_hold_last_boolean_vector(r=1)[0]
                    effort_bools = self._cyc_effort_boolean_vector(r=2)
                    if isinstance(start, str):
                        if effort_bools[0] == 0:
                            start = start
                        else:
                            start = self._make_effort_dynamics(start)
                        start = abjad.Dynamic(start)
                    elif isinstance(start, int):
                        start = abjad.Dynamic.dynamic_ordinal_to_dynamic_name(start)
                        if effort_bools[0] == 0:
                            start = start
                        else:
                            start = self._make_effort_dynamics(start)
                        start = abjad.Dynamic(start)
                    else:
                        pass
                    if isinstance(stop, str):
                        if effort_bools[1] == 0:
                            stop = stop
                        else:
                            stop = self._make_effort_dynamics(stop)
                        stop = abjad.Dynamic(stop)
                    elif isinstance(stop, int):
                        stop = abjad.Dynamic.dynamic_ordinal_to_dynamic_name(stop)
                        if effort_bools[1] == 0:
                            stop = stop
                        else:
                            stop = self._make_effort_dynamics(stop)
                        stop = abjad.Dynamic(stop)
                    else:
                        pass
                    if start.name == "niente":
                        start = abjad.Dynamic("niente", hide=True)
                    if stop.name == "niente":
                        stop = abjad.Dynamic("niente", command=r"\!")
                    if hold_last == 1:
                        if stop.name != "niente":
                            if self.with_constante_hairpins is True:
                                abjad.attach(abjad.StartHairpin("--"), run[-1])
                                next_tie_leaf = abjad.get.leaf(run[-1], 1)
                                abjad.attach(abjad.StopHairpin(), next_tie_leaf)
                        else:  # attach to anchor?
                            if isinstance(abjad.get.leaf(run[-1], 1), abjad.Rest):
                                stop = abjad.Dynamic(stop, command=r"\!", leak=True)
                            else:
                                pass
                    else:
                        if isinstance(abjad.get.leaf(run[-1], 1), abjad.Rest):
                            stop = abjad.Dynamic(stop, leak=True)  # attach to anchor
                        else:
                            pass
                    if abjad.get.has_indicator(run[0], abjad.Dynamic):
                        abjad.attach(abjad.StopHairpin(), run[0])
                        abjad.attach(hairpin, run[0])
                        abjad.attach(stop, run[-1])
                    else:
                        abjad.hairpin([start, hairpin, stop], run)
                        if self.terminating_dynamic_markup is True:  # NEW
                            markup_val = self._terminating_dynamic_boolean_vector(r=1)[
                                0
                            ]
                            if markup_val == 1:
                                if start.ordinal < stop.ordinal:
                                    mark_text = abjad.Markup(
                                        fr"""\markup {{ \override #'(style . "box") \override #'(box-padding . 0.5) \italic \box \whiteout \small "cresc. a {stop.name}" }}""",
                                        direction=abjad.Down,
                                    )
                                else:
                                    mark_text = abjad.Markup(
                                        fr"""\markup {{ \override #'(style . "box") \override #'(box-padding . 0.5) \italic \box \whiteout \small "dim. a {stop.name}" }}""",
                                        direction=abjad.Down,
                                    )
                                abjad.attach(mark_text, abjad.select(run).leaf(0))
                else:
                    hold_last = self._cyc_hold_last_boolean_vector(r=1)[0]
                    if hold_last == 1:
                        start = self._cyc_dynamics(r=1)[0]
                        if start == "niente":
                            start = self._cyc_dynamics(r=1)[0]
                        else:
                            pass
                        if self._cyc_effort_boolean_vector(r=1)[0] == 0:
                            start = abjad.Dynamic(start)
                        else:
                            start_string = self._make_effort_dynamics(start)
                            start = abjad.Dynamic(start_string)
                        sustain = abjad.StartHairpin("--")
                        next_leaf = abjad.get.leaf(run[-1], 1)
                        abjad.attach(start, run[0])
                        if self.with_constante_hairpins is True:
                            abjad.attach(sustain, run[0])
                            if isinstance(
                                next_leaf, (abjad.Rest, abjad.MultimeasureRest)
                            ):
                                abjad.attach(abjad.StopHairpin(), next_leaf)
                    else:
                        items = self._cyc_dynamics(r=2)
                        effort_bools = self._cyc_effort_boolean_vector(r=2)
                        start = items[0]
                        stop = items[1]
                        if effort_bools[0] == 0:
                            if start == "niente":
                                start = abjad.Dynamic(start, hide=True)
                            else:
                                start = abjad.Dynamic(start)
                        else:
                            start_string = self._make_effort_dynamics(start)
                            if start_string == "niente":
                                start = abjad.Dynamic(start_string, hide=True)
                            else:
                                start = abjad.Dynamic(start_string)
                        if effort_bools[1] == 0:
                            if stop == "niente":
                                stop = abjad.Dynamic(
                                    stop, command=r"\!", leak=True
                                )  # attach to anchor
                            else:
                                stop = abjad.Dynamic(
                                    stop, leak=True
                                )  # attach to anchor
                        else:
                            stop_string = self._make_effort_dynamics(stop)
                            if stop_string == "niente":
                                stop = abjad.Dynamic(
                                    stop_string,
                                    command=r"\!",
                                    leak=True,  # attach to anchor
                                )
                            else:
                                stop = abjad.Dynamic(
                                    stop_string, leak=True
                                )  # attach to anchor
                        flare_value = self._cyc_flare_boolean_vector(r=1)[0]
                        calculated_hairpin = self._calculate_hairpin(
                            start,
                            stop,
                            flared=flare_value,
                        )
                        hairpin = abjad.StartHairpin(calculated_hairpin)
                        abjad.hairpin([start, hairpin, stop], run)
                        if self.terminating_dynamic_markup is True:  # NEW
                            markup_val = self._terminating_dynamic_boolean_vector(r=1)[
                                0
                            ]
                            if markup_val == 1:
                                if start.ordinal < stop.ordinal:
                                    mark_text = abjad.Markup(
                                        fr"""\markup {{ \override #'(style . "box") \override #'(box-padding . 0.5) \italic \box \whiteout \small "cresc. a {stop.name}" }}""",
                                        direction=abjad.Down,
                                    )
                                else:
                                    mark_text = abjad.Markup(
                                        fr"""\markup {{ \override #'(style . "box") \override #'(box-padding . 0.5) \italic \box \whiteout \small "dim. a {stop.name}" }}""",
                                        direction=abjad.Down,
                                    )
                                abjad.attach(mark_text, abjad.select(run).leaf(0))
            else:
                start = self._cyc_dynamics(r=1)[0]
                if start == "niente":
                    start = self._cyc_dynamics(r=1)[0]
                effort_bool = self._cyc_effort_boolean_vector(r=1)[0]
                if effort_bool == 1:
                    start_string = self._make_effort_dynamics(start)
                    start = abjad.Dynamic(start_string)
                else:
                    start = abjad.Dynamic(start)
                hairpin = abjad.StartHairpin("--")
                stopper = abjad.StopHairpin()
                next_leaf = abjad.get.leaf(run[-1], 1)
                abjad.attach(start, run[0])
                if self.with_constante_hairpins is True:
                    abjad.attach(hairpin, run[0])
                    if isinstance(next_leaf, (abjad.Rest, abjad.MultimeasureRest)):
                        abjad.attach(stopper, next_leaf)
                else:
                    pass
        self._remove_niente(selections)

    # attach to anchor?
    # maybe just continue instead of replacing?
    def _remove_niente(self, selections):
        for leaf in abjad.select(selections).leaves():
            for dynamic in abjad.get.indicators(leaf, abjad.Dynamic):
                if dynamic.name == "niente":
                    if dynamic.command == r"\!":
                        abjad.detach(dynamic, leaf)
                        abjad.attach(
                            abjad.Dynamic(dynamic, command=r"\!", leak=True), leaf
                        )
                    elif dynamic.leak is True:
                        abjad.detach(dynamic, leaf)
                        abjad.attach(
                            abjad.Dynamic(dynamic, command=r"\!", leak=True), leaf
                        )
                    else:
                        abjad.detach(dynamic, leaf)
                        abjad.attach(abjad.Dynamic(dynamic, hide=True), leaf)
                else:
                    continue

    def name(self):
        return self.name

    def state(self):
        return dict(
            [
                ("count_1", self._cyc_dynamics.state()),
                ("count_2", self._cyc_flare_boolean_vector.state()),
                ("count_3", self._cyc_hold_first_boolean_vector.state()),
                ("count_4", self._cyc_hold_last_boolean_vector.state()),
                ("count_5", self._cyc_effort_boolean_vector.state()),
            ]
        )


class GettatoHandler(Handler):
    r"""
    Gettato Handler

    .. container:: example

        >>> staff = abjad.Voice("c'4 fs'4 c''4 gqs''4", name="Voice 1")
        >>> handler = evans.GettatoHandler(
        ...     number_of_attacks=[4, 5, 6],
        ...     actions=["throw", "drop"],
        ... )
        >>> handler(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \context Voice = "Voice 1"
            {
                <<
                    \context Voice = "On_Beat_Grace_Container"
                    {
                        \set fontSize = #-4
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        \once \override Beam.grow-direction = #left
                        \slash
                        \voiceOne
                        <
                            \tweak font-size 0
                            \tweak transparent ##t
                            c'
                        >32 * 4/3
                        ^ \markup { \hspace #1 throw (4)}
                        [
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        c'32 * 4/3
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        c'32 * 4/3
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        c'32 * 4/3
                        ]
                    }
                    \context Voice = "Voice 1"
                    {
                        \voiceTwo
                        c'4
                    }
                >>
                <<
                    \context Voice = "On_Beat_Grace_Container"
                    {
                        \set fontSize = #-4
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        \once \override Beam.grow-direction = #right
                        \slash
                        \voiceOne
                        <
                            \tweak font-size 0
                            \tweak transparent ##t
                            fs'
                        >32 * 4/3
                        ^ \markup { \hspace #1 drop (5)}
                        [
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        fs'32 * 4/3
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        fs'32 * 4/3
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        fs'32 * 4/3
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        fs'32 * 4/3
                        ]
                    }
                    \context Voice = "Voice 1"
                    {
                        \voiceTwo
                        fs'4
                    }
                >>
                <<
                    \context Voice = "On_Beat_Grace_Container"
                    {
                        \set fontSize = #-4
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        \once \override Beam.grow-direction = #left
                        \slash
                        \voiceOne
                        <
                            \tweak font-size 0
                            \tweak transparent ##t
                            c''
                        >32 * 4/3
                        ^ \markup { \hspace #1 throw (6)}
                        [
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        c''32 * 4/3
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        c''32 * 4/3
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        c''32 * 4/3
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        c''32 * 4/3
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        c''32 * 4/3
                        ]
                    }
                    \context Voice = "Voice 1"
                    {
                        \voiceTwo
                        c''4
                    }
                >>
                <<
                    \context Voice = "On_Beat_Grace_Container"
                    {
                        \set fontSize = #-4
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        \once \override Beam.grow-direction = #right
                        \slash
                        \voiceOne
                        <
                            \tweak font-size 0
                            \tweak transparent ##t
                            gqs''
                        >32 * 4/3
                        ^ \markup { \hspace #1 drop (4)}
                        [
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        gqs''32 * 4/3
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        gqs''32 * 4/3
                        \once \override NoteHead.no-ledgers = ##t
                        \once \override Accidental.transparent = ##t
                        \tweak transparent ##t
                        gqs''32 * 4/3
                        ]
                    }
                    \context Voice = "Voice 1"
                    {
                        \voiceTwo
                        gqs''4
                    }
                >>
            }

    """

    def __init__(
        self,
        number_of_attacks=[4, 5, 6],
        attack_number_forget=False,
        actions=["throw", "drop"],
        action_forget=False,
        boolean_vector=[1],
        vector_forget=False,
        attack_count=-1,
        action_count=-1,
        vector_count=-1,
        name="Gettato Handler",
    ):
        self._attack_count = attack_count
        self._action_count = action_count
        self._vector_count = vector_count
        self.attack_number_forget = attack_number_forget
        self.action_forget = action_forget
        self.vector_forget = vector_forget
        self.attacks = sequence.CyclicList(
            number_of_attacks, self.attack_number_forget, self._attack_count
        )
        self.actions = sequence.CyclicList(
            actions, self.action_forget, self._action_count
        )
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.vector_forget, self._vector_count
        )
        self.name = name

    def __call__(self, selections):
        self.add_gettato(selections)

    def add_gettato(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        vector = self.boolean_vector(r=len(ties))
        for value, tie in zip(vector, ties):
            if value == 1:
                repetitions = self.attacks(r=1)[0]
                pitches = [_ for _ in abjad.get.pitches(tie[0])]
                repeated_pitch = pitches[-1]
                list_ = []
                list_.append(abjad.Chord([repeated_pitch], (1, 32)))
                for _ in range(repetitions - 1):
                    list_.append(abjad.Note(repeated_pitch, (1, 32)))
                sel = abjad.Selection(list_)
                abjad.beam(sel)
                t = abjad.LilyPondLiteral(
                    [
                        r"\once \override NoteHead.no-ledgers = ##t",
                        r"\once \override Accidental.transparent = ##t",
                        r"\tweak transparent ##t",
                    ],
                    format_slot="before",
                )
                for leaf in abjad.select(sel).leaves():
                    abjad.attach(t, leaf)
                a = self.actions(r=1)[0]
                if a == "throw":
                    literal = abjad.LilyPondLiteral(
                        r"\once \override Beam.grow-direction = #left",
                        format_slot="before",
                    )
                    abjad.attach(literal, sel[0])
                    mark = abjad.Markup(
                        fr"\markup {{ \hspace #1 throw ({repetitions})}}",
                        direction=abjad.Up,
                    )
                    abjad.attach(mark, sel[0])
                elif a == "drop":
                    literal = abjad.LilyPondLiteral(
                        r"\once \override Beam.grow-direction = #right",
                        format_slot="before",
                    )
                    abjad.attach(literal, sel[0])
                    mark = abjad.Markup(
                        fr"\markup {{ \hspace #1 drop ({repetitions})}}",
                        direction=abjad.Up,
                    )
                    abjad.attach(mark, sel[0])
                else:
                    pass
                abjad.on_beat_grace_container(
                    sel,
                    tie[:],
                    leaf_duration=(1, 24),
                    do_not_slur=True,
                    do_not_beam=True,
                    font_size=-4,
                )

    def name(self):
        return self.name

    def state(self):
        return dict(
            [
                ("attack_count", self.attacks.state()),
                ("action_count", self.actions.state()),
                ("vector_count", self.boolean_vector.state()),
            ]
        )


class GlissandoHandler(Handler):
    r"""
    Glissando Handler

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.GlissandoHandler(
        ...     line_style="dotted-line",
        ...     boolean_vector=[1],
        ...     forget=False,
        ...     apply_to="runs",
        ... )
        >>> handler(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
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
                - \tweak style #'dotted-line
                \glissando
                c'4
                - \tweak style #'dotted-line
                \glissando
                c'4
                - \tweak style #'dotted-line
                \glissando
                c'4
            }

    """

    def __init__(
        self,
        glissando_style=None,
        line_style=None,
        boolean_vector=[0],
        forget=False,
        apply_to="runs",
        count=-1,
        name="Glissando Handler",
    ):
        self.glissando_style = glissando_style
        self.line_style = f"#'{line_style}"
        self._count = count
        self.forget = forget
        self.apply_to = apply_to
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.forget, self._count
        )
        self.name = name

    def __call__(self, selections):
        self.add_glissando(selections)

    def add_glissando(self, selections):
        if self.apply_to == "runs":
            runs = abjad.select(selections).runs()
            if self.glissando_style == "hide_middle_note_heads":
                if self.line_style is not None:
                    for run in runs:
                        if self.boolean_vector(r=1)[0] == 1:
                            if len(run) > 1:
                                t = abjad.tweak(self.line_style).style
                                abjad.glissando(run[:], t, hide_middle_note_heads=True)
                            else:
                                continue
                        else:
                            continue
                else:
                    for run in runs:
                        if self.boolean_vector(r=1)[0] == 1:
                            if len(run) > 1:
                                abjad.glissando(
                                    run[:],
                                    hide_middle_note_heads=True,
                                    allow_repeats=True,
                                )
                            else:
                                continue
                        else:
                            continue
            elif self.glissando_style == "hide_middle_stems":
                if self.line_style is not None:
                    for run in runs:
                        if self.boolean_vector(r=1)[0] == 1:
                            if len(run) > 1:
                                t = abjad.tweak(self.line_style).style
                                abjad.glissando(
                                    run[:],
                                    t,
                                    hide_middle_note_heads=True,
                                    hide_middle_stems=True,
                                )
                            else:
                                continue
                        else:
                            continue
                else:
                    for run in runs:
                        if self.boolean_vector(r=1)[0] == 1:
                            if len(run) > 1:
                                abjad.glissando(
                                    run[:],
                                    hide_middle_note_heads=True,
                                    hide_middle_stems=True,
                                )
                            else:
                                continue
                        else:
                            continue
            else:
                if self.line_style is not None:
                    for run in runs:
                        if self.boolean_vector(r=1)[0] == 1:
                            if len(run) > 1:
                                t = abjad.tweak(self.line_style).style
                                abjad.glissando(
                                    run[:],
                                    t,
                                    allow_repeats=True,
                                    allow_ties=False,
                                )
                            else:
                                continue
                        else:
                            continue
                else:
                    for run in runs:
                        if self.boolean_vector(r=1)[0] == 1:
                            if len(run) > 1:
                                abjad.glissando(
                                    run[:],
                                    allow_repeats=True,
                                    allow_ties=False,
                                )
                            else:
                                continue
                        else:
                            continue
        else:
            ties = abjad.select(selections).logical_ties(pitched=True)
            values = self.boolean_vector(r=len(ties))
            for value, tie in zip(values, ties):
                if value == 1:
                    abjad.attach(abjad.Glissando(), tie[-1])

    def name(self):
        return self.name

    def state(self):
        return dict([("count", self.boolean_vector.state())])


class GraceHandler(Handler):
    r"""
    Grace Handler

    .. container:: example

        >>> staff = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.GraceHandler(
        ...     boolean_vector=[0, 1, 0, 1],
        ...     gesture_lengths=[1, 2],
        ...     forget=False,
        ... )
        >>> handler(staff[:])
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'4
                \scaleDurations #'(1 . 1) {
                \slashedGrace {
                    c'16
                    s8..
                    s2
                }
                }
                c'4
                c'4
                \scaleDurations #'(1 . 1) {
                \slashedGrace {
                    \slash
                    \override Stem.direction = #UP
                    \override Staff.Stem.stemlet-length = 0
                    c'16
                    [
                    s8..
                    c'16
                    \revert Stem.direction
                    s8..
                    \revert Staff.Stem.stemlet-length
                    s2
                    ]
                }
                }
                c'4
            }

    """

    def __init__(
        self,
        boolean_vector=None,
        gesture_lengths=None,
        forget=True,
        remove_skips=False,
        vector_count=-1,
        gesture_count=-1,
        name="Grace Handler",
    ):
        self.forget = forget
        self.remove_skips = remove_skips
        self._vector_count = vector_count
        self._gesture_count = gesture_count
        self.boolean_vector = boolean_vector
        self.gesture_lengths = gesture_lengths
        self._cyc_boolean_vector = sequence.CyclicList(
            boolean_vector, self.forget, self._vector_count
        )
        self._cyc_gesture_lengths = sequence.CyclicList(
            gesture_lengths, self.forget, self._gesture_count
        )
        self.name = name

    def __call__(self, selections):
        self._add_grace_notes(selections)

    def _add_grace_notes(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        vectors = self._cyc_boolean_vector(r=len(ties))
        if self.boolean_vector is not None:
            for value, tie in zip(vectors, ties):
                if value == 1:
                    grace_list = ""
                    if self.gesture_lengths is not None:
                        grace_length = self._cyc_gesture_lengths(r=1)[0]
                        for x in range(grace_length):
                            s = "c'16"
                            grace_list = grace_list + s
                            grace_list = grace_list + " "
                            if self.remove_skips is False:
                                grace_list = grace_list + "s8.."
                                grace_list = grace_list + " "
                        if self.remove_skips is False:
                            grace_list = grace_list + "s2"
                        grace = abjad.BeforeGraceContainer(
                            grace_list, command=r"\slashedGrace"
                        )
                        if 1 < len(abjad.select(grace).leaves(pitched=True)):
                            abjad.beam(
                                grace,
                                beam_rests=True,
                                beam_lone_notes=True,
                                stemlet_length=0,
                            )
                            literal_slash = abjad.LilyPondLiteral(
                                r"\slash", format_slot="before"
                            )
                            abjad.attach(
                                literal_slash,
                                abjad.select(grace).leaves(pitched=True)[0],
                            )
                            direction_override = abjad.LilyPondLiteral(
                                r"\override Stem.direction = #UP", format_slot="before"
                            )
                            direction_revert = abjad.LilyPondLiteral(
                                r"\revert Stem.direction", format_slot="after"
                            )
                            abjad.attach(
                                direction_override,
                                abjad.select(grace).leaves(pitched=True)[0],
                            )
                            abjad.attach(
                                direction_revert,
                                abjad.select(grace).leaves(pitched=True)[-1],
                            )
                        open_literal = abjad.LilyPondLiteral(
                            r"\scaleDurations #'(1 . 1) {", format_slot="before"
                        )
                        close_literal = abjad.LilyPondLiteral("}", format_slot="after")
                        abjad.attach(open_literal, grace)
                        abjad.attach(close_literal, grace)
                        abjad.attach(grace, tie[0])
                    else:
                        grace = abjad.BeforeGraceContainer(
                            "c'16", command=r"\slashedGrace"
                        )
                        open_literal = abjad.LilyPondLiteral(
                            r"\scaleDurations #'(1 . 1) {", format_slot="before"
                        )
                        close_literal = abjad.LilyPondLiteral("}", format_slot="after")
                        abjad.attach(open_literal, grace)
                        abjad.attach(close_literal, grace)
                        abjad.attach(grace, tie[0])
                else:
                    continue
        else:
            pass

    def name(self):
        return self.name

    def state(self):
        return dict(
            [
                ("vector_count", self._cyc_boolean_vector.state()),
                ("gesture_count", self._cyc_gesture_lengths.state()),
            ]
        )


class IntermittentVoiceHandler(Handler):
    r"""
    IntermittentVoiceHandler

    .. container:: example

        >>> ph_up = evans.PitchHandler([8, 8.5, 9, 9.5, 9, 8.5], forget=False)
        >>> ph_down = evans.PitchHandler([0, 1, 2, 3, 4, 5], forget=False)
        >>> s = abjad.Staff([abjad.Voice("c'4 c'8 c'8 c'8 c'4.", name="Voice1")], name="Staff1")
        >>> ph_down(s)
        >>> h = evans.RhythmHandler(
        ...     rmakers.stack(
        ...         rmakers.talea(
        ...             [1, 2, 3, 4],
        ...             8,
        ...             extra_counts=[1, 0, -1],
        ...         ),
        ...         rmakers.trivialize(abjad.select().tuplets()),
        ...         rmakers.extract_trivial(abjad.select().tuplets()),
        ...         rmakers.rewrite_rest_filled(abjad.select().tuplets()),
        ...         rmakers.rewrite_sustained(abjad.select().tuplets()),
        ...     ),
        ...     forget=False,
        ... )
        ...
        >>> ivh = evans.IntermittentVoiceHandler(h, direction=abjad.Up)
        >>> sel1 = abjad.select(s["Voice1"]).leaf(0)
        >>> sel2 = abjad.select(s["Voice1"]).leaf(2)
        >>> sel3 = abjad.select(s["Voice1"]).leaves().get([3, 4])
        >>> ivh(sel1)
        >>> ivh(sel2)
        >>> ivh(sel3)
        >>> ph_up = evans.PitchHandler([8, 8.5, 9, 9.5, 9, 8.5], forget=False)
        >>> for voice in abjad.select(s).components(abjad.Voice):
        ...     if voice.name == "intermittent_voice":
        ...         ph_up(voice)
        ...
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \context Staff = "Staff1"
            {
                \context Voice = "Voice1"
                {
                    <<
                        \context Voice = "Voice1"
                        {
                            \voiceTwo
                            c'4
                        }
                        \context Voice = "intermittent_voice"
                        {
                            \times 2/3
                            {
                                \voiceOne
                                af'8
                                aqf'4
                            }
                        }
                    >>
                    \oneVoice
                    cs'8
                    <<
                        \context Voice = "Voice1"
                        {
                            \voiceTwo
                            d'8
                        }
                        \context Voice = "intermittent_voice"
                        {
                            \voiceOne
                            a'8
                        }
                    >>
                    \oneVoice
                    <<
                        \context Voice = "Voice1"
                        {
                            \voiceTwo
                            ef'8
                            e'4.
                        }
                        \context Voice = "intermittent_voice"
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3
                            {
                                \voiceOne
                                aqs'4
                                a'8
                            }
                        }
                    >>
                    \oneVoice
                }
            }

    """

    def __init__(
        self,
        rhythm_handler,
        direction=abjad.Up,
    ):
        self.rhythm_handler = rhythm_handler
        self.direction = direction

    def __call__(
        self,
        selections,
    ):
        selections = abjad.select(selections)
        self._add_voice(selections)

    def _add_voice(self, selections):
        if self.direction == abjad.Up:
            literal1 = abjad.LilyPondLiteral(r"\voiceTwo")
            literal2 = abjad.LilyPondLiteral(r"\voiceOne")
        else:
            literal1 = abjad.LilyPondLiteral(r"\voiceOne")
            literal2 = abjad.LilyPondLiteral(r"\voiceTwo")
        closing_literal = abjad.LilyPondLiteral(r"\oneVoice", format_slot="after")
        duration = [abjad.get.duration(selections[:])]
        container = abjad.Container(simultaneous=True)
        original_voice = abjad.Voice(name=self._find_parent(selections))
        intermittent_voice = abjad.Voice(name="intermittent_voice")
        intermittent_voice.append(self._make_components(duration)[:])
        abjad.mutate.wrap(selections, original_voice)
        abjad.mutate.wrap(original_voice, container)
        container.append(intermittent_voice)
        abjad.attach(literal1, abjad.select(original_voice).leaf(0))
        abjad.attach(literal2, abjad.select(intermittent_voice).leaf(0))
        abjad.attach(closing_literal, container)

    def _find_parent(self, selections):
        first_leaf = abjad.select(selections).leaf(0)
        parentage = abjad.get.parentage(first_leaf)
        parent_voice = abjad.select(parentage).components(abjad.Voice)
        return parent_voice[0].name

    def _make_components(self, duration):
        return self.rhythm_handler(duration)


class NoteheadHandler(Handler):
    r"""
    Notehead Handler

    .. container:: example

        >>> staff = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.NoteheadHandler(
        ...     notehead_list=["default", "harmonic", "triangle", "slash"],
        ...     transition=True,
        ...     head_boolean_vector=[1],
        ...     head_vector_forget=False,
        ...     transition_boolean_vector=[0, 1],
        ...     transition_vector_forget=False,
        ...     forget=True,
        ... )
        >>> handler(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                \tweak NoteHead.style #'default
                c'4
                \tweak NoteHead.style #'harmonic
                c'4
                - \tweak arrow-length #2
                - \tweak arrow-width #0.5
                - \tweak bound-details.right.arrow ##t
                - \tweak thickness #2.5
                \glissando
                \tweak NoteHead.style #'triangle
                c'4
                \tweak NoteHead.style #'slash
                c'4
            }


    """

    def __init__(
        self,
        notehead_list=None,
        transition=False,
        head_boolean_vector=[0],
        head_vector_forget=False,
        transition_boolean_vector=[0],
        transition_vector_forget=False,
        forget=True,
        count=-1,
        name="Notehead Handler",
    ):
        self.notehead_list = notehead_list
        self.transition = transition
        self.head_vector_forget = head_vector_forget
        self._head_vector_count = -1
        self.head_boolean_vector = sequence.CyclicList(
            head_boolean_vector, self.head_vector_forget, self._head_vector_count
        )
        self.transition_vector_forget = transition_vector_forget
        self._transition_vector_count = -1
        self.transition_boolean_vector = sequence.CyclicList(
            transition_boolean_vector,
            self.transition_vector_forget,
            self._transition_vector_count,
        )
        self.forget = forget
        self._count = count
        self._cyc_noteheads = sequence.CyclicList(
            notehead_list, self.forget, self._count
        )
        self.name = name

    def __call__(self, selections):
        self.add_noteheads(selections)

    def add_noteheads(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        heads = self._cyc_noteheads(r=len(ties))
        head_vector = self.head_boolean_vector(r=len(ties))
        trans_vector = self.transition_boolean_vector(r=len(ties))
        if self.notehead_list is not None:
            for tie, head, bool in zip(ties, heads, head_vector):
                string = str(r"""\tweak NoteHead.style #'""")
                full_string = string + head
                style = abjad.LilyPondLiteral(full_string, format_slot="opening")
                if bool == 1:
                    for leaf in abjad.select(tie).leaves(pitched=True):
                        abjad.attach(style, leaf)
                else:
                    continue
        if self.transition is True:
            transition_arrow = abjad.LilyPondLiteral(
                r"""
                - \tweak arrow-length #2
                - \tweak arrow-width #0.5
                - \tweak bound-details.right.arrow ##t
                - \tweak thickness #2.5
                \glissando
                """,
                "absolute_after",
            )  # verify that heads are different?
            for tie, bool1, bool2 in zip(ties, head_vector, trans_vector):
                if bool1 == 1:
                    if bool2 == 1:
                        abjad.attach(transition_arrow, tie[-1])
                    else:
                        continue
                else:
                    continue
            for run in abjad.select(selections).runs():
                last_tie = abjad.select(run).logical_ties(pitched=True)[-1]
                abjad.detach(transition_arrow, last_tie[-1])

    def name(self):
        return self.name

    def state(self):
        return dict(
            [
                ("count", self._cyc_noteheads.state()),
                ("head_vector_count", self.head_boolean_vector.state()),
                ("transition_vector_count", self.transition_boolean_vector.state()),
            ]
        )


class OnBeatGraceHandler(Handler):
    r"""
    On Beat Grace Handler

    .. container:: example

        >>> grace_handler = evans.OnBeatGraceHandler(
        ...     number_of_attacks=[
        ...         4,
        ...         3,
        ...         4,
        ...         5,
        ...         6,
        ...         3,
        ...         4,
        ...         3,
        ...         4,
        ...         3,
        ...         4,
        ...         5,
        ...         5,
        ...         3,
        ...         4,
        ...         3,
        ...     ],
        ...     durations=[
        ...         2,
        ...         1,
        ...         1,
        ...         1,
        ...         2,
        ...         1,
        ...         2,
        ...         1,
        ...         1,
        ...     ],
        ...     font_size=-4,
        ...     leaf_duration=(1, 100),
        ...     attack_number_forget=False,
        ...     durations_forget=False,
        ...     boolean_vector=[1],
        ...     vector_forget=False,
        ...     name="On Beat Grace Handler",
        ...     )
        ...
        >>> head_handler = evans.NoteheadHandler(
        ...     ["harmonic"],
        ...     head_boolean_vector=[1],
        ...     forget=False,
        ... )
        ...
        >>> pitch_handler = evans.PitchHandler(
        ...     [
        ...         30,
        ...         32,
        ...         29.5,
        ...         31,
        ...         31.5,
        ...         33,
        ...         30,
        ...         29,
        ...         32.5,
        ...     ],
        ...     forget=False,
        ... )
        ...
        >>> s = abjad.Staff([abjad.Voice("e''4 e''2 e''4", name="Voice1")], name="Staff1")
        >>> grace_handler(abjad.select(s).leaf(1))
        >>> pitch_handler(abjad.select(s).logical_ties(grace=True))
        >>> head_handler(abjad.select(s).logical_ties(grace=True))
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \context Staff = "Staff1"
            {
                \context Voice = "Voice1"
                {
                    e''4
                    <<
                        \context Voice = "On_Beat_Grace_Container"
                        {
                            \set fontSize = #-4
                            \slash
                            \voiceOne
                            \tweak NoteHead.style #'harmonic
                            fs'''8 * 2/25
                            [
                            (
                            \tweak NoteHead.style #'harmonic
                            af'''16 * 4/25
                            \tweak NoteHead.style #'harmonic
                            fqs'''16 * 4/25
                            \tweak NoteHead.style #'harmonic
                            g'''16 * 4/25
                            )
                            ]
                        }
                        \context Voice = "Voice1"
                        {
                            \voiceTwo
                            e''2
                        }
                    >>
                    \oneVoice
                    e''4
                }
            }

    """

    def __init__(
        self,
        number_of_attacks=[4, 5, 6],
        durations=[
            2,
            1,
            1,
            1,
            2,
            1,
            2,
            1,
            1,
        ],
        attack_number_forget=False,
        durations_forget=False,
        font_size=(-4),
        forced_multiplier=None,
        leaf_duration=(1, 28),
        boolean_vector=[1],
        vector_forget=False,
        attack_count=-1,
        durations_count=-1,
        vector_count=-1,
        name="On Beat Grace Handler",
    ):
        self.font_size = font_size
        self.forced_multiplier = forced_multiplier
        self.leaf_duration = leaf_duration
        self._attack_count = attack_count
        self._durations_count = durations_count
        self._vector_count = vector_count
        self.attack_number_forget = attack_number_forget
        self.durations_forget = durations_forget
        self.vector_forget = vector_forget
        self.attacks = sequence.CyclicList(
            number_of_attacks, self.attack_number_forget, self._attack_count
        )
        self.durations = sequence.CyclicList(
            durations, self.durations_forget, self._durations_count
        )
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.vector_forget, self._vector_count
        )
        self.name = name

    def __call__(self, selections):
        self.add_grace(selections)

    def add_grace(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        vector = self.boolean_vector(r=len(ties))
        for value, tie in zip(vector, ties):
            if value == 1:
                repetitions = self.attacks(r=1)[0]
                list_ = []
                durs = self.durations(r=repetitions)
                for _ in durs:
                    list_.append(abjad.Note("c'", (_, 16)))
                sel = abjad.Selection(list_)
                abjad.on_beat_grace_container(
                    sel,
                    tie[:],
                    leaf_duration=self.leaf_duration,
                    do_not_slur=False,
                    do_not_beam=False,
                    font_size=self.font_size,
                )
        if self.forced_multiplier is not None:
            for grace in abjad.select(selections).leaves(grace=True):
                grace.multiplier = abjad.Multiplier(self.forced_multiplier)

    def name(self):
        return self.name

    def state(self):
        return dict(
            [
                ("attack_count", self.attacks.state()),
                ("vector_count", self.boolean_vector.state()),
            ]
        )


class PitchHandler(Handler):
    r"""
    Pitch Handler

    .. container:: example

        >>> import fractions

        >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.PitchHandler(
        ...     pitch_list=[1, 2, 3, 4],
        ...     forget=False,
        ... )
        >>> handler(abjad.select(s).logical_ties())
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \new Staff
            {
                cs'4
                d'4
                ef'4
                e'4
            }

    .. container:: example

        >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.PitchHandler(
        ...     pitch_list=[1, [2, 3], 4],
        ...     forget=False,
        ... )
        >>> handler(abjad.select(s).logical_ties())
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \new Staff
            {
                cs'4
                <d' ef'>4
                e'4
                cs'4
            }

    .. container:: example

        >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.PitchHandler(
        ...     pitch_list=[0, 1, 2.5, 3, 4, 5.5],
        ...     chord_boolean_vector=[0, 1, 1],
        ...     chord_groups=[2, 4],
        ...     forget=False,
        ... )
        >>> handler(abjad.select(s).logical_ties())
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \new Staff
            {
                c'4
                <cs' dqs'>4
                <c' ef' e' fqs'>4
                cs'4
            }

    .. container:: example

        >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.PitchHandler(
        ...     pitch_list=[0, 1, 1, 3, 4, 5.5],
        ...     allow_chord_duplicates=True,
        ...     chord_boolean_vector=[0, 1, 1],
        ...     chord_groups=[2, 4],
        ...     forget=False,
        ... )
        >>> handler(abjad.select(s).logical_ties())
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \new Staff
            {
                c'4
                <cs' cs'>4
                <c' ef' e' fqs'>4
                cs'4
            }

    .. container:: example

        >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.PitchHandler(
        ...     pitch_list=[1, fractions.Fraction(9, 4), 3, 4],
        ...     forget=False,
        ... )
        >>> handler(abjad.select(s).logical_ties())
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...         abjad.Block(name="layout"),
        ...     ],
        ... )
        >>> style = '"dodecaphonic"'
        >>> file.layout_block.items.append(fr"\accidentalStyle {style}")
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \new Staff
            {
                cs'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \one-eighth-sharp-markup
                d'4
                ef'4
                e'4
            }

    .. container:: example

        >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.PitchHandler(
        ...     pitch_list=[1, [fractions.Fraction(4, 3), 4], 5, fractions.Fraction(37, 6)],
        ...     allow_chord_duplicates=True,
        ...     forget=False,
        ... )
        >>> handler(abjad.select(s).logical_ties())
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...         abjad.Block(name="layout"),
        ...     ],
        ... )
        >>> style = '"dodecaphonic"'
        >>> file.layout_block.items.append(fr"\accidentalStyle {style}")
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \new Staff
            {
                cs'4
                <
                    \tweak Accidental.stencil #ly:text-interface::print
                    \tweak Accidental.text \one-third-flat-markup
                    df'
                    e'
                >4
                f'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \five-twelfths-flat-markup
                gf'4
            }

    .. container:: example

        >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.PitchHandler(
        ...      pitch_list=[
        ...         fractions.Fraction(3, 4),
        ...         [
        ...             fractions.Fraction(25, 2),
        ...             fractions.Fraction(4, 3),
        ...         ],
        ...         2,
        ...         fractions.Fraction(23, 4),
        ...     ],
        ...     forget=False,
        ...     allow_chord_duplicates=True,
        ... )
        >>> handler(s)
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...         abjad.Block(name="layout"),
        ...     ],
        ... )
        >>> style = '"dodecaphonic"'
        >>> file.layout_block.items.append(fr"\accidentalStyle {style}")
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \new Staff
            {
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \three-eighths-sharp-markup
                c'4
                <
                    \tweak Accidental.stencil #ly:text-interface::print
                    \tweak Accidental.text \one-third-flat-markup
                    df'
                    cqs''
                >4
                d'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \three-eighths-sharp-markup
                f'4
            }

    .. container:: example

        >>> pitch_set = microtones.PitchSegment([0, Fraction(3, 2), 7, Fraction(19, 4)])
        >>> pitch_set = pitch_set + pitch_set.invert(2).multiply(Fraction(5, 4))
        >>> pitch_set = pitch_set + pitch_set.retrograde().rotate(3).transpose(Fraction(13, 2))
        >>> pitch_set = microtones.PitchSegment([evans.to_nearest_eighth_tone(_) for _ in pitch_set])
        >>> notes = [abjad.Note() for _ in pitch_set]
        >>> staff = abjad.Staff(notes)
        >>> handler = evans.PitchHandler(
        ...     pitch_list=[_ for _ in pitch_set],
        ...     forget=False,
        ... )
        >>> handler(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...         abjad.Block(name="layout"),
        ...     ],
        ... )
        >>> style = '"dodecaphonic"'
        >>> file.layout_block.items.append(fr"\accidentalStyle {style}")
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'4
                dqf'4
                g'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \three-eighths-sharp-markup
                e'4
                f'4
                ef'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \three-eighths-flat-markup
                a4
                b4
                bqs'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \one-eighth-sharp-markup
                b'4
                dqf''4
                af'4
                gqf'4
                fqs'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \three-eighths-sharp-markup
                d'4
                aqs'4
            }

    .. container:: example

        >>> pitch_segment = microtones.PitchSegment([0, Fraction(3, 2), 7, Fraction(19, 4)])
        >>> pitch_segment = pitch_segment + pitch_segment.invert(2).multiply(Fraction(5, 4))
        >>> pitch_segment = pitch_segment + pitch_segment.retrograde().rotate(3).transpose(Fraction(13, 2))
        >>> pitch_segment = microtones.PitchSegment([evans.to_nearest_eighth_tone(_) for _ in pitch_segment])
        >>> notes = [abjad.Note() for _ in pitch_segment]
        >>> staff = abjad.Staff(notes)
        >>> handler = evans.PitchHandler(
        ...     pitch_list=[_ for _ in pitch_set],
        ...     apply_all=True,
        ...     forget=False,
        ... )
        >>> handler(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...         abjad.Block(name="layout"),
        ...     ],
        ... )
        >>> style = '"dodecaphonic"'
        >>> file.layout_block.items.append(fr"\accidentalStyle {style}")
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \abjad-natural-markup
                c'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \one-quarter-flat-markup
                df'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \abjad-natural-markup
                g'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \three-eighths-sharp-markup
                e'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \abjad-natural-markup
                f'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \abjad-flat-markup
                ef'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \three-eighths-flat-markup
                a4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \abjad-natural-markup
                b4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \one-quarter-sharp-markup
                b'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \one-eighth-sharp-markup
                b'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \one-quarter-flat-markup
                df''4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \abjad-flat-markup
                af'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \one-quarter-flat-markup
                gf'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \one-quarter-sharp-markup
                f'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \three-eighths-sharp-markup
                d'4
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \one-quarter-sharp-markup
                a'4
            }

    .. container:: example

        >>> ratio_segment = microtones.RatioSegment([1, Fraction(3, 2), Fraction(5, 4)])
        >>> ratio_segment = ratio_segment + ratio_segment.invert(2).multiply(Fraction(5, 4))
        >>> ratio_segment = ratio_segment + ratio_segment.retrograde().rotate(3).transpose(1)
        >>> notes = [abjad.Note() for _ in ratio_segment]
        >>> staff = abjad.Staff(notes)
        >>> handler = evans.PitchHandler(
        ...     pitch_list=[_ for _ in ratio_segment],
        ...     as_ratios=True,
        ...     forget=False,
        ... )
        >>> handler(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/ekmelos-ji-accidental-markups.ily\'",
        ...         score,
        ...         abjad.Block(name="layout"),
        ...     ],
        ... )
        >>> style = '"dodecaphonic"'
        >>> file.layout_block.items.append(fr"\accidentalStyle {style}")
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \abjad-natural  }
                c'4
                ^ \markup \center-align { +0 }
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \abjad-natural  }
                g'4
                ^ \markup \center-align { +2 }
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \natural-one-syntonic-comma-down  }
                e'4
                ^ \markup \center-align { -14 }
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \natural-one-syntonic-comma-down  }
                e'''4
                ^ \markup \center-align { -14 }
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \natural-one-syntonic-comma-down  }
                a''4
                ^ \markup \center-align { -16 }
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \abjad-natural  }
                c'''4
                ^ \markup \center-align { +0 }
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \abjad-natural  }
                d''4
                ^ \markup \center-align { +4 }
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \natural-one-syntonic-comma-down  }
                e''4
                ^ \markup \center-align { -14 }
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \abjad-natural  }
                c''4
                ^ \markup \center-align { +0 }
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \natural-one-syntonic-comma-down  }
                e'''4
                ^ \markup \center-align { -14 }
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \one-tridecimal-third-tone-down  }
                d'''4
                ^ \markup \center-align { C♯+39 }
                \tweak Accidental.stencil #ly:text-interface::print
                \tweak Accidental.text \markup { \abjad-natural  }
                g'''4
                ^ \markup \center-align { +2 }
            }

    """

    def __init__(  # for apply all add a sharp/flat/none keyword
        self,
        pitch_list=None,
        allow_chord_duplicates=False,
        apply_all=False,
        apply_all_spelling=None,
        as_ratios=False,
        chord_boolean_vector=[0],
        chord_groups=None,
        forget=True,
        to_ties=False,
        pitch_count=-1,
        state=None,
        chord_boolean_count=-1,
        chord_groups_count=-1,
        name="Pitch Handler",
    ):
        self.pitch_list = pitch_list
        self.allow_chord_duplicates = allow_chord_duplicates
        self.apply_all = apply_all
        self.apply_all_spelling = apply_all_spelling
        self.as_ratios = as_ratios
        self.chord_boolean_vector = chord_boolean_vector
        self.chord_groups = chord_groups
        self.forget = forget
        self.to_ties = to_ties
        self.name = name
        self._state = state
        self._pitch_count = pitch_count
        self._chord_boolean_count = chord_boolean_count
        self._chord_groups_count = chord_groups_count
        if self._state is not None:
            self._pitch_count = state["pitch_count"]
            self._chord_boolean_count = state["chord_boolean_count"]
            self._chord_groups_count = state["chord_groups_count"]
        self._cyc_pitches = sequence.CyclicList(
            self.pitch_list,
            self.forget,
            self._pitch_count,
        )
        self._cyc_chord_boolean_vector = sequence.CyclicList(
            self.chord_boolean_vector,
            self.forget,
            self._chord_boolean_count,
        )
        self._cyc_chord_groups = sequence.CyclicList(
            self.chord_groups,
            self.forget,
            self._chord_groups_count,
        )

    def __call__(self, selections):
        if self.to_ties is True:
            for tie in selections:
                self._apply_pitches(tie)
        else:
            self._apply_pitches(selections)

    def _collect_pitches_durations_leaves(self, logical_ties):
        pitches, durations, leaves = [[], [], []]
        ties_ = logical_ties
        if self.chord_groups is not None:
            pitches_ = []
            bools = self._cyc_chord_boolean_vector(r=len(ties_))
            for tie, bool in zip(ties_, bools):
                if 0 < bool:
                    group_size = self._cyc_chord_groups(r=1)[0]
                    pitches_.append(self._cyc_pitches(r=group_size))
                else:
                    pitches_.append(self._cyc_pitches(r=1)[0])
        else:
            pitches_ = self._cyc_pitches(r=len(ties_))
        for tie, pitch in zip(ties_, pitches_):
            for leaf in tie:
                if isinstance(pitch, list):
                    if self.allow_chord_duplicates is False:
                        pitch = list(set(pitch))
                pitches.append(pitch)
                durations.append(leaf.written_duration)
                leaves.append(leaf)
        return pitches, durations, leaves

    def _apply_pitches(self, selections):  # get apply all to handler chords
        if self.as_ratios is True:
            self.apply_all = True
        leaf_maker = abjad.LeafMaker()
        old_ties = [tie for tie in abjad.iterate.logical_ties(selections, pitched=True)]
        if len(old_ties) > 0:
            collect = self._collect_pitches_durations_leaves(old_ties)
            pitches, durations, old_leaves = collect
            microtonal_indices_to_pitch = dict()
            for i, _ in enumerate(pitches):
                if isinstance(_, list):
                    _.sort()
                    nested_indices_to_pitch = dict()
                    for i_, sub_ in enumerate(_):
                        if self.apply_all is False:
                            if isinstance(sub_, str):
                                val = abjad.NumberedPitch(sub_).number
                            else:
                                val = sub_
                            if 0 < val % quicktions.Fraction(1, 2):
                                nested_indices_to_pitch[str(i_)] = sub_
                                pitches[i][i_] = 0
                                microtonal_indices_to_pitch[
                                    str(i)
                                ] = nested_indices_to_pitch
                        else:
                            nested_indices_to_pitch[str(i_)] = sub_
                            pitches[i][i_] = 0
                            microtonal_indices_to_pitch[
                                str(i)
                            ] = nested_indices_to_pitch
                else:
                    if self.apply_all is False:
                        if isinstance(_, str):
                            val = abjad.NumberedPitch(_).number
                        else:
                            val = _
                        if val is not None:
                            if 0 < val % quicktions.Fraction(1, 2):
                                microtonal_indices_to_pitch[str(i)] = _
                                pitches[i] = 0
                        else:
                            pitches[i] = None
                    else:
                        microtonal_indices_to_pitch[str(i)] = _
                        pitches[i] = 0
            for pitch_index, pitch_value in enumerate(
                pitches
            ):  # find way to add cent when 1/4 is false
                if isinstance(pitch_value, JIPitch):
                    pitches[pitch_index] = pitch_value.pitch
            if self.apply_all is False:
                new_leaves = [leaf for leaf in leaf_maker(pitches, durations)]
            else:
                new_leaves = old_leaves
                for i, pair in enumerate(
                    zip(new_leaves, microtonal_indices_to_pitch.values())
                ):
                    leaf, pitch = pair
                    if isinstance(pitch, dict):
                        replacement_chord = abjad.Chord()
                        replacement_chord.written_duration = leaf.written_duration
                        replacement_chord.note_heads = abjad.NoteHeadList(
                            [abjad.NoteHead(leaf.written_pitch) for _ in pair[1]]
                        )
                        indicators = abjad.get.indicators(leaf)
                        before_grace = abjad.get.before_grace_container(leaf)
                        multiplier = leaf.multiplier
                        for indicator in indicators:
                            abjad.attach(indicator, replacement_chord)
                        if before_grace is not None:
                            abjad.attach(before_grace, replacement_chord)
                        if multiplier is not None:
                            replacement_chord.multiplier = multiplier
                        abjad.mutate.replace(leaf, replacement_chord)
                        new_leaves[i] = replacement_chord
            for index in microtonal_indices_to_pitch:
                for leaf in abjad.select(new_leaves[int(index)]).leaves():
                    leaf_annotation_pitch = [_.hertz for _ in abjad.get.pitches(leaf)]
                    leaf_annotation_ratio = []
                    if isinstance(leaf, abjad.Chord):
                        marks = []
                        heads = leaf.note_heads
                        for sub_index in microtonal_indices_to_pitch[index]:
                            head = heads[int(sub_index)]
                            if self.as_ratios is False:
                                microtones.apply_alteration(
                                    head,
                                    microtonal_indices_to_pitch[index][sub_index],
                                    spell=self.apply_all_spelling,
                                )
                            else:
                                ratio = microtonal_indices_to_pitch[index][sub_index]
                                factors = []
                                for _ in microtones.ji._prime_factors(
                                    quicktions.Fraction(ratio).numerator
                                ):
                                    factors.append(_)
                                for _ in microtones.ji._prime_factors(
                                    quicktions.Fraction(ratio).denominator
                                ):
                                    factors.append(_)
                                over_23 = 0
                                if 0 < len(factors):
                                    over_23 = max(factors)
                                if 23 < over_23:
                                    marks.append(return_cent_markup(head, ratio))
                                    tune_to_ratio(head, ratio)
                                    leaf_annotation_ratio.append(ratio)
                                else:
                                    marks.append(
                                        microtones.return_cent_deviation_markup(
                                            ratio, head.written_pitch
                                        )
                                    )
                                    microtones.tune_to_ratio(head, ratio)
                                    leaf_annotation_ratio.append(ratio)
                        if 0 < len(marks):
                            marks_strings = r""
                            for marks_string in marks[::-1]:
                                marks_strings += fr"{marks_string.contents[0][24:-1]}"
                            column = abjad.Markup(
                                fr"\center-column {{ {marks_strings} }}",
                            )
                            m = abjad.Markup(
                                fr"\markup \center-align {column}",
                                direction=abjad.Up,
                            )
                            if leaf is abjad.get.logical_tie(leaf).head:
                                abjad.attach(m, leaf)
                    else:
                        if self.as_ratios is False:
                            temp = microtonal_indices_to_pitch[index]
                            if isinstance(temp, dict):
                                temp = microtonal_indices_to_pitch[index]["1"]
                            microtones.apply_alteration(
                                leaf.note_head,
                                temp,
                                spell=self.apply_all_spelling,
                            )
                        else:
                            temp = microtonal_indices_to_pitch[index]
                            if isinstance(temp, dict):
                                temp = microtonal_indices_to_pitch[index]["1"]
                            factors = []
                            for _ in microtones.ji._prime_factors(
                                quicktions.Fraction(temp).numerator
                            ):
                                factors.append(_)
                            for _ in microtones.ji._prime_factors(
                                quicktions.Fraction(temp).denominator
                            ):
                                factors.append(_)
                            over_23 = 0
                            if 0 < len(factors):
                                over_23 = max(factors)
                            if 23 < over_23:
                                m = return_cent_markup(leaf.note_head, temp)
                                tune_to_ratio(leaf.note_head, temp)
                                leaf_annotation_ratio.append(temp)
                            else:
                                m = microtones.return_cent_deviation_markup(
                                    temp,
                                    leaf.note_head.written_pitch,
                                )
                                microtones.tune_to_ratio(
                                    leaf.note_head,
                                    temp,
                                )
                                leaf_annotation_ratio.append(temp)
                            if leaf is abjad.get.logical_tie(leaf).head:
                                abjad.attach(m, leaf)
                    annotation_string = [
                        f"{x} * {y}"
                        for x, y in zip(leaf_annotation_pitch, leaf_annotation_ratio)
                    ]
                    abjad.annotate(leaf, "ratio", annotation_string)
            if self.apply_all is False:
                for old_leaf, new_leaf in zip(old_leaves, new_leaves):
                    indicators = abjad.get.indicators(old_leaf)
                    before_grace = abjad.get.before_grace_container(old_leaf)
                    multiplier = old_leaf.multiplier
                    for indicator in indicators:
                        abjad.attach(indicator, new_leaf)
                    if before_grace is not None:
                        abjad.attach(before_grace, new_leaf)
                    if multiplier is not None:
                        new_leaf.multiplier = multiplier
                    abjad.mutate.replace(old_leaf, new_leaf)

    def make_persistent_copy(self, state_dict):
        copied_handler = type(self)(
            pitch_list=self.pitch_list,
            allow_chord_duplicates=self.allow_chord_duplicates,
            apply_all=self.apply_all,
            apply_all_spelling=self.apply_all_spelling,
            as_ratios=self.as_ratios,
            chord_boolean_vector=self.chord_boolean_vector,
            chord_groups=self.chord_groups,
            forget=self.forget,
            to_ties=self.to_ties,
            state=state_dict,
            name=self.name,
        )
        return copied_handler

    def name(self):
        return self.name

    def state(self):
        return dict(
            [
                ("pitch_count", self._cyc_pitches.state()),
                ("chord_boolean_count", self._cyc_chord_boolean_vector.state()),
                ("chord_groups_count", self._cyc_chord_groups.state()),
            ]
        )


class RhythmHandler(Handler):
    r"""
    Rhythm Handler

    .. container:: example

        >>> spans = abjad.TimespanList(
        ...     [
        ...         abjad.Timespan(0, 1),
        ...         abjad.Timespan(1, 2),
        ...     ]
        ... )
        >>> maker = rmakers.stack(
        ...     rmakers.NoteRhythmMaker()
        ... )
        >>> handler = evans.RhythmHandler(rmaker=maker)
        >>> staff = abjad.Staff()
        >>> for span in spans:
        ...     selections = maker([span.duration])
        ...     staff.extend(selections)
        ...
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'1
                c'1
            }

    """

    def __init__(self, rmaker, forget=True, state=None, name="Rhythm Handler"):
        self.rmaker = rmaker
        self.forget = forget
        self._input_state = state
        self.state = self.rmaker.state
        self.name = name

    def __call__(self, durations):
        return self._make_music(durations)

    def _make_basic_rhythm(self, durations):
        if self.forget is False:
            if self._input_state is not None:
                self.state = self._input_state
                selections = self.rmaker(durations, previous_state=self.state)
                self.state = self.rmaker.state
                self._input_state = None
            else:
                selections = self.rmaker(durations, previous_state=self.rmaker.state)
                self.state = self.rmaker.state
        else:
            selections = self.rmaker(durations)
        return selections

    def _make_music(self, durations):
        selections = self._make_basic_rhythm(durations)
        return selections

    def make_persistent_copy(self, state_dict):
        new_handler = type(self)(
            rmaker=self.rmaker,
            forget=self.forget,
            state=state_dict,
            name=self.name,
        )
        return new_handler

    def name(self):
        return self.name

    def return_state(self):
        return dict([("state", self.rmaker.state)])


class ScordaturaHandler(Handler):
    r"""
    Scordatura Handler

    .. container:: example

        >>> handler = evans.ScordaturaHandler()
        >>> staff = abjad.Staff("a,,4 a,,4 a,,4 a,,4 a,,4 a,,4 a,,4 a,,4")
        >>> abjad.attach(abjad.Clef("bass"), staff[0])
        >>> handler(staff[1:-1])
        >>> block = abjad.Block(name="score")
        >>> block.items.append(staff)
        >>> path = "/Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily"
        >>> file = abjad.LilyPondFile(items=[f"\\include {path}", block])
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                \clef "bass"
                a,,4
                c,4
                - \abjad-dashed-line-with-hook
                - \tweak bound-details.left.text \markup \concat { IV \hspace #0.5 }
                - \tweak staff-padding 1
                \startTextSpan
                c,4
                c,4
                c,4
                c,4
                c,4
                a,,4
                \stopTextSpan
            }

    """

    def __init__(
        self,
        string_number="IV",
        default_pitch="c,",
        new_pitch="a,,",
        name="ScordaturaHandler",
        padding=1,
    ):
        self.string_number = string_number
        self.default_pitch = default_pitch
        self.new_pitch = new_pitch
        self.name = name
        self.padding = padding

    def __call__(self, selections):
        leaves = abjad.select(selections).leaves()
        interval = self._find_transposition()
        abjad.mutate.transpose(leaves, interval)
        start, stop = self._make_spanner()
        abjad.attach(start, leaves[0])
        abjad.attach(stop, abjad.get.leaf(leaves[-1], 1))

    def _find_transposition(self):
        interval = abjad.NamedInterval.from_pitch_carriers(
            self.new_pitch, self.default_pitch
        )
        return interval

    def _make_spanner(self):
        start_spanner = abjad.StartTextSpan(
            left_text=abjad.Markup(self.string_number),
            style="dashed-line-with-hook",
        )
        abjad.tweak(start_spanner).staff_padding = self.padding
        stop_spanner = abjad.StopTextSpan()
        return start_spanner, stop_spanner

    def name(self):
        return self.name

    def state(self):
        return f"STATE not maintained for {type(self)}"


# add style option for \slurDotted and \slurDashed and \slurSolid
class SlurHandler(Handler):
    r"""
    Slur Handler

    .. container:: example

        >>> staff = abjad.Staff("c'4 c'4 c'4 c'4")
        >>> handler = evans.SlurHandler()
        >>> handler(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
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
                (
                c'4
                c'4
                c'4
                )
            }

    """

    def __init__(
        self,
        apply_slur_to="runs",
        boolean_vector=[1],
        forget=False,
        count=-1,
        name="Slur Handler",
    ):
        self.apply_slur_to = apply_slur_to
        self._count = count
        self.forget = forget
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.forget, self._count
        )
        self.name = name

    def __call__(self, selections):
        self.add_slurs(selections)

    def add_slurs(self, selections):
        if self.apply_slur_to == "selections":
            if len(abjad.select(selections).logical_ties(pitched=True)) < 2:
                pass
            if self.boolean_vector(r=1)[0] == 1:
                abjad.slur(selections[:])
            else:
                pass
        elif self.apply_slur_to == "runs":
            for run in abjad.select(selections).runs():
                if len(abjad.select(run).logical_ties()) < 2:
                    continue
                if self.boolean_vector(r=1)[0] == 1:
                    abjad.slur(run[:])
                else:
                    continue
        else:
            pass

    def name(self):
        return self.name

    def state(self):
        return dict([("count", self.boolean_vector.state())])


class TempoSpannerHandler(Handler):
    r"""
    Tempo Spanner Handler

    ..  container:: example

        >>> s = abjad.Staff("s4 s4 s4 s4")
        >>> handler = evans.TempoSpannerHandler(
        ...     tempo_list=[(3, 0, 1, "87"), (3, 0, 1, "95")],
        ...     boolean_vector=[1],
        ...     padding=4,
        ...     staff_padding=2,
        ...     forget=False,
        ... )
        >>> handler(s[:-1])
        >>> score = abjad.Score([s])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         "\include \'Users/gregoryevans/evans/lilypond/evans-spanners.ily\'",
        ...         score,
        ...     ],
        ... )
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(s))
            \new Staff
            {
                s4
                - \abjad-dashed-line-with-arrow
                - \baca-metronome-mark-spanner-left-text 3 0 1 "87"
                - \tweak padding #4
                - \tweak staff-padding #2
                - \tweak font-size #2
                \bacaStartTextSpanMM
                s4
                s4
                \bacaStopTextSpanMM
                - \abjad-invisible-line
                - \baca-metronome-mark-spanner-left-text 3 0 1 "95"
                - \tweak padding #4
                - \tweak staff-padding #2
                - \tweak font-size #2
                \bacaStartTextSpanMM
                s4
                \bacaStopTextSpanMM
            }

    """

    def __init__(
        self,
        tempo_list=[(3, 0, 1, "87"), (3, 0, 1, "95")],
        boolean_vector=[1],
        padding=4,
        staff_padding=2,
        font_size=2,
        forget=False,
        tempo_count=-1,
        bool_count=-1,
        name="Tempo Spanner Handler",
    ):
        self._tempo_count = tempo_count
        self._bool_count = bool_count
        self.padding = padding
        self.forget = forget
        self.staff_padding = staff_padding
        self.font_size = font_size
        self.tempo_list = sequence.CyclicList(
            tempo_list, self.forget, self._tempo_count
        )
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.forget, self._bool_count
        )
        self.name = name

    def __call__(self, selections):
        self.add_spanner(selections)

    def add_spanner(self, selections):
        ties = abjad.select(selections).logical_ties()
        value = self.boolean_vector(r=1)[0]
        if value == 1:
            start_temp = self.tempo_list(r=1)[0]
            stop_temp = self.tempo_list(r=1)[0]
            start_literal = abjad.LilyPondLiteral(
                [
                    r"- \abjad-dashed-line-with-arrow",
                    r"- \baca-metronome-mark-spanner-left-text "
                    + f"{start_temp[0]} {start_temp[1]} {start_temp[2]}"
                    + f' "{start_temp[3]}"',
                    r"- \tweak padding #" + f"{self.padding}",
                    r"- \tweak staff-padding #" + f"{self.staff_padding}",
                    r"- \tweak font-size #" + f"{self.font_size}",
                    r"\bacaStartTextSpanMM",
                ],
                format_slot="after",
            )
            stop_literal = abjad.LilyPondLiteral(
                [
                    r"\bacaStopTextSpanMM",
                    r"- \abjad-invisible-line",
                    r"- \baca-metronome-mark-spanner-left-text "
                    + f'{stop_temp[0]} {stop_temp[1]} {stop_temp[2]} "{stop_temp[3]}"',
                    r"- \tweak padding #" + f"{self.padding}",
                    r"- \tweak staff-padding #" + f"{self.staff_padding}",
                    r"- \tweak font-size #" + f"{self.font_size}",
                    r"\bacaStartTextSpanMM",
                ],
                format_slot="after",
            )
            stopper = abjad.LilyPondLiteral(r"\bacaStopTextSpanMM", format_slot="after")
            abjad.attach(start_literal, abjad.select(ties).leaves()[0])
            abjad.attach(stop_literal, abjad.select(ties).leaves()[-1])
            abjad.attach(stopper, abjad.get.leaf(abjad.select(ties).leaves()[-1], 1))

    def name(self):
        return self.name

    def state(self):
        return dict([("count", self.boolean_vector.state())])


class TextSpanHandler(Handler):
    r"""
    Text Span Handler

    .. container:: example

        >>> staff = abjad.Staff("c'4 c'4 c'4 r4")
        >>> handler = evans.TextSpanHandler(
        ...     span_one_positions=["pont.", "tast."],
        ...     span_one_style="dashed-line",
        ...     span_one_padding=1.5,
        ...     attach_span_one_to="bounds",
        ... )
        >>> handler(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'4
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.padding 1.4
                - \tweak staff-padding #1.5
                \startTextSpanOne
                c'4
                c'4
                \stopTextSpanOne
                - \abjad-dashed-line-with-hook
                - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                - \tweak bound-details.right.padding 3
                - \tweak staff-padding #1.5
                \startTextSpanOne
                r4
                \stopTextSpanOne
            }

    """

    def __init__(
        self,
        span_one_positions=None,
        span_one_style=None,
        span_one_padding=None,
        attach_span_one_to=None,
        span_two_positions=None,
        span_two_style=None,
        span_two_padding=None,
        attach_span_two_to=None,
        span_three_positions=None,
        span_three_style=None,
        span_three_padding=None,
        attach_span_three_to=None,
        hooks=True,
        forget=True,
        count_1=-1,
        count_2=-1,
        count_3=-1,
        name="TextSpan Handler",
    ):
        self.span_one_positions = span_one_positions
        self.span_one_style = span_one_style
        self.span_one_padding = span_one_padding
        self.attach_span_one_to = attach_span_one_to
        self.span_two_positions = span_two_positions
        self.span_two_style = span_two_style
        self.span_two_padding = span_two_padding
        self.attach_span_two_to = attach_span_two_to
        self.span_three_positions = span_three_positions
        self.span_three_style = span_three_style
        self.span_three_padding = span_three_padding
        self.attach_span_three_to = attach_span_three_to
        self.hooks = hooks
        self.forget = forget
        self._count_1 = count_1
        self._count_2 = count_2
        self._count_3 = count_3
        self._cyc_span_one_positions = sequence.CyclicList(
            span_one_positions, self.forget, self._count_1
        )
        self._cyc_span_two_positions = sequence.CyclicList(
            span_two_positions, self.forget, self._count_2
        )
        self._cyc_span_three_positions = sequence.CyclicList(
            span_three_positions, self.forget, self._count_3
        )
        self.name = name

    def __call__(self, selections):
        self._add_spanners(selections)

    def _add_spanners(self, selections):
        if self.attach_span_one_to == "bounds":
            self._apply_position_and_span_to_bounds(
                selections,
                self._cyc_span_one_positions,
                self.span_one_style,
                r"One",
                self.span_one_padding,
            )
        elif self.attach_span_one_to == "leaves":
            self._apply_position_and_span_to_leaves(
                selections,
                self._cyc_span_one_positions,
                self.span_one_style,
                r"One",
                self.span_one_padding,
            )
        elif self.attach_span_one_to == "left":
            self._apply_position_and_span_to_left(
                selections,
                self._cyc_span_one_positions,
                self.span_one_style,
                r"One",
                self.span_one_padding,
            )
        else:
            pass
        if self.attach_span_two_to == "bounds":
            self._apply_position_and_span_to_bounds(
                selections,
                self._cyc_span_two_positions,
                self.span_two_style,
                r"Two",
                self.span_two_padding,
            )
        elif self.attach_span_two_to == "leaves":
            self._apply_position_and_span_to_leaves(
                selections,
                self._cyc_span_two_positions,
                self.span_two_style,
                r"Two",
                self.span_two_padding,
            )
        elif self.attach_span_two_to == "left":
            self._apply_position_and_span_to_left(
                selections,
                self._cyc_span_two_positions,
                self.span_two_style,
                r"Two",
                self.span_two_padding,
            )
        else:
            pass
        if self.attach_span_three_to == "bounds":
            self._apply_position_and_span_to_bounds(
                selections,
                self._cyc_span_three_positions,
                self.span_three_style,
                r"Three",
                self.span_three_padding,
            )
        elif self.attach_span_three_to == "leaves":
            self._apply_position_and_span_to_leaves(
                selections,
                self._cyc_span_three_positions,
                self.span_three_style,
                r"Three",
                self.span_three_padding,
            )
        elif self.attach_span_three_to == "left":
            self._apply_position_and_span_to_left(
                selections,
                self._cyc_span_three_positions,
                self.span_three_style,
                r"Three",
                self.span_three_padding,
            )
        else:
            pass

    def _apply_empty_spanner(self, selections, span_command):
        first_leaf = abjad.select(selections).leaves()[0]
        stop_indicator = abjad.StopTextSpan(command=r"\stopTextSpan" + span_command)
        abjad.attach(stop_indicator, first_leaf)

    def _apply_position_and_span_to_bounds(
        self, selections, positions, style, span_command, span_padding
    ):
        for run in abjad.select(selections).runs():
            if len(run) < 2:
                start_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(
                        fr"\upright {positions(r=1)[0]}",
                    ),
                    style=style + "-with-hook",
                    command=r"\startTextSpan" + span_command,
                )
                abjad.attach(
                    abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                    abjad.get.leaf(run[-1], 1),
                )
                abjad.attach(start_span, run[0])
                abjad.tweak(start_span).staff_padding = f"#{span_padding}"
            else:
                start_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(
                        fr"\upright {positions(r=1)[0]}",
                    ),
                    style=style + "-with-arrow",
                    command=r"\startTextSpan" + span_command,
                    right_padding=1.4,
                )
                if self.hooks is True:
                    stop_span = abjad.StartTextSpan(
                        left_text=abjad.Markup(
                            rf"\upright {positions(r=1)[0]}",
                        ),
                        style=style + "-with-hook",
                        command=r"\startTextSpan" + span_command,
                        right_padding=3,
                    )
                else:
                    stop_span = abjad.StartTextSpan(
                        left_text=abjad.Markup(
                            fr"\upright {positions(r=1)[0]}",
                        ),
                        style="invisible-line",
                        command=r"\startTextSpan" + span_command,
                        right_padding=3,
                    )
                abjad.attach(start_span, run[0])
                abjad.attach(
                    abjad.StopTextSpan(command=r"\stopTextSpan" + span_command), run[-1]
                )
                abjad.attach(stop_span, run[-1])
                abjad.attach(
                    abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                    abjad.get.leaf(run[-1], 1),
                )
                abjad.tweak(start_span).staff_padding = f"#{span_padding}"
                abjad.tweak(stop_span).staff_padding = f"#{span_padding}"

    def _apply_position_and_span_to_leaves(
        self, selections, positions, style, span_command, span_padding
    ):
        for run in abjad.select(selections).runs():
            ties = abjad.select(run).logical_ties(pitched=True)
            following_leaf = abjad.get.leaf(ties[-1][-1], 1)
            distance = len(ties) + 1
            start_strings = [positions(r=1)[0] for _ in range(distance)]
            for i, start_string in enumerate(start_strings[:-1]):
                if all(start_string[_].isdigit() for _ in (0, -1)):
                    if quicktions.Fraction(
                        int(start_strings[i][0]), int(start_strings[i][-1])
                    ) > quicktions.Fraction(
                        int(start_strings[i + 1][0]), int(start_strings[i + 1][-1])
                    ):
                        start_strings[
                            i
                        ] = fr"""\center-column {{ \center-align \vcenter \musicglyph \evans-upbow \vspace #0.2 \upright \fraction {start_string[0]} {start_string[-1]} }}"""
                    elif quicktions.Fraction(
                        int(start_strings[i][0]), int(start_strings[i][-1])
                    ) < quicktions.Fraction(
                        int(start_strings[i + 1][0]), int(start_strings[i + 1][-1])
                    ):
                        start_strings[
                            i
                        ] = fr"""\center-column {{ \center-align \vcenter \musicglyph \evans-downbow \vspace #0.2 \upright \fraction {start_string[0]} {start_string[-1]} }}"""
                    else:
                        start_strings[
                            i
                        ] = fr"""\center-column {{ \center-align \vcenter \upright \fraction {start_string[0]} {start_string[-1]} }}"""
                else:
                    start_strings[
                        i
                    ] = fr"""\center-column {{ \upright \center-align \vcenter {start_string} }}"""
            start_indicators = [
                abjad.StartTextSpan(
                    left_text=abjad.Markup(f"{start_string}"),
                    style=fr"{style}-with-arrow",
                    command=r"\startTextSpan" + span_command,
                    right_padding=1.4,
                )
                for start_string in start_strings
            ]
            final_indicator = abjad.StartTextSpan()
            if all(start_string[-1].isdigit() for _ in (0, -1)):
                final_indicator = abjad.StartTextSpan(
                    left_text=abjad.Markup(
                        fr"""\center-column {{ \center-align \vcenter \upright \fraction {start_strings[-1][0]} {start_strings[-1][-1]} }}""",
                    ),
                    style=r"invisible-line",
                    command=r"\startTextSpan" + span_command,
                    right_padding=3,
                )
            else:
                final_indicator = abjad.StartTextSpan(
                    left_text=abjad.Markup(
                        fr"""\center-column {{ \center-align \upright \vcenter {start_strings[-1]} }}""",
                    ),
                    style=r"invisible-line",
                    command=r"\startTextSpan" + span_command,
                    right_padding=3,
                )
            for indicator in start_indicators:
                abjad.tweak(indicator).staff_padding = f"#{span_padding}"
            abjad.tweak(final_indicator).staff_padding = f"#{span_padding}"
            abjad.attach(start_indicators[0], ties[0][0])
            for pair in zip(ties[1:], start_indicators[1:]):
                tie, start_indicator = pair
                abjad.attach(
                    abjad.StopTextSpan(command=r"\stopTextSpan" + span_command), tie[0]
                )
                abjad.attach(start_indicator, tie[0])
            abjad.attach(
                abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                following_leaf,
            )
            abjad.attach(final_indicator, following_leaf)
            abjad.attach(
                abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                abjad.get.leaf(following_leaf, 1),
            )

    def _apply_position_and_span_to_left(
        self, selections, positions, style, span_command, span_padding
    ):
        runs = abjad.select(selections).runs()
        start_strings = [positions(r=1)[0] for _ in runs]
        start_indicators = [
            abjad.StartTextSpan(
                left_text=abjad.Markup(fr"\upright {start_string}"),
                style=fr"{style}-with-hook",
                command=r"\startTextSpan" + span_command,
                right_padding=3,
            )
            for start_string in start_strings
        ]
        for indicator in start_indicators:
            abjad.tweak(indicator).staff_padding = f"#{span_padding}"
        for i, pair in enumerate(zip(runs, start_indicators)):
            run, start_indicator = pair
            abjad.attach(start_indicator, run[0])
            abjad.attach(
                abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                abjad.get.leaf(run[-1], 1),
            )

    def name(self):
        return self.name

    def state(self):
        return dict(
            [
                ("count_1", self._cyc_span_one_positions.state()),
                ("count_2", self._cyc_span_two_positions.state()),
                ("count_3", self._cyc_span_three_positions.state()),
            ]
        )


class TranspositionHandler(Handler):
    def __init__(
        self,
        transposition_list=("+P8",),
        forget=False,
        count=-1,
        name="Transposition Handler",
    ):
        self.transposition_list = transposition_list
        self.forget = forget
        self._count = count
        self.name = name
        self.cyc_transpositions = sequence.CyclicList(
            transposition_list, self.forget, self._count
        )

    def __call__(self, selections):
        self.transpose_leaves(selections)

    def transpose_leaves(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        transpositions = self.cyc_transpositions(r=len(ties))
        for tie, interval in zip(ties, transpositions):
            abjad.mutate.transpose(tie, interval)


class TrillHandler(Handler):
    r"""
    Trill Handler

    .. container:: example

        >>> staff = abjad.Staff("<c' d'>4 c'4 c'4 <c' d'>4 c'4 c'4 c'4 c'4 ")
        >>> handler = evans.TrillHandler(boolean_vector=[0, 1], forget=False)
        >>> handler(staff)
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[
        ...         "#(set-default-paper-size \"a4\" \'portrait)",
        ...         r"#(set-global-staff-size 16)",
        ...         "\\include \'Users/gregoryevans/abjad/docs/source/_stylesheets/abjad.ily\'",
        ...         score,
        ...     ],
        ... )
        ...
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                <c' d'>4
                c'4
                c'4
                \pitchedTrill
                c'4
                \startTrillSpan d'
                c'4
                \stopTrillSpan
                c'4
                c'4
                c'4
            }

    """

    def __init__(
        self,
        boolean_vector=[0],
        forget=False,
        count=-1,
        name="Trill Handler",
        only_chords=False,
    ):
        self.forget = forget
        self._count = count
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.forget, self._count
        )
        self.name = name
        self.only_chords = only_chords

    def __call__(self, selections):
        self._apply_trills(selections)

    def _apply_trills(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        if self.only_chords:
            chords = abjad.select(selections).components(abjad.Chord)
            ties = abjad.select(chords).logical_ties(pitched=True)
        vector = self.boolean_vector
        for tie, bool in zip(ties, vector(r=len(ties))):
            if bool == 1:
                if all(
                    isinstance(leaf, abjad.Chord) for leaf in abjad.iterate.leaves(tie)
                ):
                    last_leaf = tie[-1]
                    next_leaf = abjad.get.leaf(last_leaf, 1)
                    if next_leaf is not None:
                        abjad.attach(abjad.StopTrillSpan(), next_leaf)
                    else:
                        continue

                    old_chord = tie[0]
                    base_pitch = old_chord.written_pitches[0]
                    trill_pitch = old_chord.written_pitches[-1]
                    new_leaf = abjad.Note(base_pitch, old_chord.written_duration)
                    indicators = abjad.get.indicators(old_chord)
                    for indicator in indicators:
                        abjad.attach(indicator, new_leaf)

                    parent = abjad.get.parentage(old_chord).parent
                    parent[parent.index(old_chord)] = new_leaf
                    trill_start = abjad.StartTrillSpan(pitch=trill_pitch)
                    abjad.attach(trill_start, new_leaf)

                    tail = abjad.select(tie).leaves()[1:]
                    for leaf in tail:
                        new_tail = abjad.Note(base_pitch, leaf.written_duration)
                        indicators = abjad.get.indicators(leaf)
                        for indicator in indicators:
                            abjad.attach(indicator, new_tail)
                        before_grace = abjad.get.before_grace_container(leaf)
                        if before_grace is not None:
                            abjad.attach(before_grace, new_tail)
                        parent = abjad.get.parentage(leaf).parent
                        parent[parent.index(leaf)] = new_tail

    def name(self):
        return self.name

    def state(self):
        return dict([("count", self.boolean_vector.state())])
