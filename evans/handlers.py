import statistics

import abjad
import quicktions
from abjadext import microtones

from . import sequence


class Handler(object):
    def __str__(self):
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)


class ArticulationHandler(Handler):
    r"""
    >>> staff = abjad.Staff("c'4 c'4 c'4 r4 c'4 c'4 c'4 c'4 c'4")
    >>> art_lst = ["staccato", "tenuto", "staccatissimo", "open", "halfopen", "stopped", "portato", "tremolo"]
    >>> handler = evans.ArticulationHandler(
    ...     articulation_list=art_lst,
    ...     articulation_boolean_vector=[0],
    ...     vector_continuous=True,
    ...     continuous=True,
    ... )
    >>> handler(staff)
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
        articulation_boolean_vector=[0],
        vector_continuous=True,
        continuous=False,
        count=-1,
        vector_count=-1,
        name="Articulation Handler",
    ):
        self.articulation_list = articulation_list
        self.vector_continuous = vector_continuous
        self.continuous = continuous
        self._count = count
        self._vector_count = vector_count
        self.articulation_boolean_vector = sequence.CyclicList(
            articulation_boolean_vector, self.vector_continuous, self._vector_count
        )
        self._cyc_articulations = sequence.CyclicList(
            lst=articulation_list, continuous=self.continuous, count=self._count
        )
        self.name = name

    def __call__(self, selections):
        self.add_articulations(selections)

    def add_articulations(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        articulations = self._cyc_articulations(r=len(ties))
        vector = self.articulation_boolean_vector(r=len(ties))
        for tie, articulation, bool in zip(ties, articulations, vector):
            if bool == 0:
                if self.articulation_list is not None:
                    if articulation == "tremolo":
                        for leaf in tie:
                            if abjad.inspect(leaf).duration() <= abjad.Duration(1, 32):
                                continue
                            else:
                                abjad.attach(abjad.StemTremolo(32), leaf)
                    elif articulation == "default":
                        continue
                    else:
                        abjad.attach(abjad.Articulation(articulation), tie[0])
            else:
                continue

    def identifiers(self):
        return f"""articulation list:\n{self.articulation_list}\narticulation boolean vector\n{self.articulation_boolean_vector}\nvector continuous\n{self.vector_continuous}\ncontinuous\n{self.continuous},"""

    def name(self):
        return self.name

    def state(self):
        return abjad.OrderedDict(
            [
                ("count", self._cyc_articulations.state()),
                ("vector_count", self.articulation_boolean_vector.state()),
            ]
        )


class BendHandler(Handler):
    r"""
    >>> staff = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = evans.BendHandler(
    ...     bend_amounts=[1, 1.5],
    ...     bend_continuous=True,
    ...     boolean_vector=[1, 1, 0, 1],
    ...     vector_continuous=True,
    ... )
    >>> handler(staff)
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
        bend_amounts=[1],
        bend_continuous=True,
        boolean_vector=[0],
        vector_continuous=True,
        bend_count=-1,
        vector_count=-1,
        name="Bend Handler",
    ):
        self._bend_count = bend_count
        self._vector_count = vector_count
        self.bend_continuous = bend_continuous
        self.vector_continuous = vector_continuous
        self.bend_amounts = sequence.CyclicList(
            bend_amounts, self.bend_continuous, self._bend_count
        )
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.vector_continuous, self._vector_count
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
        return abjad.OrderedDict(
            [
                ("bend_count", self.bend_amounts.state()),
                ("vector_count", self.boolean_vector.state()),
            ]
        )


class BisbigliandoHandler(Handler):
    r"""
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
    ... continuous=True,
    ... )
    >>> handler(s[:-1])
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
        fingering_list=[None],
        boolean_vector=[1],
        padding=2,
        staff_padding=2,
        right_padding=2,
        continuous=True,
        bis_count=-1,
        bool_count=-1,
        name="Bisbigliando Handler",
    ):
        self._bis_count = bis_count
        self._bool_count = bool_count
        self.continuous = continuous
        self.padding = padding
        self.staff_padding = staff_padding
        self.right_padding = right_padding
        self.fingering_list = sequence.CyclicList(
            fingering_list, self.continuous, self._bis_count
        )
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.continuous, self._bool_count
        )
        self.name = name

    def __call__(self, selections):
        self.add_spanner(selections)

    def add_spanner(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        values = self.boolean_vector(r=len(ties))
        for value, tie in zip(values, ties):
            if value == 1:
                fingering = self.fingering_list(r=1)[0]
                if fingering is None:
                    start_literal = abjad.LilyPondLiteral(
                        [
                            r"""- \tweak padding""" + f""" #{self.padding}""",
                            r"""- \tweak staff-padding"""
                            + f""" #{self.staff_padding}""",
                            r"""- \tweak bound-details.right.padding"""
                            + f""" #{self.right_padding}""",
                            r"""- \tweak bound-details.left.text""",
                            r"""\markup{ \raise #1 \teeny \musicglyph #"scripts.halfopenvertical" }""",
                            r"""\startTrillSpan""",
                        ],
                        format_slot="after",
                    )
                    stop_literal = abjad.LilyPondLiteral(
                        r"\stopTrillSpan", format_slot="after"
                    )
                    abjad.attach(start_literal, tie[0])
                    abjad.attach(stop_literal, abjad.inspect(tie[-1]).leaf(1))
                else:
                    start_literal_pre = abjad.LilyPondLiteral(
                        [
                            r"""- \tweak padding""" + f""" #{self.padding}""",
                            r"""- \tweak staff-padding"""
                            + f""" #{self.staff_padding}""",
                            r"""- \tweak bound-details.right.padding"""
                            + f""" #{self.right_padding}""",
                            r"""- \tweak bound-details.left.text""",
                        ],
                        format_slot="after",
                    )
                    start_literal = abjad.LilyPondLiteral(
                        fingering, format_slot="after"
                    )
                    start_literal_post = abjad.LilyPondLiteral(
                        [r"""\startTrillSpan"""], format_slot="after"
                    )
                    stop_literal = abjad.LilyPondLiteral(
                        r"\stopTrillSpan", format_slot="after"
                    )
                    abjad.attach(start_literal_pre, tie[0])
                    abjad.attach(start_literal, tie[0])
                    abjad.attach(start_literal_post, tie[0])
                    abjad.attach(stop_literal, abjad.inspect(tie[-1]).leaf(1))

    def name(self):
        return self.name

    def state(self):
        return abjad.OrderedDict([("count", self.boolean_vector.state())])


# add shelf for ottava to ensure that no notes in the bracket are illegible
class ClefHandler(Handler):
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

    def __call__(self, voice):
        self._add_clefs(voice)
        self._add_ottavas(voice)

    def _extended_range_clefs(self, clef):
        clef_groups_up = {
            "bass": ("bass", "tenorvarC", "treble"),  # "treble^8", "treble^15"),
            "tenor": ("tenorvarC", "treble"),  # "treble^8", "treble^15"),
            "alto": ("varC", "treble"),  # "treble^8", "treble^15"),
            "treble": ("treble",),  # "treble^8", "treble^15"),
        }
        clef_groups_down = {
            "bass": ("bass", "bass_8", "bass_15"),
            "tenor": ("tenorvarC", "bass", "bass_8"),
            "alto": ("varC", "bass", "bass_8"),
            "treble": ("treble", "treble_8", "bass"),
        }
        if self.extend_in_direction == "down":
            return clef_groups_down[clef]
        else:
            return clef_groups_up[clef]

    def _extended_range_ottavas(self, clef):
        default_clef_shelves = {
            "bass": (-28, 6),
            "tenor": (-10, 12),
            "tenorvarC": (-10, 12),
            "alto": (-12, 18),
            "varC": (-12, 18),
            "treble": (-5, 24),
            "treble^8": (7, 36),
            "treble^15": (19, 48),
        }
        return default_clef_shelves[clef]

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
                    for pitch in abjad.inspect(tie[0]).pitches():
                        pitches.append(pitch.number)
                    pitch = statistics.mean(pitches)
                    value = None
                    for count, allowed_clef in enumerate(allowable_clefs):
                        if clef_list[-1] == abjad.Clef(allowed_clef):
                            value = count
                        else:
                            continue
                    active_clef_in_list = clef_list[-1]
                    active_clef_in_list_shelf = self._extended_range_ottavas(
                        active_clef_in_list.name
                    )
                    if pitch > active_clef_in_list_shelf[1]:
                        test_value = value + 1
                        if test_value < len(allowable_clefs):
                            temp_clef = allowable_clefs[test_value]
                            clef = abjad.Clef(temp_clef)
                            if clef == clef_list[-1]:
                                continue
                            elif (
                                abjad.inspect(tie[0]).indicator(abjad.Clef) is not None
                            ):
                                abjad.detach(
                                    abjad.inspect(tie[0]).indicator(abjad.Clef), tie[0]
                                )
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
                                    elif (
                                        abjad.inspect(tie[0]).indicator(abjad.Clef)
                                        is not None
                                    ):
                                        abjad.detach(
                                            abjad.inspect(tie[0]).indicator(abjad.Clef),
                                            tie[0],
                                        )
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
                            elif (
                                abjad.inspect(tie[0]).indicator(abjad.Clef) is not None
                            ):
                                abjad.detach(
                                    abjad.inspect(tie[0]).indicator(abjad.Clef), tie[0]
                                )
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
                                    elif (
                                        abjad.inspect(tie[0]).indicator(abjad.Clef)
                                        is not None
                                    ):
                                        abjad.detach(
                                            abjad.inspect(tie[0]).indicator(abjad.Clef),
                                            tie[0],
                                        )
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
                                elif (
                                    abjad.inspect(tie[0]).indicator(abjad.Clef)
                                    is not None
                                ):
                                    abjad.detach(
                                        abjad.inspect(tie[0]).indicator(abjad.Clef),
                                        tie[0],
                                    )
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
                if abjad.inspect(first_leaf).indicator(abjad.Clef) is not None:
                    abjad.detach(
                        abjad.inspect(first_leaf).indicator(abjad.Clef), first_leaf
                    )
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
                        for pitch in abjad.inspect(tie[0]).pitches():
                            if pitch < shelf[0]:
                                start = abjad.Ottava(n=-1)
                                stop = abjad.Ottava(n=0)
                                if (
                                    abjad.inspect(tie[0]).indicator(abjad.Ottava)
                                    is not None
                                ):
                                    abjad.detach(
                                        abjad.inspect(tie[0]).indicator(abjad.Ottava),
                                        tie[0],
                                    )
                                    abjad.attach(stop, abjad.inspect(tie[-1]).leaf(1))
                                else:
                                    abjad.attach(start, tie[0])
                                    abjad.attach(stop, abjad.inspect(tie[-1]).leaf(1))
                    else:
                        for pitch in abjad.inspect(tie[0]).pitches():
                            if pitch > shelf[1]:
                                start = abjad.Ottava(n=1)
                                stop = abjad.Ottava(n=0)
                                if (
                                    abjad.inspect(tie[0]).indicator(abjad.Ottava)
                                    is not None
                                ):
                                    abjad.detach(
                                        abjad.inspect(tie[0]).indicator(abjad.Ottava),
                                        tie[0],
                                    )
                                    abjad.attach(stop, abjad.inspect(tie[-1]).leaf(1))
                                else:
                                    abjad.attach(start, tie[0])
                                    abjad.attach(stop, abjad.inspect(tie[-1]).leaf(1))
                else:
                    shelf = self._extended_range_ottavas(current_clef)
                    if self.extend_in_direction == "down":
                        for pitch in abjad.inspect(tie[0]).pitches():
                            if pitch < shelf[0]:
                                start = abjad.Ottava(n=-1)
                                stop = abjad.Ottava(n=0)
                                if (
                                    abjad.inspect(tie[0]).indicator(abjad.Ottava)
                                    is not None
                                ):
                                    abjad.detach(
                                        abjad.inspect(tie[0]).indicator(abjad.Ottava),
                                        tie[0],
                                    )
                                    abjad.attach(stop, abjad.inspect(tie[-1]).leaf(1))
                                else:
                                    abjad.attach(start, tie[0])
                                    abjad.attach(stop, abjad.inspect(tie[-1]).leaf(1))
                    else:
                        for pitch in abjad.inspect(tie[0]).pitches():
                            if pitch > shelf[1]:
                                start = abjad.Ottava(n=1)
                                stop = abjad.Ottava(n=0)
                                if (
                                    abjad.inspect(tie[0]).indicator(abjad.Ottava)
                                    is not None
                                ):
                                    abjad.detach(
                                        abjad.inspect(tie[0]).indicator(abjad.Ottava),
                                        tie[0],
                                    )
                                    abjad.attach(stop, abjad.inspect(tie[-1]).leaf(1))
                                else:
                                    abjad.attach(start, tie[0])
                                    abjad.attach(stop, abjad.inspect(tie[-1]).leaf(1))
        else:
            pass


# incorporate spanner anchors
class DynamicHandler(Handler):
    r"""
    >>> staff = abjad.Staff("c'4 d'4 e'4 f'4 r4 g'4 r2")
    >>> handler = evans.DynamicHandler(
    ...     dynamic_list=['f', 'niente', 'p', 'mf'],
    ...     flare_boolean_vector=[0, 0, 0, 1],
    ...     flare_continuous=True,
    ...     hold_first_boolean_vector=[1, 0, 0,],
    ...     hold_first_continuous=True,
    ...     hold_last_boolean_vector=[0, 1],
    ...     hold_last_continuous=True,
    ...     effort_boolean_vector=[1, 0],
    ...     effort_continuous=True,
    ...     continuous=True,
    ... )
    >>> first_group = staff[0:3]
    >>> second_group = staff[2:]
    >>> handler(first_group)
    >>> handler(second_group)
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
        flare_continuous=True,
        hold_first_boolean_vector=[0],
        hold_first_continuous=True,
        hold_last_boolean_vector=[0],
        hold_last_continuous=True,
        effort_boolean_vector=[0],
        effort_continuous=True,
        with_constante_hairpins=True,
        continuous=True,
        count_1=-1,
        count_2=-1,
        count_3=-1,
        count_4=-1,
        count_5=-1,
        name="Dynamic Handler",
    ):
        self.dynamic_list = dynamic_list
        self.flare_boolean_vector = flare_boolean_vector
        self.flare_continuous = flare_continuous
        self.hold_first_boolean_vector = hold_first_boolean_vector
        self.hold_first_continuous = hold_first_continuous
        self.hold_last_boolean_vector = hold_last_boolean_vector
        self.hold_last_continuous = hold_last_continuous
        self.effort_boolean_vector = effort_boolean_vector
        self.effort_continuous = effort_continuous
        self.with_constante_hairpins = with_constante_hairpins
        self.continuous = continuous
        self._count_1 = count_1
        self._count_2 = count_2
        self._count_3 = count_3
        self._count_4 = count_4
        self._count_5 = count_5
        self._cyc_dynamics = sequence.CyclicList(
            dynamic_list, self.continuous, self._count_1
        )
        self._cyc_flare_boolean_vector = sequence.CyclicList(
            flare_boolean_vector, self.flare_continuous, self._count_2
        )
        self._cyc_hold_first_boolean_vector = sequence.CyclicList(
            hold_first_boolean_vector, self.hold_first_continuous, self._count_3
        )
        self._cyc_hold_last_boolean_vector = sequence.CyclicList(
            hold_last_boolean_vector, self.hold_last_continuous, self._count_4
        )
        self._cyc_effort_boolean_vector = sequence.CyclicList(
            effort_boolean_vector, self.effort_continuous, self._count_5
        )
        self.name = name

    def __call__(self, selections):
        self._apply_dynamics(selections)

    def _calculate_hairpin(self, start, stop, flared=0):
        if isinstance(start, str):
            start = abjad.Dynamic(start)
        elif isinstance(start, int):
            start = abjad.Dynamic(abjad.Dynamic.dynamic_ordinal_to_dynamic_name(start))
        else:
            pass
        if isinstance(stop, str):
            stop = abjad.Dynamic(stop)
        elif isinstance(stop, int):
            stop = abjad.Dynamic(abjad.Dynamic.dynamic_ordinal_to_dynamic_name(stop))
        else:
            pass
        if flared == 1:
            if start.ordinal < stop.ordinal:
                if start.name == "niente":
                    start = abjad.Dynamic(
                        "niente", hide=True
                    )  # carry these through instead?
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
                    if abjad.inspect(run[0]).has_indicator(abjad.Dynamic):
                        current_dynamic = abjad.inspect(run[0]).indicator(abjad.Dynamic)
                        start = abjad.Dynamic(current_dynamic, hide=True)
                        stop = self._cyc_dynamics(r=1)[0]
                    else:
                        items = self._cyc_dynamics(r=2)
                        start = items[0]
                        stop = items[1]
                    hairpin = abjad.StartHairpin(
                        self._calculate_hairpin(
                            start, stop, flared=self._cyc_flare_boolean_vector(r=1)[0]
                        )
                    )
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
                                abjad.attach(
                                    abjad.StopHairpin(), abjad.inspect(run[-1]).leaf(1)
                                )
                        else:
                            if isinstance(abjad.inspect(run[-1]).leaf(1), abjad.Rest):
                                stop = abjad.Dynamic(
                                    stop, command=r"\!", leak=True
                                )  # attach to anchor
                            else:
                                pass
                    else:
                        if isinstance(abjad.inspect(run[-1]).leaf(1), abjad.Rest):
                            stop = abjad.Dynamic(stop, leak=True)  # attach to anchor
                        else:
                            pass
                    if abjad.inspect(run[0]).has_indicator(abjad.Dynamic):
                        abjad.attach(abjad.StopHairpin(), run[0])
                        abjad.attach(hairpin, run[0])
                        abjad.attach(stop, run[-1])
                    else:
                        abjad.hairpin([start, hairpin, stop], run)
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
                        next_leaf = abjad.inspect(run[-1]).leaf(1)
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
                        hairpin = abjad.StartHairpin(
                            self._calculate_hairpin(
                                start,
                                stop,
                                flared=self._cyc_flare_boolean_vector(r=1)[0],
                            )
                        )
                        abjad.hairpin([start, hairpin, stop], run)
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
                next_leaf = abjad.inspect(run[-1]).leaf(1)
                abjad.attach(start, run[0])
                if self.with_constante_hairpins is True:
                    abjad.attach(hairpin, run[0])
                    if isinstance(next_leaf, (abjad.Rest, abjad.MultimeasureRest)):
                        abjad.attach(stopper, next_leaf)
                else:
                    pass
        self._remove_niente(selections)

    def _remove_niente(self, selections):
        for leaf in abjad.select(selections).leaves():
            for dynamic in abjad.inspect(leaf).indicators(abjad.Dynamic):
                if dynamic.name == "niente":
                    if dynamic.command == r"\!":
                        abjad.detach(dynamic, leaf)
                        abjad.attach(
                            abjad.Dynamic(dynamic, command=r"\!", leak=True),
                            leaf,  # attach to anchor
                        )  # maybe just continue instead of replacing?
                    elif dynamic.leak is True:
                        abjad.detach(dynamic, leaf)
                        abjad.attach(
                            abjad.Dynamic(dynamic, command=r"\!", leak=True),
                            leaf,  # attach to anchor
                        )
                    else:
                        abjad.detach(dynamic, leaf)
                        abjad.attach(abjad.Dynamic(dynamic, hide=True), leaf)
                else:
                    continue

    def name(self):
        return self.name

    def state(self):
        return abjad.OrderedDict(
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
    >>> staff = abjad.Voice("c'4 fs'4 c''4 gqs''4", name="Voice 1")
    >>> handler = evans.GettatoHandler(
    ...     number_of_attacks=[4, 5, 6],
    ...     actions=["throw", "drop"],
    ... )
    >>> handler(staff)
    >>> print(abjad.lilypond(staff))
    \context Voice = "Voice 1"
    {
        <<
            \context Voice = "On_Beat_Grace_Container"
            {
                \set fontSize = #-4 %! abjad.on_beat_grace_container(1)
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                \once \override Beam.grow-direction = #left
                \slash %! abjad.on_beat_grace_container(2)
                \voiceOne %! abjad.on_beat_grace_container(3)
                <
                    \tweak font-size #0
                    \tweak transparent ##t
                    c'
                >32 * 4/3
                ^ \markup {
                    \hspace
                        #1
                    throw
                    (4)
                    }
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
                \voiceTwo %! abjad.on_beat_grace_container(4)
                c'4
            }
        >>
        <<
            \context Voice = "On_Beat_Grace_Container"
            {
                \set fontSize = #-4 %! abjad.on_beat_grace_container(1)
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                \once \override Beam.grow-direction = #right
                \slash %! abjad.on_beat_grace_container(2)
                \voiceOne %! abjad.on_beat_grace_container(3)
                <
                    \tweak font-size #0
                    \tweak transparent ##t
                    fs'
                >32 * 4/3
                ^ \markup {
                    \hspace
                        #1
                    drop
                    (5)
                    }
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
                \voiceTwo %! abjad.on_beat_grace_container(4)
                fs'4
            }
        >>
        <<
            \context Voice = "On_Beat_Grace_Container"
            {
                \set fontSize = #-4 %! abjad.on_beat_grace_container(1)
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                \once \override Beam.grow-direction = #left
                \slash %! abjad.on_beat_grace_container(2)
                \voiceOne %! abjad.on_beat_grace_container(3)
                <
                    \tweak font-size #0
                    \tweak transparent ##t
                    c''
                >32 * 4/3
                ^ \markup {
                    \hspace
                        #1
                    throw
                    (6)
                    }
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
                \voiceTwo %! abjad.on_beat_grace_container(4)
                c''4
            }
        >>
        <<
            \context Voice = "On_Beat_Grace_Container"
            {
                \set fontSize = #-4 %! abjad.on_beat_grace_container(1)
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                \once \override Beam.grow-direction = #right
                \slash %! abjad.on_beat_grace_container(2)
                \voiceOne %! abjad.on_beat_grace_container(3)
                <
                    \tweak font-size #0
                    \tweak transparent ##t
                    gqs''
                >32 * 4/3
                ^ \markup {
                    \hspace
                        #1
                    drop
                    (4)
                    }
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
                \voiceTwo %! abjad.on_beat_grace_container(4)
                gqs''4
            }
        >>
    }

    """

    def __init__(
        self,
        number_of_attacks=[4, 5, 6],
        attack_number_continuous=True,
        actions=["throw", "drop"],
        action_continuous=True,
        boolean_vector=[1],
        vector_continuous=True,
        attack_count=-1,
        action_count=-1,
        vector_count=-1,
        name="Gettato Handler",
    ):
        self._attack_count = attack_count
        self._action_count = action_count
        self._vector_count = vector_count
        self.attack_number_continuous = attack_number_continuous
        self.action_continuous = action_continuous
        self.vector_continuous = vector_continuous
        self.attacks = sequence.CyclicList(
            number_of_attacks, self.attack_number_continuous, self._attack_count
        )
        self.actions = sequence.CyclicList(
            actions, self.action_continuous, self._action_count
        )
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.vector_continuous, self._vector_count
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
                pitches = [_ for _ in abjad.inspect(tie[0]).pitches()]
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
                        fr"\hspace #1 throw ({repetitions})", direction=abjad.Up
                    )
                    abjad.attach(mark, sel[0])
                elif a == "drop":
                    literal = abjad.LilyPondLiteral(
                        r"\once \override Beam.grow-direction = #right",
                        format_slot="before",
                    )
                    abjad.attach(literal, sel[0])
                    mark = abjad.Markup(
                        fr"\hspace#1 drop ({repetitions})", direction=abjad.Up
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
        return abjad.OrderedDict(
            [
                ("attack_count", self.attacks.state()),
                ("action_count", self.actions.state()),
                ("vector_count", self.boolean_vector.state()),
            ]
        )


class GlissandoHandler(Handler):
    r"""
    >>> staff = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = evans.GlissandoHandler(
    ...     line_style="dotted-line",
    ...     boolean_vector=[1],
    ...     continuous=True,
    ...     apply_to="runs",
    ... )
    >>> handler(staff)
    >>> print(abjad.lilypond(staff))
    \new Staff
    {
        c'4
        - \tweak style #'dotted-line %! abjad.glissando(7)
        \glissando                   %! abjad.glissando(7)
        c'4
        - \tweak style #'dotted-line %! abjad.glissando(7)
        \glissando                   %! abjad.glissando(7)
        c'4
        - \tweak style #'dotted-line %! abjad.glissando(7)
        \glissando                   %! abjad.glissando(7)
        c'4
    }

    """

    def __init__(
        self,
        glissando_style=None,
        line_style=None,
        boolean_vector=[0],
        continuous=True,
        apply_to="runs",
        count=-1,
        name="Glissando Handler",
    ):
        self.glissando_style = glissando_style
        self.line_style = line_style
        self._count = count
        self.continuous = continuous
        self.apply_to = apply_to
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.continuous, self._count
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
                                abjad.glissando(
                                    run[:],
                                    abjad.tweak(self.line_style).style,
                                    hide_middle_note_heads=True,
                                )
                            else:
                                continue
                        else:
                            continue
                else:
                    for run in runs:
                        if self.boolean_vector(r=1)[0] == 1:
                            if len(run) > 1:
                                abjad.glissando(run[:], hide_middle_note_heads=True)
                            else:
                                continue
                        else:
                            continue
            elif self.glissando_style == "hide_middle_stems":
                if self.line_style is not None:
                    for run in runs:
                        if self.boolean_vector(r=1)[0] == 1:
                            if len(run) > 1:
                                abjad.glissando(
                                    run[:],
                                    abjad.tweak(self.line_style).style,
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
                                abjad.glissando(
                                    run[:],
                                    abjad.tweak(self.line_style).style,
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
                                    run[:], allow_repeats=True, allow_ties=False
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
        return abjad.OrderedDict([("count", self.boolean_vector.state())])


class GraceHandler(Handler):
    r"""
    >>> staff = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = GraceHandler(
    ...     boolean_vector=[0, 1, 0, 1],
    ...     gesture_lengths=[1, 2],
    ...     continuous=True,
    ... )
    >>> handler(staff[:])
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
        continuous=False,
        vector_count=-1,
        gesture_count=-1,
        name="Grace Handler",
    ):
        self.continuous = continuous
        self._vector_count = vector_count
        self._gesture_count = gesture_count
        self.boolean_vector = boolean_vector
        self.gesture_lengths = gesture_lengths
        self._cyc_boolean_vector = sequence.CyclicList(
            boolean_vector, self.continuous, self._vector_count
        )
        self._cyc_gesture_lengths = sequence.CyclicList(
            gesture_lengths, self.continuous, self._gesture_count
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
                            grace_list = grace_list + "s8.."
                            grace_list = grace_list + " "
                        grace_list = grace_list + "s2"
                        grace = abjad.BeforeGraceContainer(
                            grace_list, command=r"\slashedGrace"
                        )
                        if len(abjad.select(grace).leaves(pitched=True)) > 1:
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
        return abjad.OrderedDict(
            [
                ("vector_count", self._cyc_boolean_vector.state()),
                ("gesture_count", self._cyc_gesture_lengths.state()),
            ]
        )


class NoteheadHandler(Handler):
    r"""
    >>> staff = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = evans.NoteheadHandler(
    ...     notehead_list=["default", "harmonic", "triangle", "slash"],
    ...     transition=True,
    ...     head_boolean_vector=[1],
    ...     head_vector_continuous=True,
    ...     transition_boolean_vector=[0, 1],
    ...     transition_vector_continuous=True,
    ...     continuous=False,
    ... )
    >>> handler(staff)
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
        head_vector_continuous=True,
        transition_boolean_vector=[0],
        transition_vector_continuous=True,
        continuous=False,
        count=-1,
        name="Notehead Handler",
    ):
        self.notehead_list = notehead_list
        self.transition = transition
        self.head_vector_continuous = head_vector_continuous
        self._head_vector_count = -1
        self.head_boolean_vector = sequence.CyclicList(
            head_boolean_vector, self.head_vector_continuous, self._head_vector_count
        )
        self.transition_vector_continuous = transition_vector_continuous
        self._transition_vector_count = -1
        self.transition_boolean_vector = sequence.CyclicList(
            transition_boolean_vector,
            self.transition_vector_continuous,
            self._transition_vector_count,
        )
        self.continuous = continuous
        self._count = count
        self._cyc_noteheads = sequence.CyclicList(
            notehead_list, self.continuous, self._count
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
                style = abjad.LilyPondLiteral(full_string, format_slot="before")
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
            )
            for tie, bool1, bool2 in zip(
                ties, head_vector, trans_vector
            ):  # verify that heads are different?
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
        return abjad.OrderedDict(
            [
                ("count", self._cyc_noteheads.state()),
                ("head_vector_count", self.head_boolean_vector.state()),
                ("transition_vector_count", self.transition_boolean_vector.state()),
            ]
        )


class PitchHandler(Handler):
    r"""
    >>> import fractions

    >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = evans.PitchHandler(
    ...     pitch_list=[1, 2, 3, 4],
    ...     continuous=True,
    ... )
    >>> handler(abjad.select(s).logical_ties())
    >>> print(abjad.lilypond(s))
    \new Staff
    {
        cs'4
        d'4
        ef'4
        e'4
    }

    >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = evans.PitchHandler(
    ...     pitch_list=[1, [2, 3], 4],
    ...     continuous=True,
    ... )
    >>> handler(abjad.select(s).logical_ties())
    >>> print(abjad.lilypond(s))
    \new Staff
    {
        cs'4
        <d' ef'>4
        e'4
        cs'4
    }

    >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = evans.PitchHandler(
    ...     pitch_list=[0, 1, 2.5, 3, 4, 5.5],
    ...     chord_boolean_vector=[0, 1, 1],
    ...     chord_groups=[2, 4],
    ...     continuous=True,
    ... )
    >>> handler(abjad.select(s).logical_ties())
    >>> print(abjad.lilypond(s))
    \new Staff
    {
        c'4
        <cs' dqs'>4
        <c' ef' e' fqs'>4
        cs'4
    }

    >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = evans.PitchHandler(
    ...     pitch_list=[0, 1, 1, 3, 4, 5.5],
    ...     allow_chord_duplicates=True,
    ...     chord_boolean_vector=[0, 1, 1],
    ...     chord_groups=[2, 4],
    ...     continuous=True,
    ... )
    >>> handler(abjad.select(s).logical_ties())
    >>> print(abjad.lilypond(s))
    \new Staff
    {
        c'4
        <cs' cs'>4
        <c' ef' e' fqs'>4
        cs'4
    }

    >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = evans.PitchHandler(
    ...     pitch_list=[1, fractions.Fraction(9, 4), 3, 4],
    ...     continuous=True,
    ... )
    >>> handler(abjad.select(s).logical_ties())
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

    >>> s = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = evans.PitchHandler(
    ...     pitch_list=[1, [fractions.Fraction(4, 3), 4], 5, fractions.Fraction(37, 6)],
    ...     allow_chord_duplicates=True,
    ...     continuous=True,
    ... )
    >>> handler(abjad.select(s).logical_ties())
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
    ...     continuous=True,
    ...     allow_chord_duplicates=True,
    ... )
    >>> handler(s)
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

    >>> pitch_set = microtones.PitchSegment([0, Fraction(3, 2), 7, Fraction(19, 4)])
    >>> pitch_set = pitch_set + pitch_set.invert(2).multiply(Fraction(5, 4))
    >>> pitch_set = pitch_set + pitch_set.retrograde().rotate(3).transpose(Fraction(13, 2))
    >>> pitch_set = microtones.PitchSegment([evans.to_nearest_eighth_tone(_) for _ in pitch_set])
    >>> notes = [abjad.Note() for _ in pitch_set]
    >>> staff = abjad.Staff(notes)
    >>> handler = evans.PitchHandler(
    ...     pitch_list=[_ for _ in pitch_set],
    ...     continuous=True,
    ... )
    >>> handler(staff)
    >>> file = abjad.LilyPondFile.new(
    ...     staff,
    ...     includes=[
    ...         "/Users/evansdsg2/abjad-ext-microtones/abjadext/microtones/lilypond/default-edo-accidental-markups.ily"
    ...     ],
    ... )
    >>> style = '"dodecaphonic"'
    >>> file.layout_block.items.append(fr"\accidentalStyle {style}")
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

    >>> pitch_set = microtones.PitchSegment([0, Fraction(3, 2), 7, Fraction(19, 4)])
    >>> pitch_set = pitch_set + pitch_set.invert(2).multiply(Fraction(5, 4))
    >>> pitch_set = pitch_set + pitch_set.retrograde().rotate(3).transpose(Fraction(13, 2))
    >>> pitch_set = microtones.PitchSegment([evans.to_nearest_eighth_tone(_) for _ in pitch_set])
    >>> notes = [abjad.Note() for _ in pitch_set]
    >>> staff = abjad.Staff(notes)
    >>> handler = evans.PitchHandler(
    ...     pitch_list=[_ for _ in pitch_set],
    ...     apply_all=True,
    ...     continuous=True,
    ... )
    >>> handler(staff)
    >>> file = abjad.LilyPondFile.new(
    ...     staff,
    ...     includes=[
    ...         "/Users/evansdsg2/abjad-ext-microtones/abjadext/microtones/lilypond/default-edo-accidental-markups.ily"
    ...     ],
    ... )
    >>> style = '"dodecaphonic"'
    >>> file.layout_block.items.append(fr"\accidentalStyle {style}")
    >>> print(abjad.lilypond(staff))
    \new Staff
    {
        \tweak Accidental.stencil #ly:text-interface::print
        \tweak Accidental.text \natural-markup
        c'4
        \tweak Accidental.stencil #ly:text-interface::print
        \tweak Accidental.text \one-quarter-flat-markup
        df'4
        \tweak Accidental.stencil #ly:text-interface::print
        \tweak Accidental.text \natural-markup
        g'4
        \tweak Accidental.stencil #ly:text-interface::print
        \tweak Accidental.text \three-eighths-sharp-markup
        e'4
        \tweak Accidental.stencil #ly:text-interface::print
        \tweak Accidental.text \natural-markup
        f'4
        \tweak Accidental.stencil #ly:text-interface::print
        \tweak Accidental.text \flat-markup
        ef'4
        \tweak Accidental.stencil #ly:text-interface::print
        \tweak Accidental.text \three-eighths-flat-markup
        a4
        \tweak Accidental.stencil #ly:text-interface::print
        \tweak Accidental.text \natural-markup
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
        \tweak Accidental.text \flat-markup
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

    """

    def __init__(
        self,
        pitch_list=None,
        allow_chord_duplicates=False,
        apply_all=False,
        chord_boolean_vector=[0],
        chord_groups=None,
        continuous=False,
        to_ties=False,
        pitch_count=-1,
        chord_boolean_count=-1,
        chord_groups_count=-1,
        name="Pitch Handler",
    ):
        self.pitch_list = pitch_list
        self.allow_chord_duplicates = allow_chord_duplicates
        self.apply_all = apply_all
        self.chord_boolean_vector = chord_boolean_vector
        self.chord_groups = chord_groups
        self.continuous = continuous
        self.to_ties = to_ties
        self.name = name
        self._pitch_count = pitch_count
        self._chord_boolean_count = chord_boolean_count
        self._chord_groups_count = chord_groups_count
        self._cyc_pitches = sequence.CyclicList(
            self.pitch_list, self.continuous, self._pitch_count
        )
        self._cyc_chord_boolean_vector = sequence.CyclicList(
            self.chord_boolean_vector, self.continuous, self._chord_boolean_count
        )
        self._cyc_chord_groups = sequence.CyclicList(
            self.chord_groups, self.continuous, self._chord_groups_count
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
                    pitches_.append(self._cyc_pitches(r=self._cyc_chord_groups(r=1)[0]))
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

    def _apply_pitches(self, selections):
        leaf_maker = abjad.LeafMaker()
        old_ties = [tie for tie in abjad.iterate(selections).logical_ties(pitched=True)]
        if len(old_ties) > 0:
            pitches, durations, old_leaves = self._collect_pitches_durations_leaves(
                old_ties
            )
            microtonal_indices_to_pitch = abjad.OrderedDict()
            for i, _ in enumerate(pitches):
                if isinstance(_, list):
                    _.sort()
                    for i_, sub_ in enumerate(_):
                        nested_indices_to_pitch = abjad.OrderedDict()
                        if self.apply_all is False:
                            if 0 < sub_ % quicktions.Fraction(1, 2):
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
                        if 0 < _ % quicktions.Fraction(1, 2):
                            microtonal_indices_to_pitch[str(i)] = _
                            pitches[i] = 0
                    else:
                        microtonal_indices_to_pitch[str(i)] = _
                        pitches[i] = 0
            if self.apply_all is False:
                new_leaves = [leaf for leaf in leaf_maker(pitches, durations)]
            else:
                new_leaves = old_leaves
            for index in microtonal_indices_to_pitch:
                for leaf in abjad.select(new_leaves[int(index)]).leaves():
                    if isinstance(leaf, abjad.Chord):
                        heads = leaf.note_heads
                        for sub_index in microtonal_indices_to_pitch[index]:
                            head = heads[int(sub_index)]
                            microtones.apply_alteration(
                                head, microtonal_indices_to_pitch[index][sub_index]
                            )
                    else:
                        microtones.apply_alteration(
                            leaf.note_head, microtonal_indices_to_pitch[index]
                        )
            if self.apply_all is False:
                for old_leaf, new_leaf in zip(old_leaves, new_leaves):
                    indicators = abjad.inspect(old_leaf).indicators()
                    before_grace = abjad.inspect(old_leaf).before_grace_container()
                    for indicator in indicators:
                        abjad.attach(indicator, new_leaf)
                    if before_grace is not None:
                        abjad.attach(before_grace, new_leaf)
                    abjad.mutate(old_leaf).replace(new_leaf)

    def name(self):
        return self.name

    def state(self):
        return abjad.OrderedDict(
            [
                ("pitch_count", self._cyc_pitches.state()),
                ("chord_boolean_count", self._cyc_chord_boolean_vector.state()),
                ("chord_groups_count", self._cyc_chord_groups.state()),
            ]
        )


class RhythmHandler(Handler):
    def __init__(self, rmaker, continuous=False, state=None, name="Rhythm Handler"):
        self.rmaker = rmaker
        self.continuous = continuous
        self._input_state = state
        self.state = self.rmaker.state
        self.name = name

    def __call__(self, durations):
        return self._make_music(durations)

    def _make_basic_rhythm(self, durations):
        if self.continuous is True:
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

    def name(self):
        return self.name

    def return_state(self):
        return abjad.OrderedDict([("state", self.rmaker.state)])


class SlurHandler(Handler):
    r"""
    >>> staff = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = evans.SlurHandler()
    >>> handler(staff)
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
        continuous=True,
        count=-1,
        name="Slur Handler",
    ):
        self.apply_slur_to = apply_slur_to
        self._count = count
        self.continuous = continuous
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.continuous, self._count
        )
        self.name = name

    def __call__(self, selections):
        self.add_slurs(selections)

    def add_slurs(self, selections):
        if self.apply_slur_to == "selections":
            if self.boolean_vector(r=1)[0] == 1:
                abjad.slur(selections[:])
            else:
                pass
        elif self.apply_slur_to == "runs":
            for run in abjad.select(selections).runs():
                if self.boolean_vector(r=1)[0] == 1:
                    abjad.slur(run[:])
                else:
                    continue
        else:
            pass

    def name(self):
        return self.name

    def state(self):
        return abjad.OrderedDict([("count", self.boolean_vector.state())])


class TempoSpannerHandler(Handler):
    r"""
    >>> s = abjad.Staff("s4 s4 s4 s4")
    >>> handler = TempoSpannerHandler(
    ...     tempo_list=[(3, 0, 1, "87"), (3, 0, 1, "95")],
    ...     boolean_vector=[1],
    ...     padding=4,
    ...     staff_padding=2,
    ...     continuous=True,
    ... )
    >>> handler(s[:-1])
    >>> print(abjad.lilypond(s))
    \new Staff
    {
        s4
        - \abjad-dashed-line-with-arrow
        - \baca-metronome-mark-spanner-left-text 3 0 1 "87"
        - \tweak padding #4
        - \tweak staff-padding #2
        \bacaStartTextSpanMM
        s4
        s4
        \bacaStopTextSpanMM
        - \abjad-invisible-line
        - \baca-metronome-mark-spanner-left-text 3 0 1 "95"
        - \tweak padding #4
        - \tweak staff-padding #2
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
        continuous=True,
        tempo_count=-1,
        bool_count=-1,
        name="Tempo Spanner Handler",
    ):
        self._tempo_count = tempo_count
        self._bool_count = bool_count
        self.padding = padding
        self.continuous = continuous
        self.staff_padding = staff_padding
        self.tempo_list = sequence.CyclicList(
            tempo_list, self.continuous, self._tempo_count
        )
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.continuous, self._bool_count
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
                    + f'{start_temp[0]} {start_temp[1]} {start_temp[2]} "{start_temp[3]}"',
                    r"- \tweak padding #" + f"{self.padding}",
                    r"- \tweak staff-padding #" + f"{self.staff_padding}",
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
                    r"\bacaStartTextSpanMM",
                ],
                format_slot="after",
            )
            stopper = abjad.LilyPondLiteral(r"\bacaStopTextSpanMM", format_slot="after")
            abjad.attach(start_literal, abjad.select(ties).leaves()[0])
            abjad.attach(stop_literal, abjad.select(ties).leaves()[-1])
            abjad.attach(
                stopper, abjad.inspect(abjad.select(ties).leaves()[-1]).leaf(1)
            )

    def name(self):
        return self.name

    def state(self):
        return abjad.OrderedDict([("count", self.boolean_vector.state())])


class TextSpanHandler(Handler):
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
        continuous=False,
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
        self.continuous = continuous
        self._count_1 = count_1
        self._count_2 = count_2
        self._count_3 = count_3
        self._cyc_span_one_positions = sequence.CyclicList(
            span_one_positions, self.continuous, self._count_1
        )
        self._cyc_span_two_positions = sequence.CyclicList(
            span_two_positions, self.continuous, self._count_2
        )
        self._cyc_span_three_positions = sequence.CyclicList(
            span_three_positions, self.continuous, self._count_3
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
        abjad.attach(
            abjad.StopTextSpan(command=r"\stopTextSpan" + span_command), first_leaf
        )

    def _apply_position_and_span_to_bounds(
        self, selections, positions, style, span_command, span_padding
    ):
        for run in abjad.select(selections).runs():
            if len(run) < 2:
                start_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(positions(r=1)[0]).upright(),
                    style=style + "-with-hook",
                    command=r"\startTextSpan" + span_command,
                )
                abjad.attach(
                    abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                    abjad.inspect(run[-1]).leaf(1),
                )
                abjad.attach(start_span, run[0])
                abjad.tweak(start_span).staff_padding = span_padding
            else:
                start_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(positions(r=1)[0]).upright(),
                    style=style + "-with-arrow",
                    command=r"\startTextSpan" + span_command,
                    right_padding=1.4,
                )
                stop_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(positions(r=1)[0]).upright(),
                    style=style + "-with-hook",
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
                    abjad.inspect(run[-1]).leaf(1),
                )
                abjad.tweak(start_span).staff_padding = span_padding
                abjad.tweak(stop_span).staff_padding = span_padding

    def _apply_position_and_span_to_leaves(
        self, selections, positions, style, span_command, span_padding
    ):
        for run in abjad.select(selections).runs():
            ties = abjad.select(run).logical_ties(pitched=True)
            following_leaf = abjad.inspect(ties[-1][-1]).leaf(1)
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
                    left_text=abjad.Markup(start_string, literal=True),
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
                        literal=True,
                    ),
                    style=r"invisible-line",
                    command=r"\startTextSpan" + span_command,
                    right_padding=3,
                )
            else:
                final_indicator = abjad.StartTextSpan(
                    left_text=abjad.Markup(
                        fr"""\center-column {{ \center-align \upright \vcenter {start_strings[-1]} }}""",
                        literal=True,
                    ),
                    style=r"invisible-line",
                    command=r"\startTextSpan" + span_command,
                    right_padding=3,
                )
            for indicator in start_indicators:
                abjad.tweak(indicator).staff_padding = span_padding
            abjad.tweak(final_indicator).staff_padding = span_padding
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
                abjad.inspect(following_leaf).leaf(1),
            )

    def _apply_position_and_span_to_left(
        self, selections, positions, style, span_command, span_padding
    ):
        runs = abjad.select(selections).runs()
        start_strings = [positions(r=1)[0] for _ in runs]
        start_indicators = [
            abjad.StartTextSpan(
                left_text=abjad.Markup(start_string).upright(),
                style=fr"{style}-with-hook",
                command=r"\startTextSpan" + span_command,
                right_padding=3,
            )
            for start_string in start_strings
        ]
        for indicator in start_indicators:
            abjad.tweak(indicator).staff_padding = span_padding
        for i, pair in enumerate(zip(runs, start_indicators)):
            run, start_indicator = pair
            abjad.attach(start_indicator, run[0])
            abjad.attach(
                abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                abjad.inspect(run[-1]).leaf(1),
            )

    def name(self):
        return self.name

    def state(self):
        return abjad.OrderedDict(
            [
                ("count_1", self._cyc_span_one_positions.state()),
                ("count_2", self._cyc_span_two_positions.state()),
                ("count_3", self._cyc_span_three_positions.state()),
            ]
        )


class TrillHandler(Handler):
    r"""
    >>> staff = abjad.Staff("<c' d'>4 c'4 c'4 <c' d'>4 c'4 c'4 c'4 c'4 ")
    >>> handler = TrillHandler(boolean_vector=[0, 1], continuous=True)
    >>> handler(staff)
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
        self, boolean_vector=[0], continuous=True, count=-1, name="Trill Handler"
    ):
        self.continuous = continuous
        self._count = count
        self.boolean_vector = sequence.CyclicList(
            boolean_vector, self.continuous, self._count
        )
        self.name = name

    def __call__(self, selections):
        self._apply_trills(selections)

    def _apply_trills(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        vector = self.boolean_vector
        for tie, bool in zip(ties, vector(r=len(ties))):
            if bool == 1:
                if all(
                    isinstance(leaf, abjad.Chord)
                    for leaf in abjad.iterate(tie).leaves()
                ):
                    old_chord = tie[0]
                    base_pitch = old_chord.written_pitches[0]
                    trill_pitch = old_chord.written_pitches[-1]
                    new_leaf = abjad.Note(base_pitch, old_chord.written_duration)

                    trill_start = abjad.LilyPondLiteral(
                        r"\pitchedTrill", format_slot="before"
                    )
                    trill_literal = abjad.LilyPondLiteral(
                        fr"\startTrillSpan {trill_pitch}", format_slot="after"
                    )
                    trill_stop = abjad.LilyPondLiteral(
                        r"\stopTrillSpan", format_slot="after"
                    )
                    abjad.attach(trill_start, new_leaf)
                    abjad.attach(trill_literal, new_leaf)
                    last_leaf = tie[-1]
                    next_leaf = abjad.inspect(last_leaf).leaf(1)
                    if next_leaf is not None:
                        abjad.attach(trill_stop, next_leaf)
                    else:
                        continue
                    indicators = abjad.inspect(old_chord).indicators()
                    for indicator in indicators:
                        abjad.attach(indicator, new_leaf)

                    parent = abjad.inspect(old_chord).parentage().parent
                    parent[parent.index(old_chord)] = new_leaf

                    tail = abjad.select(tie).leaves()[1:]
                    for leaf in tail:
                        new_tail = abjad.Note(base_pitch, leaf.written_duration)
                        indicators = abjad.inspect(leaf).indicators()
                        for indicator in indicators:
                            abjad.attach(indicator, new_tail)
                        before_grace = abjad.inspect(leaf).before_grace_container()
                        if before_grace is not None:
                            abjad.attach(before_grace, new_tail)
                        parent = abjad.inspect(leaf).parentage().parent
                        parent[parent.index(leaf)] = new_tail
                else:
                    continue
            else:
                continue

    def name(self):
        return self.name

    def state(self):
        return abjad.OrderedDict([("count", self.boolean_vector.state())])
