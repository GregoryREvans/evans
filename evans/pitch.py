"""
Pitch functions.
"""
import collections
import copy
import dataclasses
import math
import typing

import abjad
import baca
import quicktions
from abjadext import microtones

from .sequence import RatioClassSet, RatioSegment, Sequence
from .verticalmoment import iterate_vertical_moments_by_logical_tie


class ETPitch(abjad.Pitch):
    def __init__(
        self,
        fundamental,
        repeating_ratio,
        number_of_divisions,
        scale_degree,
        transposition=None,
        with_quarter_tones=False,
    ):
        self.fundamental = abjad.NamedPitch(fundamental)
        self.repeating_ratio = quicktions.Fraction(repeating_ratio)
        self.number_of_divisions = number_of_divisions
        self.scale_degree = scale_degree
        self.transposition = transposition
        self.with_quarter_tones = with_quarter_tones
        pair = self._calculate_pitch_and_deviation()
        self.pitch = pair[0]
        self.deviation = pair[1]
        self.pitch_hertz = pair[2]

    def __add__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            return type(self)(
                self.pitch.number + argument,
                self.repeating_ratio,
                self.number_of_divisions,
                self.scale_degree,
                self.transposition,
                self.with_quarter_tones,
            )
        else:
            raise Exception(
                "Argument must be of types: int, float, or quicktions.Fraction"
            )

    def __truediv__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            return type(self)(
                self.pitch.number / argument,
                self.repeating_ratio,
                self.number_of_divisions,
                self.scale_degree,
                self.transposition,
                self.with_quarter_tones,
            )
        else:
            raise Exception(
                "Argument must be of types: int, float, or quicktions.Fraction"
            )

    def __lt__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            return self.pitch.number < argument

    def __lte__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            return self.pitch.number <= argument

    def __mod__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            return self.pitch.number % argument

    def __mul__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            return type(self)(
                self.pitch.number * argument,
                self.repeating_ratio,
                self.number_of_divisions,
                self.scale_degree,
                self.transposition,
                self.with_quarter_tones,
            )
        else:
            raise Exception(
                "Argument must be of types: int, float, or quicktions.Fraction"
            )

    def __str__(self):
        return abjad.lilypond(self.pitch)

    def __sub__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            return type(self)(
                self.pitch.number - argument,
                self.repeating_ratio,
                self.number_of_divisions,
                self.scale_degree,
                self.transposition,
                self.with_quarter_tones,
            )
        else:
            raise Exception(
                "Argument must be of types: int, float, or quicktions.Fraction"
            )

    def _get_lilypond_format(self):
        return abjad.lilypond(self.pitch)

    def _calculate_pitch_and_deviation(self):
        nth_root_of_ratio = self.repeating_ratio ** quicktions.Fraction(
            1, self.number_of_divisions
        )
        scale_degree_multiplier = nth_root_of_ratio**self.scale_degree
        degree = self.fundamental.hertz * scale_degree_multiplier
        rounded_pitch = abjad.NamedPitch.from_hertz(degree)
        if rounded_pitch.accidental == abjad.Accidental("qs"):
            rounded_pitch = rounded_pitch + 0.5
        elif rounded_pitch.accidental == abjad.Accidental("qf"):
            rounded_pitch = rounded_pitch - 0.5
        ratio = quicktions.Fraction(degree / rounded_pitch.hertz)
        ji_pitch = JIPitch(
            rounded_pitch, ratio, with_quarter_tones=self.with_quarter_tones
        )
        nearest = ji_pitch.pitch, ji_pitch.deviation, degree
        return nearest

    @property
    def name(self):
        return abjad.lilypond(self.pitch)

    @property
    def pitch_class(self):
        return abjad.NamedPitchClass(self.pitch)

    @property
    def octave(self):
        return abjad.Octave(self.pitch)


class JIPitch(abjad.Pitch):
    r"""

    Just Intonation Pitch

    .. container:: example

        >>> pitch = evans.JIPitch("c'", "7/4", with_quarter_tones=True)
        >>> note = abjad.Note(pitch, (1, 4))
        >>> mark = abjad.Markup(fr"\markup {str(pitch.deviation)}")
        >>> abjad.attach(mark, note, direction=abjad.UP)
        >>> abjad.show(note) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(note))
            aqs'4
            ^ \markup 19

    .. container:: example

        >>> pitch = evans.JIPitch("c'", "7/4", with_quarter_tones=False)
        >>> note = abjad.Note(pitch, (1, 4))
        >>> mark = abjad.Markup(fr"\markup {str(pitch.deviation)}")
        >>> abjad.attach(mark, note, direction=abjad.UP)
        >>> abjad.show(note) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(note))
            bf'4
            ^ \markup -31

    """

    def __init__(
        self,
        fundamental,
        ratio,
        with_quarter_tones=False,
    ):
        self.fundamental = abjad.NamedPitch(fundamental)
        self.ratio = quicktions.Fraction(ratio)
        self.with_quarter_tones = with_quarter_tones
        pair = self._calculate_pitch_and_deviation(self.fundamental, self.ratio)
        self.pitch = pair[0]
        self.deviation = pair[1]

    def __add__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            self_ratio = self.ratio
            self_fraction = quicktions.Fraction(self_ratio)
            return type(self)(
                self.fundamental,
                quicktions.Fraction(self_fraction + argument),
                self.with_quarter_tones,
            )
        elif isinstance(argument, type(self)):
            self_pitch = self.pitch
            argument_pitch = argument.pitch
            return type(self)(
                self.fundamental.number + argument.fundamental.number,
                quicktions.Fraction(self_pitch.number + argument_pitch.number),
                self.with_quarter_tones,
            )

    def __truediv__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            self_ratio = self.ratio
            self_fraction = quicktions.Fraction(self_ratio)
            return type(self)(
                self.fundamental,
                quicktions.Fraction(self_fraction / argument),
                self.with_quarter_tones,
            )
        elif isinstance(argument, type(self)):
            self_pitch = self.pitch
            argument_pitch = argument.pitch
            return type(self)(
                self.fundamental.number / argument.fundamental.number,
                quicktions.Fraction(self_pitch.number / argument_pitch.number),
                self.with_quarter_tones,
            )

    def __lt__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            self_ratio = self.ratio
            self_fraction = quicktions.Fraction(self_ratio)
            return self_fraction < argument
        elif isinstance(argument, type(self)):
            self_pitch = self.pitch
            argument_pitch = argument.pitch
            return self_pitch < argument_pitch

    def __lte__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            self_ratio = self.ratio
            self_fraction = quicktions.Fraction(self_ratio)
            return self_fraction <= argument
        elif isinstance(argument, type(self)):
            self_pitch = self.pitch
            argument_pitch = argument.pitch
            return self_pitch <= argument_pitch

    def __mod__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            return self.pitch.number % argument
        elif isinstance(argument, type(self)):
            self_pitch = self.pitch
            argument_pitch = argument.pitch
            return type(self)(
                self.fundamental.number % argument.fundamental.number,
                quicktions.Fraction(self_pitch.number % argument_pitch.number),
                self.with_quarter_tones,
            )

    def __mul__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            self_ratio = self.ratio
            self_fraction = quicktions.Fraction(self_ratio)
            return type(self)(
                self.fundamental,
                quicktions.Fraction(self_fraction * argument),
                self.with_quarter_tones,
            )
        elif isinstance(argument, type(self)):
            self_pitch = self.pitch
            argument_pitch = argument.pitch
            return type(self)(
                self.fundamental.number * argument.fundamental.number,
                quicktions.Fraction(self_pitch.number * argument_pitch.number),
                self.with_quarter_tones,
            )

    def __str__(self):
        return abjad.lilypond(self.pitch)

    def __sub__(self, argument):
        if isinstance(argument, (int, float, quicktions.Fraction)):
            self_ratio = self.ratio
            self_fraction = quicktions.Fraction(self_ratio)
            return type(self)(
                self.fundamental,
                quicktions.Fraction(self_fraction - argument),
                self.with_quarter_tones,
            )
        elif isinstance(argument, type(self)):
            self_pitch = self.pitch
            argument_pitch = argument.pitch
            return type(self)(
                self.fundamental.number - argument.fundamental.number,
                quicktions.Fraction(self_pitch.number - argument_pitch.number),
                self.with_quarter_tones,
            )

    def _get_lilypond_format(self):
        return abjad.lilypond(self.pitch)

    def _calculate_pitch_and_deviation(
        self,
        pitch,
        ratio,
    ):
        ratio = quicktions.Fraction(ratio)
        log_ratio = quicktions.Fraction(math.log10(ratio))
        log_2 = quicktions.Fraction(1200 / math.log10(2))
        ji_cents = quicktions.Fraction(log_ratio * log_2)
        semitones = ji_cents / 100
        parts = math.modf(semitones)
        pitch = abjad.NumberedPitch(pitch) + parts[1]
        remainder = round(parts[0] * 100)
        if 50 < abs(remainder):
            if 0 < remainder:
                pitch += 1
                remainder = -100 + remainder
            else:
                pitch -= 1
                remainder = 100 + remainder
        if self.with_quarter_tones:
            if 25 < abs(remainder):
                if 0 < remainder:
                    pitch += 0.5
                    remainder = -50 + remainder
                else:
                    pitch -= 0.5
                    remainder = 50 + remainder
        return pitch, remainder

    @property
    def name(self):
        return abjad.lilypond(self.pitch)

    @property
    def pitch_class(self):
        return abjad.NamedPitchClass(self.pitch)

    @property
    def octave(self):
        return abjad.Octave(self.pitch)


def combination_tones(pitches=[0, 5, 7], depth=1):
    """

    ..  container:: example

        >>> print(
        ...     evans.combination_tones(
        ...         pitches=[
        ...             8.25,
        ...             18.75,
        ...             23.5,
        ...         ],
        ...         depth=1,
        ...     )
        ... )
        [-2.0, 6.0, 8.0, 14.5, 19.0, 23.5, 26.0, 29.5, 33.5]

    ..  container:: example

        >>> print(
        ...     evans.combination_tones(
        ...         pitches=[
        ...             7.75,
        ...             19,
        ...             25.25,
        ...             28.5
        ...         ],
        ...         depth=1,
        ...     )
        ... )
        [-1.0, 4.0, 6.0, 8.0, 13.5, 17.0, 19.0, 22.0, 25.0, 26.0, 28.5, 30.5, 33.0, 34.0, 36.5, 39.0]

    """
    pitches = [abjad.NumberedPitch(_).hertz for _ in pitches]
    new_pitches = []
    for iter in range(depth):
        for i, num in enumerate(pitches):
            new_pitches.append(num)
            for num_ in pitches[i + 1 :]:
                new_pitches.append(num + num_)
                if num > num_:
                    new_pitches.append(num - num_)
                elif num < num_:
                    new_pitches.append(num_ - num)
                else:
                    continue
        pitches = new_pitches
        new_pitches = []
    pitches = [float(abjad.NumberedPitch.from_hertz(x)) for x in pitches]
    reduce = []
    for y in pitches:
        if y not in reduce:
            reduce.append(y)
    reduce.sort()
    pitches = reduce
    return pitches


def herz_combination_tone_ratios(
    fundamental=261.625565, pitches=[327.03195625, 392.43834749999996], depth=2
):
    """

    ..  container:: example

        >>> print(
        ...     evans.herz_combination_tone_ratios(
        ...     fundamental=261.625565,
        ...     pitches=[
        ...         327.03195625,
        ...         392.43834749999996
        ...         ],
        ...     depth=1,
        ...     )
        ... )
        ['4503599627370493/18014398509481984', '5/4', '3/2', '11/4']

    """
    new_pitches = []
    for iter in range(depth):
        for i, num in enumerate(pitches):
            new_pitches.append(num)
            for num_ in pitches[i + 1 :]:
                new_pitches.append(num + num_)
                if num > num_:
                    new_pitches.append(num - num_)
                elif num < num_:
                    new_pitches.append(num_ - num)
                else:
                    continue
        pitches = new_pitches
        new_pitches = []
    reduce = []
    for y in pitches:
        if y not in reduce:
            reduce.append(y)
    reduce.sort()
    pitches = reduce
    returned_list = []
    for freq in pitches:
        returned_list.append(str(quicktions.Fraction(freq / fundamental)))
    return returned_list


def return_cent_markup(
    note_head,
    ratio,
    quarter_tones=False,
):
    ratio = quicktions.Fraction(ratio)
    log_ratio = quicktions.Fraction(math.log10(ratio))
    log_2 = quicktions.Fraction(1200 / math.log10(2))
    ji_cents = quicktions.Fraction(log_ratio * log_2)
    semitones = ji_cents / 100
    parts = math.modf(semitones)
    pitch = abjad.NumberedPitch(note_head.written_pitch) + parts[1]
    remainder = round(parts[0] * 100)
    if 50 < abs(remainder):
        if 0 < remainder:
            pitch += 1
            remainder = -100 + remainder
        else:
            pitch -= 1
            remainder = 100 + remainder
    if quarter_tones:
        if 25 < abs(remainder):
            if 0 < remainder:
                pitch += 0.5
                remainder = -50 + remainder
            else:
                pitch -= 0.5
                remainder = 50 + remainder
    if remainder < 0:
        cent_string = f"{remainder}"
    else:
        cent_string = f"+{remainder}"
    mark = abjad.Markup(
        rf"\markup \center-align {cent_string}"
    )  # WARNING: previously had direction=abjad.UP maybe remove ^
    return mark


def return_vertical_moment_ties(score):
    r"""

    ..  container:: example

        >>> staff_1 = abjad.Staff("c'4 c'2 c'4")
        >>> staff_2 = abjad.Staff("cs'4 cs'4 cs'2")
        >>> staff_3 = abjad.Staff("d'8 d'8 d'8 d'8 d'8 d'8 d'8 d'8")
        >>> score = abjad.Score(
        ...     [
        ...         staff_1,
        ...         staff_2,
        ...         staff_3,
        ...     ]
        ... )
        >>> for tie in evans.return_vertical_moment_ties(score):
        ...     tie
        ...
        LogicalTie(items=[Note("d'8")])
        LogicalTie(items=[Note("c'4")])
        LogicalTie(items=[Note("cs'4")])
        LogicalTie(items=[Note("d'8")])
        LogicalTie(items=[Note("d'8")])
        LogicalTie(items=[Note("cs'4")])
        LogicalTie(items=[Note("c'2")])
        LogicalTie(items=[Note("d'8")])
        LogicalTie(items=[Note("d'8")])
        LogicalTie(items=[Note("cs'2")])
        LogicalTie(items=[Note("d'8")])
        LogicalTie(items=[Note("d'8")])
        LogicalTie(items=[Note("c'4")])
        LogicalTie(items=[Note("d'8")])

    ..  container:: example

        >>> staff_1 = abjad.Staff("c'4 c'2 c'4")
        >>> staff_2 = abjad.Staff("cs'4 cs'4 cs'2")
        >>> staff_3 = abjad.Staff("d'8 d'8 d'8 d'8 d'8 d'8 d'8 d'8")
        >>> score = abjad.Score(
        ...     [
        ...         staff_1,
        ...         staff_2,
        ...         staff_3,
        ...     ]
        ... )
        ...
        >>> handler = evans.PitchHandler(
        ...     pitch_list=[0, 1, 2, 3, 4],
        ...     forget=False,
        ...     to_ties=True,
        ... )
        ...
        >>> vm_ties = evans.return_vertical_moment_ties(score)
        >>> numbers = [_ for _ in range(len(vm_ties))]
        >>> for i, tie in zip(numbers, vm_ties):
        ...     string = f"{i}"
        ...     markup = abjad.Markup(fr"\markup {string}")
        ...     abjad.attach(markup, tie[0])
        ...
        >>> handler(vm_ties)
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

            >>> print(abjad.lilypond(score))
            \new Score
            \with
            {
                proportionalNotationDuration = #(ly:make-moment 1 25)
            }
            <<
                \new Staff
                {
                    cs'4
                    - \markup 1
                    cs'2
                    - \markup 6
                    d'4
                    - \markup 12
                }
                \new Staff
                {
                    d'4
                    - \markup 2
                    c'4
                    - \markup 5
                    e'2
                    - \markup 9
                }
                \new Staff
                {
                    c'8
                    - \markup 0
                    ef'8
                    - \markup 3
                    e'8
                    - \markup 4
                    d'8
                    - \markup 7
                    ef'8
                    - \markup 8
                    c'8
                    - \markup 10
                    cs'8
                    - \markup 11
                    ef'8
                    - \markup 13
                }
            >>

    ..  container:: example

        >>> staff_1 = abjad.Staff("c'4 ~ c'2 c'4")
        >>> staff_2 = abjad.Staff("cs'4 cs'4 cs'2")
        >>> staff_3 = abjad.Staff("d'8 d'8 d'8 d'8 d'8 d'8 d'8 d'8")
        >>> score = abjad.Score(
        ...     [
        ...         staff_1,
        ...         staff_2,
        ...         staff_3,
        ...     ]
        ... )
        >>> handler = evans.PitchHandler(pitch_list=[0, 1, 2, 3, 4], forget=False)
        >>> vm_ties = evans.return_vertical_moment_ties(score)
        >>> numbers = [_ for _ in range(len(vm_ties))]
        >>> for i, tie in zip(numbers, vm_ties):
        ...     string = f"{i}"
        ...     markup = abjad.Markup(fr"\markup {string}")
        ...     abjad.attach(markup, tie[0])
        ...     handler(tie)
        ...
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

            >>> print(abjad.lilypond(score))
            \new Score
            \with
            {
                proportionalNotationDuration = #(ly:make-moment 1 25)
            }
            <<
                \new Staff
                {
                    d'4
                    - \markup 2
                    ~
                    d'2
                    cs'4
                    - \markup 11
                }
                \new Staff
                {
                    cs'4
                    - \markup 1
                    c'4
                    - \markup 5
                    ef'2
                    - \markup 8
                }
                \new Staff
                {
                    c'8
                    - \markup 0
                    ef'8
                    - \markup 3
                    e'8
                    - \markup 4
                    cs'8
                    - \markup 6
                    d'8
                    - \markup 7
                    e'8
                    - \markup 9
                    c'8
                    - \markup 10
                    d'8
                    - \markup 12
                }
            >>

    """
    moments = [_ for _ in iterate_vertical_moments_by_logical_tie(score)]
    new_moments = []
    final_moments = []
    for moment in moments:
        new_moment = []
        for tie in moment.start_ties:
            if isinstance(tie, abjad.LogicalTie):
                new_moment.append(tie)
        if 0 < len(new_moment):
            new_moments.append(new_moment)
    for moment in new_moments:
        moment.sort(key=lambda _: abjad.get.timespan(_))
    new_moments.sort(key=lambda _: abjad.get.timespan(_[0]).start_offset)
    for moment in new_moments:
        final_moments.extend(moment)
    assert isinstance(final_moments[0], abjad.LogicalTie)
    return final_moments


def to_nearest_eighth_tone(number, frac=False):
    """
    Rounds number to nearest eighth

    ..  container:: example

        >>> l = [0, 1.111, 4.5, 2.23, 6.4, 7.3, 7.15]
        >>> l = [evans.to_nearest_eighth_tone(_, frac=True) for _ in l]
        >>> l
        [Fraction(0, 1), Fraction(1, 1), Fraction(9, 2), Fraction(9, 4), Fraction(13, 2), Fraction(29, 4), Fraction(29, 4)]

    """
    number = round(float(number) * 4) / 4
    div, mod = divmod(number, 1)
    if mod == 0.75:
        div += 0.75
    elif mod == 0.5:
        div += 0.5
    elif mod == 0.25:
        div += 0.25
    if frac is False:
        return abjad.math.integer_equivalent_number_to_integer(div)
    else:
        return quicktions.Fraction(abjad.math.integer_equivalent_number_to_integer(div))


def to_nearest_quarter_tone(number, frac=False):
    """
    Rounds number to nearest quarter

    ..  container:: example

        >>> l = [0, 1.111, 4.5, 2.23, 6.4, 7.3, 7.15]
        >>> l = [evans.to_nearest_quarter_tone(_, frac=True) for _ in l]
        >>> l
        [Fraction(0, 1), Fraction(1, 1), Fraction(9, 2), Fraction(2, 1), Fraction(13, 2), Fraction(7, 1), Fraction(7, 1)]

    """
    number = round(float(number) * 4) / 4
    div, mod = divmod(number, 1)
    if mod == 0.75:
        div += 1
    elif mod == 0.5:
        div += 0.5
    if frac is False:
        return abjad.math.integer_equivalent_number_to_integer(div)
    else:
        return quicktions.Fraction(abjad.math.integer_equivalent_number_to_integer(div))


def to_nearest_sixth_tone(number):
    """
    Rounds number to nearest sixth

    ..  container:: example

        >>> l = [0, 1.111, 4.5, 2.23, 6.4, 7.3, 7.15]
        >>> l = [evans.to_nearest_sixth_tone(_) for _ in l]
        >>> l
        [Fraction(0, 1), Fraction(1, 1), Fraction(9, 2), Fraction(7, 3), Fraction(19, 3), Fraction(22, 3), Fraction(7, 1)]

    """
    semitones = quicktions.Fraction(int(round(6 * number)), 6)
    if semitones.denominator == 6:
        semitones = quicktions.Fraction(int(round(3 * number)), 3)
    return semitones


def to_nearest_third_tone(number):
    """
    Rounds number to nearest third

    ..  container:: example

        >>> l = [0, 1.111, 4.5, 2.23, 6.4, 7.3, 7.15]
        >>> l = [evans.to_nearest_third_tone(_) for _ in l]
        >>> l
        [Fraction(0, 1), Fraction(1, 1), Fraction(14, 3), Fraction(2, 1), Fraction(20, 3), Fraction(22, 3), Fraction(7, 1)]

    """
    semitones = quicktions.Fraction(int(round(3 * number)), 3)
    if semitones.denominator == 3:
        semitones = quicktions.Fraction(
            int(round(quicktions.Fraction(3, 2) * number)), quicktions.Fraction(3, 2)
        )
    return semitones


def to_nearest_twelfth_tone(number):
    """
    Rounds number to nearest twelfth

    ..  container:: example

        >>> l = [0, 1.111, 4.5, 2.23, 6.4, 7.3, 7.15]
        >>> l = [evans.to_nearest_twelfth_tone(_) for _ in l]
        >>> l
        [Fraction(0, 1), Fraction(7, 6), Fraction(9, 2), Fraction(9, 4), Fraction(19, 3), Fraction(22, 3), Fraction(43, 6)]

    """
    semitones = quicktions.Fraction(int(round(12 * number)), 12)
    if semitones.denominator == 12:
        semitones = quicktions.Fraction(int(round(6 * number)), 6)
    return semitones


def tonnetz(chord, chord_quality, transforms):
    """
    ..  container:: example

        >>> source = ["1/1", "6/5", "3/2"]
        >>> triads = evans.tonnetz(source, "minor", ["p", "l", "r"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 6/5, 3/2)
        (1, 5/4, 3/2)
        (5/4, 3/2, 15/8)
        (3/2, 15/8, 9/8)

    ..  container:: example

        >>> source = ["1/1", "5/4", "3/2"]
        >>> triads = evans.tonnetz(source, "major", ["p", "l", "r"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 5/4, 3/2)
        (1, 6/5, 3/2)
        (4/5, 1, 6/5)
        (2/3, 4/5, 1)

    ..  container:: example

        >>> source = ["1/1", "12/7", "3/2"]
        >>> triads = evans.tonnetz(source, "minor", ["p", "l7", "r7"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 12/7, 3/2)
        (1, 7/8, 3/2)
        (7/4, 3/2, 21/16)
        (3/2, 21/16, 9/8)

    ..  container:: example

        >>> source = ["1/1", "7/4", "3/2"]
        >>> triads = evans.tonnetz(source, "major", ["p", "l7", "r7"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 7/4, 3/2)
        (1, 6/7, 3/2)
        (4/7, 1, 6/7)
        (2/3, 4/7, 1/2)

    ..  container:: example

        >>> source = ["1/1", "12/11", "3/2"]
        >>> triads = evans.tonnetz(source, "minor", ["p", "l11", "r11"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 12/11, 3/2)
        (1, 11/8, 3/2)
        (11/8, 3/2, 33/32)
        (3/2, 33/32, 9/8)

    ..  container:: example

        >>> source = ["1/1", "11/8", "3/2"]
        >>> triads = evans.tonnetz(source, "major", ["p", "l11", "r11"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 11/8, 3/2)
        (1, 12/11, 3/2)
        (8/11, 1, 12/11)
        (2/3, 8/11, 1)

    ..  container:: example

        >>> source = ["1/1", "24/13", "3/2"]
        >>> triads = evans.tonnetz(source, "minor", ["p", "l13", "r13"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 24/13, 3/2)
        (1, 13/16, 3/2)
        (13/8, 3/2, 39/32)
        (3/2, 39/32, 9/8)

    ..  container:: example

        >>> source = ["1/1", "13/8", "3/2"]
        >>> triads = evans.tonnetz(source, "major", ["p", "l13", "r13"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 13/8, 3/2)
        (1, 12/13, 3/2)
        (8/13, 1, 12/13)
        (2/3, 8/13, 1/2)

    ..  container:: example

        >>> source = ["1/1", "24/17", "3/2"]
        >>> triads = evans.tonnetz(source, "minor", ["p", "l17", "r17"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 24/17, 3/2)
        (1, 17/16, 3/2)
        (17/16, 3/2, 51/32)
        (3/2, 51/32, 9/8)

    ..  container:: example

        >>> source = ["1/1", "17/16", "3/2"]
        >>> triads = evans.tonnetz(source, "major", ["p", "l17", "r17"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 17/16, 3/2)
        (1, 24/17, 3/2)
        (16/17, 1, 24/17)
        (2/3, 16/17, 1)

    ..  container:: example

        >>> source = ["1/1", "24/19", "3/2"]
        >>> triads = evans.tonnetz(source, "minor", ["p", "l19", "r19"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 24/19, 3/2)
        (1, 19/16, 3/2)
        (19/16, 3/2, 57/32)
        (3/2, 57/32, 9/8)

    ..  container:: example

        >>> source = ["1/1", "19/16", "3/2"]
        >>> triads = evans.tonnetz(source, "major", ["p", "l19", "r19"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 19/16, 3/2)
        (1, 24/19, 3/2)
        (16/19, 1, 24/19)
        (2/3, 16/19, 1)

    ..  container:: example

        >>> source = ["1/1", "24/23", "3/2"]
        >>> triads = evans.tonnetz(source, "minor", ["p", "l23", "r23"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 24/23, 3/2)
        (1, 23/16, 3/2)
        (23/16, 3/2, 69/64)
        (3/2, 69/64, 9/8)

    ..  container:: example

        >>> source = ["1/1", "23/16", "3/2"]
        >>> triads = evans.tonnetz(source, "major", ["p", "l23", "r23"])
        >>> for triad in triads:
        ...     print(triad)
        ...
        (1, 23/16, 3/2)
        (1, 24/23, 3/2)
        (16/23, 1, 24/23)
        (2/3, 16/23, 1)

    """
    chord = RatioSegment(chord)
    chord = chord.constrain_to_octave()
    returned_list = [chord]
    updated_transforms = []
    for transform in transforms:
        if transform == "n":
            updated_transforms.extend(["r", "l", "p"])
        elif transform == "s":
            updated_transforms.extend(["l", "p", "r"])
        elif transform == "h":
            updated_transforms.extend(["l", "p", "l"])
        elif transform == "N":
            updated_transforms.append(["r", "l", "p"])
        elif transform == "S":
            updated_transforms.append(["l", "p", "r"])
        elif transform == "H":
            updated_transforms.append(["l", "p", "l"])
        else:
            updated_transforms.append(transform)
    for transform in updated_transforms:
        if isinstance(transform, list):
            returned_list.append(
                tonnetz(returned_list[-1], chord_quality, transform)[-1]
            )
        elif transform == "p":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                returned_list.append(i)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                returned_list.append(i)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "l":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("5/4")
                il = il.constrain_to_octave()
                returned_list.append(il)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("4/5")
                il = il.constrain_to_octave()
                returned_list.append(il)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "r":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("5/6")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("6/5")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "l7":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("7/4")
                il = il.constrain_to_octave()
                returned_list.append(il)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("4/7")
                il = il.constrain_to_octave()
                returned_list.append(il)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "r7":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("7/12")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("12/7")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "l11":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("11/8")
                il = il.constrain_to_octave()
                returned_list.append(il)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("8/11")
                il = il.constrain_to_octave()
                returned_list.append(il)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "r11":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("11/12")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("12/11")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "l13":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("13/8")
                il = il.constrain_to_octave()
                returned_list.append(il)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("8/13")
                il = il.constrain_to_octave()
                returned_list.append(il)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "r13":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("13/24")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("24/13")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "l17":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("17/16")
                il = il.constrain_to_octave()
                returned_list.append(il)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("16/17")
                il = il.constrain_to_octave()
                returned_list.append(il)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "r17":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("17/24")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("24/17")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "l19":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("19/16")
                il = il.constrain_to_octave()
                returned_list.append(il)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("16/19")
                il = il.constrain_to_octave()
                returned_list.append(il)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "r19":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("19/24")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("24/19")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "l23":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("23/16")
                il = il.constrain_to_octave()
                returned_list.append(il)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                il = i.multiply("16/23")
                il = il.constrain_to_octave()
                returned_list.append(il)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        elif transform == "r23":
            if chord_quality == "major":
                chord_quality = "minor"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("23/24")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            elif chord_quality == "minor":
                chord_quality = "major"
                target = returned_list[-1]
                i = target.invert(target[0])
                i = i.multiply("3/2")
                i = i.constrain_to_octave()
                i = i.retrograde()
                ir = i.multiply("24/23")
                ir = ir.constrain_to_octave()
                returned_list.append(ir)
            else:
                raise Exception(f"Unrecogized chord quality {chord_quality}")
        else:
            raise Exception(
                f"Transform '{transform}' not recognized. Use p, l, l7, l11, l13, l17, l19, l23, r, r7, r11, r13, r17, r19, r23, s, h, or, n."
            )
    return returned_list


def tune_to_ratio(
    note_head,
    ratio,
    quarter_tones=False,
):
    """

    Tunes pitch to ratio.

    """
    ratio = quicktions.Fraction(ratio)
    log_ratio = quicktions.Fraction(math.log10(ratio))
    log_2 = quicktions.Fraction(1200 / math.log10(2))
    ji_cents = quicktions.Fraction(log_ratio * log_2)
    semitones = ji_cents / 100
    parts = math.modf(semitones)
    pitch = abjad.NumberedPitch(note_head.written_pitch) + parts[1]
    remainder = round(parts[0] * 100)
    if 50 < abs(remainder):
        if 0 < remainder:
            pitch += 1
            remainder = -100 + remainder
        else:
            pitch -= 1
            remainder = 100 + remainder
    if quarter_tones:
        if 25 < abs(remainder):
            if 0 < remainder:
                pitch += 0.5
                remainder = -50 + remainder
            else:
                pitch -= 0.5
                remainder = 50 + remainder
    note_head.written_pitch = pitch


class BacaLoop:
    def __init__(self, pitches, intervals):
        self.pitches = pitches
        self.intervals = intervals

    def __getitem__(self, i):
        intervals = abjad.CyclicTuple(self.intervals)
        pitches = abjad.CyclicTuple(self.pitches)
        iteration = i // len(pitches)
        if not pitches:
            transposition = 0
        else:
            transposition = sum(intervals[:iteration])
        number = pitches[i]
        pitch = abjad.NamedPitch(number + transposition)
        return pitch

    def __iter__(self):
        return self.pitches.__iter__()


class PitchCommand:
    def __init__(self, command_function):
        self.command_function = command_function

    def __call__(self, argument):
        self.command_function(argument)


def loop(
    items: baca.typing.Sequence,
    intervals: baca.typing.Sequence,
    selector=lambda _: baca.select.plts(_, exclude=baca.enums.HIDDEN),
):
    loop = BacaLoop(items, intervals)

    def returned_function(selections):
        new_sel = selector(selections)
        sel_len = len(new_sel)
        new_pitches = [loop[i] for i in range(sel_len)]
        baca.pitches(new_sel, pitches=new_pitches, allow_obgc_mutation=True)

    return PitchCommand(returned_function)


class ArtificialHarmonic(abjad.Chord):

    ### CLASS VARIABLES ###

    __slots__ = (
        "style",
        "is_parenthesized",
        "with_sounding_pitch",
        "language",
        "multiplier",
        "tag",
    )

    ### INITIALISER ###
    def __init__(
        self,
        *arguments,
        style="harmonic",
        is_parenthesized=False,
        with_sounding_pitch=True,
        language="english",
        multiplier=None,
        tag=None,
    ):
        self.style = style
        self.is_parenthesized = is_parenthesized
        self.with_sounding_pitch = with_sounding_pitch
        self._note_heads = abjad.NoteHeadList()
        if len(arguments) == 1 and isinstance(arguments[0], str):
            string = f"{{ {arguments[0]} }}"
            parsed = self._parse_lilypond_string(string, language=language)
            assert len(parsed) == 1 and isinstance(parsed[0], abjad.Leaf)
            arguments = tuple([parsed[0]])
        are_cautionary: list[bool | None] = []
        are_forced: list[bool | None] = []
        are_parenthesized: list[bool | None] = []
        if len(arguments) == 1 and isinstance(arguments[0], abjad.Leaf):
            leaf = arguments[0]
            written_pitches = []
            written_duration = leaf.written_duration
            if multiplier is None:
                multiplier = leaf.multiplier
            # TODO: move to dedicated from_note() constructor:
            if isinstance(leaf, abjad.Note) and leaf.note_head is not None:
                written_pitches.append(leaf.note_head.written_pitch)
                are_cautionary = [leaf.note_head.is_cautionary]
                are_forced = [leaf.note_head.is_forced]
                are_parenthesized = [leaf.note_head.is_parenthesized]
                calculated_note = abjad.NamedInterval("+P4").transpose(arguments[0])
                written_pitches.append(calculated_note.note_head.written_pitch)
                are_cautionary.append(calculated_note.note_head.is_cautionary)
                are_forced.append(calculated_note.note_head.is_forced)
                are_parenthesized.append(calculated_note.note_head.is_parenthesized)
                self.written_pitches = written_pitches
            elif isinstance(leaf, abjad.Chord):
                written_pitches.extend(_.written_pitch for _ in leaf.note_heads)
                are_cautionary = [_.is_cautionary for _ in leaf.note_heads]
                are_forced = [_.is_forced for _ in leaf.note_heads]
                are_parenthesized = [_.is_parenthesized for _ in leaf.note_heads]
        # TODO: move to dedicated constructor:
        elif len(arguments) == 2:
            written_pitches, written_duration = arguments
            if isinstance(written_pitches, str):
                written_pitches = [_ for _ in written_pitches.split() if _]
            elif isinstance(written_pitches, type(self)):
                written_pitches = written_pitches.written_pitches
        elif len(arguments) == 0:
            written_pitches = [abjad.NamedPitch(_) for _ in [0, 4, 7]]
            written_duration = abjad.Duration(1, 4)
        else:
            raise ValueError(f"can not initialize chord from {arguments!r}.")
        abjad.Leaf.__init__(self, written_duration, multiplier=multiplier, tag=tag)
        if not are_cautionary:
            are_cautionary = [None for _ in written_pitches]
        if not are_forced:
            are_forced = [None for _ in written_pitches]
        if not are_parenthesized:
            are_parenthesized = [None for _ in written_pitches]
        if len(arguments) == 1:
            if isinstance(arguments[0], abjad.Note):
                self._note_heads = abjad.NoteHeadList()
        for written_pitch, is_cautionary, is_forced, is_parenthesized in zip(
            written_pitches, are_cautionary, are_forced, are_parenthesized
        ):
            if not is_cautionary:
                is_cautionary = False
            if not is_forced:
                is_forced = False
            if not is_parenthesized:
                is_parenthesized = False
            note_head = abjad.NoteHead(
                written_pitch=written_pitch,
                is_cautionary=is_cautionary,
                is_forced=is_forced,
                is_parenthesized=is_parenthesized,
            )
            if isinstance(written_pitch, abjad.NoteHead):
                note_head.tweaks = copy.deepcopy(written_pitch.tweaks)
            self._note_heads.append(note_head)
        if len(arguments) == 1 and isinstance(arguments[0], abjad.Leaf):
            self._copy_override_and_set_from_leaf(arguments[0])

        self.written_pitches = [
            note_head.written_pitch for note_head in self._note_heads
        ]

        if self.is_parenthesized:
            first_head = self._note_heads[0]
            first_head.is_parenthesized = self.is_parenthesized
            abjad.tweak(self._note_heads[0], r"\tweak ParenthesesItem.font-size #-4")
            # was: abjad.tweak(self._note_heads[0]).ParenthesesItem__font_size = -4

        if with_sounding_pitch is True:
            written_pitch_list = [_ for _ in written_pitches]
            written_pitch_list.append(self.sounding_pitch())
            self.written_pitches = written_pitch_list

        second_head = self._note_heads[1]
        abjad.tweak(
            second_head, rf"\tweak style #'{self.style}"
        )  # was: abjad.tweak(second_head).style = self.style

        if len(self._note_heads) == 3:
            third_head = self._note_heads[2]
            third_head.is_parenthesized = True
            abjad.tweak(third_head, r"\tweak font-size #-4")
            abjad.tweak(third_head, r"\tweak Accidental.font-size #-4")

    ### PUBLIC METHODS ###

    def sounding_pitch(self):
        r"Returns the sounding pitch of the harmonic as an |abjad.Pitch|."
        if len(self.written_pitches) == 1:
            interval = 24
        else:
            interval = abs(self.written_pitches[1] - self.written_pitches[0]).semitones
        sounding_pitch_dict = {
            1: 48,
            2: 36,
            3: 31,
            4: 28,
            5: 24,
            7: 19,
            9: 28,
            12: 12,
            16: 28,
            19: 19,
            24: 24,
            28: 28,
        }
        try:
            sounding_pitch = self.written_pitches[0] + sounding_pitch_dict[interval]
        except KeyError as err:
            raise ValueError(
                "cannot calculate sounding pitch for given interval"
            ) from err
        return sounding_pitch


def reduce_list_by_prime_limit(input_list, prime_limit):
    out = []
    for i in input_list:
        factors = microtones.ji._prime_factors(i)
        booleans = [prime_limit < factor for factor in factors]
        if any(booleans):
            continue
        out.append(i)
    return out


def reduce_list_to_contain_sole_prime(input_list, prime_limit):
    out = []
    for i in input_list:
        factors = microtones.ji._prime_factors(i)
        booleans = [prime_limit != factor for factor in factors]
        if any(booleans):
            continue
        out.append(i)
    return out


def reduced_spectrum(prime_limit, partial_cap, multiplier_reduction_function):
    """
    .. container:: example

        >>> value = evans.reduced_spectrum(
        ...     prime_limit=29,
        ...     partial_cap=192,
        ...     multiplier_reduction_function=evans.reduce_list_by_prime_limit,
        ...     )
        ...
        >>> print(value)
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 60, 63, 64, 65, 66, 68, 69, 70, 72, 75, 76, 77, 78, 80, 81, 84, 85, 87, 88, 90, 91, 92, 95, 96, 98, 99, 100, 102, 104, 105, 108, 110, 112, 114, 115, 116, 117, 119, 120, 121, 125, 126, 128, 130, 132, 133, 135, 136, 138, 140, 143, 144, 145, 147, 150, 152, 153, 154, 156, 160, 161, 162, 165, 168, 169, 170, 171, 174, 175, 176, 180, 182, 184, 187, 189, 190, 192]

    .. container:: example

        >>> value = evans.reduced_spectrum(
        ...     prime_limit=29,
        ...     partial_cap=192,
        ...     multiplier_reduction_function=evans.reduce_list_by_prime_limit,
        ...     )
        ...
        >>> primes = []
        >>> for i in value:
        ...     if microtones.ji._is_prime(i):
        ...         primes.append(i)
        ...
        >>> print(primes)
        [3, 5, 7, 11, 13, 17, 19, 23, 29]

    .. container:: example

        >>> value = evans.reduced_spectrum(
        ...     prime_limit=29,
        ...     partial_cap=192,
        ...     multiplier_reduction_function=evans.reduce_list_to_contain_sole_prime,
        ...     )
        ...
        >>> print(value)
        [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 46, 57, 85, 91, 92, 121, 171, 184]

    """
    out = []
    numbers_below_prime_limit = [_ for _ in range(1, prime_limit + 1)]
    numbers_below_partial_cap = [_ for _ in range(1, partial_cap + 1)]
    primes = [1, 2]
    for item in numbers_below_prime_limit:
        if microtones.ji._is_prime(item):
            primes.append(item)
    reversed_primes = [_ for _ in primes[::-1]]
    multipliers = [
        multiplier_reduction_function(numbers_below_partial_cap, prime)
        for prime in primes
    ]
    for prime, multiplier_set in zip(reversed_primes, multipliers):
        for multiplier in multiplier_set:
            out.append(prime * multiplier)
    out = list(set(out))
    out.sort()
    reduced_out = []
    for i in out:
        if partial_cap < i:
            continue
        reduced_out.append(i)
    return reduced_out


def annotate_concurrent_ratios(score, color="red", show_leaf_order=False):
    moments = [_.start_ties for _ in iterate_vertical_moments_by_logical_tie(score)]
    for moment in moments:
        counter = 0
        for tie in moment:
            if isinstance(tie[0], abjad.Rest):
                continue
            if isinstance(tie[0], abjad.Note):
                tie = tie[0]
                if show_leaf_order is True:
                    markup = abjad.Markup(rf"\markup {counter}")
                    bundle = abjad.bundle(markup, r"\tweak color #blue")
                    abjad.attach(bundle, tie, direction=abjad.DOWN)
                    counter += 1
                abjad.annotate(tie, "requires annotation", True)

    moments = [_ for _ in iterate_vertical_moments_by_logical_tie(score)]
    for moment in moments:
        for tie in moment.ties:
            attempt_booleans = [
                abjad.get.annotation(tie[0], "requires annotation") is not None,
                abjad.get.annotation(tie[0], "already annotated") is not True,
            ]
            if all(attempt_booleans):
                annotated_ratios = {}
                if len(moment.overlap_ties) == 0:
                    for tie_ in moment.ties:
                        leaf = tie_[0]
                        try:
                            ratio = abjad.get.annotation(leaf, "JI ratio")[0]
                            fraction = quicktions.Fraction(ratio)
                            fraction = (fraction.numerator, fraction.denominator)
                        except:  # do not use bare exception?
                            fraction = None
                        if fraction is not None:
                            voice_name = abjad.get.parentage(leaf).logical_voice()[
                                "voice"
                            ][7:-1]
                            annotated_ratios[voice_name] = fraction
                else:
                    for tie_ in moment.overlap_ties:
                        leaf = tie_[0]
                        try:
                            ratio = abjad.get.annotation(leaf, "JI ratio")[0]
                            fraction = quicktions.Fraction(ratio)
                            fraction = (fraction.numerator, fraction.denominator)
                        except:
                            fraction = None
                        if fraction is not None:
                            voice_name = abjad.get.parentage(leaf).logical_voice()[
                                "voice"
                            ][7:-1]
                            annotated_ratios[voice_name] = fraction
                tie_parent_name = abjad.get.parentage(tie[0]).logical_voice()["voice"][
                    7:-1
                ]
                try:
                    tie_fraction = annotated_ratios[tie_parent_name]
                    del annotated_ratios[tie_parent_name]
                except:
                    tie_annotation = abjad.get.annotation(tie[0], "JI ratio")[0]
                    tie_fraction = quicktions.Fraction(tie_annotation)
                    tie_fraction = (tie_fraction.numerator, tie_fraction.denominator)
                if len(annotated_ratios) == 0:
                    continue
                comparison_ratios = {}
                for key, value in annotated_ratios.items():
                    value_object = quicktions.Fraction(value[0], value[1])
                    tie_fraction_object = quicktions.Fraction(
                        tie_fraction[0], tie_fraction[1]
                    )
                    comparison_ratios[key] = quicktions.Fraction(
                        tie_fraction_object, value_object
                    )
                ordered_keys = sorted(
                    comparison_ratios,
                    key=lambda _: (
                        comparison_ratios[_].numerator,
                        comparison_ratios[_].denominator,
                    ),
                )
                chosen_comparison = ordered_keys[0]
                numerator = comparison_ratios[chosen_comparison].numerator
                denominator = comparison_ratios[chosen_comparison].denominator
                chosen_comparison = chosen_comparison.replace("voice", "")
                markup = abjad.Markup(
                    rf'\markup \center-align \concat {{ "{chosen_comparison} "\fraction {numerator} {denominator} }}'
                )
                bundle = abjad.bundle(markup, rf"\tweak color #{color}")
                abjad.attach(bundle, tie[0], direction=abjad.DOWN)
                abjad.annotate(tie[0], "already annotated", True)


def force_accidentals(selections):
    ties = abjad.select.logical_ties(selections, pitched=True)
    for tie in ties:
        first_leaf = tie[0]
        if isinstance(first_leaf, abjad.Note):
            first_leaf.note_head.is_forced = True
        elif isinstance(first_leaf, abjad.Chord):
            heads = first_leaf.note_heads
            for head in heads:
                head.is_forced = True
        else:
            ex = f"Object must be of type {type(abjad.Note())} or {type(abjad.Chord())}"
            raise Exception(ex)


def annotate_hertz(selections):
    for tie in abjad.select.logical_ties(selections):
        try:
            hertz = abjad.get.annotation(tie[0], "ratio")
            hertz = round(float(hertz), 1)
            m = abjad.Markup(rf"\markup \center-align {hertz}")
            bundle = abjad.bundle(m, r"\tweak color #red")
            abjad.attach(bundle, tie[0], direction=abjad.DOWN)
        except:
            continue


def clean_cent_markup(selections):
    # this is a hack because logical ties cannot be selected from leaves
    # ask trevor later
    ties = abjad.select.logical_ties(selections, pitched=True)
    for tie in ties:
        leaves = abjad.select.leaves(tie)[1:]
        for leaf in leaves:
            indicators = abjad.get.indicators(leaf, abjad.Markup)
            for indicator in indicators:
                abjad.detach(indicator, leaf)


class Lapidary:  # or Sculp?
    def __init__(
        self,
        direction="up",  # neutral, down
        following_treatment_reference="previous alteration",  # "previous pitch"
        following_treatment_range="centroid octave",  # "pure octave" "octave above" "octave below"
        force_initial_octavation=False,
    ):
        self.direction = direction
        self.following_treatment_reference = following_treatment_reference
        self.following_treatment_range = following_treatment_range
        self.force_initial_octavation = force_initial_octavation


def get_centroid(pitch_list):
    if isinstance(pitch_list, list):
        pitch_list.sort()
        lowest = pitch_list[0]
        highest = pitch_list[-1]
        interval = abjad.NumberedInterval(highest - lowest).semitones
        half_interval = abjad.NumberedInterval(interval / 2)
        reference_pitch = half_interval.transpose(highest)
    else:
        reference_pitch = pitch_list
    return reference_pitch


def transpose_from_range(pitch, range):
    temp_pitch = pitch
    low = range.start_pitch
    high = range.stop_pitch
    while temp_pitch < low:
        temp_pitch = abjad.NamedInterval("+P8").transpose(temp_pitch)
    while high < temp_pitch:
        temp_pitch = abjad.NamedInterval("-P8").transpose(temp_pitch)
    return temp_pitch


def get_register(reference_pitch=0, specifier="pure octave"):
    if isinstance(reference_pitch, list):
        reference_pitch = get_centroid(reference_pitch)
    named_reference_pitch = abjad.NamedPitch(reference_pitch)

    if specifier == "octave above":
        cap_pitch = abjad.NamedPitch(reference_pitch + 12)
    elif specifier == "octave below":
        cap_pitch = abjad.NamedPitch(reference_pitch - 12)
    elif specifier == "pure octave":
        while abjad.NamedPitchClass(named_reference_pitch) != abjad.NamedPitchClass(
            "c"
        ):
            named_reference_pitch = abjad.NamedPitch(named_reference_pitch.number - 0.5)
        cap_pitch = abjad.NamedPitch(named_reference_pitch + 12)
    elif specifier == "centroid octave":
        named_reference_pitch = abjad.NamedPitch(reference_pitch - 6)
        cap_pitch = abjad.NamedPitch(reference_pitch + 6)
    else:
        raise Exception(
            f"BAD value for 'specifier'!\nShould be 'octave above', 'octave below', 'pure octave', or 'centroid octave'.\nGot {specifier}."
        )

    pitch_list = [named_reference_pitch, cap_pitch]
    pitch_list.sort()
    register_string = pitch_list[0].name + ", " + pitch_list[1].name
    if specifier == "centroid octave":
        register_string = "[" + register_string + "]"
    elif specifier == "octave below":
        register_string = "[" + register_string + ")"
    elif specifier == "octave above":
        register_string = "(" + register_string + "]"
    else:
        register_string = "[" + register_string + ")"
    gotten_register = abjad.PitchRange(register_string)

    return gotten_register


def do_contouring(pitch_list, command):
    force_initial_octavation = command[1].force_initial_octavation
    if isinstance(command[0], int):
        try:
            index = command[0]
            continuation = pitch_list[index + 1 :]
            continuation_indices = [index + 1 + _ for _ in range(len(continuation))]
            if command[1].direction == "up":
                if force_initial_octavation is True:
                    if not isinstance(pitch_list[index], list):
                        pitch_list[index] = abjad.NamedInterval("+P8").transpose(
                            pitch_list[index]
                        )
                    else:
                        temp = []
                        for pitch in pitch_list[index]:
                            temp.append(abjad.NamedInterval("+P8").transpose(pitch))
                        pitch_list[index] = temp
                else:
                    try:
                        assert -1 < index - 1
                        if not isinstance(pitch_list[index], list):
                            while pitch_list[index] < get_centroid(
                                pitch_list[index - 1]
                            ):
                                pitch_list[index] = abjad.NamedInterval(
                                    "+P8"
                                ).transpose(pitch_list[index])
                        else:
                            centroid = get_centroid(pitch_list[index])
                            while centroid < get_centroid(pitch_list[index - 1]):
                                temp = []
                                centroid = abjad.NamedInterval("+P8").transpose(
                                    centroid
                                )
                                for pitch in pitch_list[index]:
                                    temp.append(
                                        abjad.NamedInterval("+P8").transpose(pitch)
                                    )
                                pitch_list[index] = temp
                    except:
                        pass
            elif command[1].direction == "down":
                if force_initial_octavation is True:
                    if not isinstance(pitch_list[index], list):
                        pitch_list[index] = abjad.NamedInterval("-P8").transpose(
                            pitch_list[index]
                        )
                    else:
                        temp = []
                        for pitch in pitch_list[index]:
                            temp.append(abjad.NamedInterval("-P8").transpose(pitch))
                        pitch_list[index] = temp
                else:
                    try:
                        assert -1 < index - 1
                        if not isinstance(pitch_list[index], list):
                            while (
                                get_centroid(pitch_list[index - 1]) < pitch_list[index]
                            ):
                                pitch_list[index] = abjad.NamedInterval(
                                    "-P8"
                                ).transpose(pitch_list[index])
                        else:
                            centroid = get_centroid(pitch_list[index])
                            while get_centroid(pitch_list[index - 1]) < centroid:
                                temp = []
                                centroid = abjad.NamedInterval("-P8").transpose(
                                    centroid
                                )
                                for pitch in pitch_list[index]:
                                    temp.append(
                                        abjad.NamedInterval("-P8").transpose(pitch)
                                    )
                                pitch_list[index] = temp
                    except:
                        pass
            elif command[1].direction == "neutral":
                pitch_list[index] = pitch_list[index]
            else:
                raise Exception("Must be up, down, or neutral.")
            gotten_register = get_register(
                get_centroid(pitch_list[index]), command[1].following_treatment_range
            )
            if command[1].following_treatment_reference == "previous alteration":
                for index in continuation_indices:
                    if not isinstance(pitch_list[index], list):
                        pitch_list[index] = transpose_from_range(
                            pitch_list[index], gotten_register
                        )
                    else:
                        temp = []
                        for pitch_ in pitch_list[index]:
                            temp.append(transpose_from_range(pitch_, gotten_register))
                        pitch_list[index] = temp
            elif command[1].following_treatment_reference == "previous pitch":
                for index in continuation_indices:
                    if not isinstance(pitch_list[index], list):
                        pitch_list[index] = transpose_from_range(
                            pitch_list[index], gotten_register
                        )
                    else:
                        temp = []
                        for pitch_ in pitch_list[index]:
                            temp.append(transpose_from_range(pitch_, gotten_register))
                        pitch_list[index] = temp
                    gotten_register = get_register(
                        get_centroid(pitch_list[index]),
                        command[1].following_treatment_range,
                    )
            else:
                raise Exception("Must be previous alteration or previous pitch.")
        except:
            raise Exception("SOMETHING WENT WRONG")

    elif isinstance(command[0], (list, tuple)):
        if isinstance(command[0], tuple):
            indices = [_ for _ in range(command[0][0], command[0][1])]
        else:
            indices = command[0]
        continuation = pitch_list[indices[-1] + 1 :]
        continuation_indices = [indices[-1] + 1 + _ for _ in range(len(continuation))]
        for i, index in enumerate(indices):
            if command[1].direction == "up":
                if i == 0:
                    if force_initial_octavation is True:
                        if not isinstance(pitch_list[index], list):
                            pitch_list[index] = abjad.NamedInterval("+P8").transpose(
                                pitch_list[index]
                            )
                        else:
                            temp = []
                            for p_ in pitch_list[index]:
                                temp.append(abjad.NamedInterval("+P8").transpose(p_))
                            pitch_list[index] = temp
                    else:
                        try:
                            assert -1 < index - 1
                            if not isinstance(pitch_list[index], list):
                                while pitch_list[index] < get_centroid(
                                    pitch_list[index - 1]
                                ):
                                    pitch_list[index] = abjad.NamedInterval(
                                        "+P8"
                                    ).transpose(pitch_list[index])
                            else:
                                centroid = get_centroid(pitch_list[index])
                                while centroid < get_centroid(pitch_list[index - 1]):
                                    temp = []
                                    centroid = abjad.NamedInterval("+P8").transpose(
                                        centroid
                                    )
                                    for p_ in pitch_list[index]:
                                        temp.append(
                                            abjad.NamedInterval("+P8").transpose(p_)
                                        )
                                    pitch_list[index] = temp
                        except:
                            pass
                else:
                    if not isinstance(pitch_list[index], list):
                        while pitch_list[index] < get_centroid(pitch_list[index - 1]):
                            pitch_list[index] = abjad.NamedInterval("+P8").transpose(
                                pitch_list[index]
                            )
                    else:
                        centroid = get_centroid(pitch_list[index])
                        while centroid < get_centroid(pitch_list[index - 1]):
                            centroid = abjad.NamedInterval("+P8").transpose(centroid)
                            temp = []
                            for p_ in pitch_list[index]:
                                temp.append(abjad.NamedInterval("+P8").transpose(p_))
                            pitch_list[index] = temp

            elif command[1].direction == "down":
                if i == 0:
                    if force_initial_octavation is True:
                        if not isinstance(pitch_list[index], list):
                            pitch_list[index] = abjad.NamedInterval("-P8").transpose(
                                pitch_list[index]
                            )
                        else:
                            temp = []
                            for p_ in pitch_list[index]:
                                temp.append(abjad.NamedInterval("-P8").transpose(p_))
                            pitch_list[index] = temp
                    else:
                        try:
                            assert -1 < index - 1
                            if not isinstance(pitch_list[index], list):
                                while (
                                    get_centroid(pitch_list[index - 1])
                                    < pitch_list[index]
                                ):
                                    pitch_list[index] = abjad.NamedInterval(
                                        "-P8"
                                    ).transpose(pitch_list[index])
                            else:
                                centroid = get_centroid(pitch_list[index])
                                while get_centroid(pitch_list[index - 1]) < centroid:
                                    temp = []
                                    centroid = abjad.NamedInterval("-P8").transpose(
                                        centroid
                                    )
                                    for p_ in pitch_list[index]:
                                        temp.append(
                                            abjad.NamedInterval("-P8").transpose(p_)
                                        )
                                    pitch_list[index] = temp
                        except:
                            pass
                else:
                    if not isinstance(pitch_list[index], list):
                        while get_centroid(pitch_list[index - 1]) < pitch_list[index]:
                            pitch_list[index] = abjad.NamedInterval("-P8").transpose(
                                pitch_list[index]
                            )
                    else:
                        centroid = get_centroid(pitch_list[index])
                        while get_centroid(pitch_list[index - 1]) < centroid:
                            temp = []
                            centroid = abjad.NamedInterval("-P8").transpose(centroid)
                            for p_ in pitch_list[index]:
                                temp.append(abjad.NamedInterval("-P8").transpose(p_))
                            pitch_list[index] = temp
            elif command[1].direction == "neutral":
                pitch_list[index] = pitch_list[index]
            else:
                raise Exception("Must be up, down, or neutral.")
        gotten_register = get_register(
            get_centroid(pitch_list[indices[-1]]), command[1].following_treatment_range
        )
        if command[1].following_treatment_reference == "previous alteration":
            for index in continuation_indices:
                if not isinstance(pitch_list[index], list):
                    pitch_list[index] = transpose_from_range(
                        pitch_list[index], gotten_register
                    )
                else:
                    temp = []
                    for p_ in pitch_list[index]:
                        temp.append(transpose_from_range(p_, gotten_register))
                    pitch_list[index] = temp
        elif command[1].following_treatment_reference == "previous pitch":
            for index in continuation_indices:
                if not isinstance(pitch_list[index], list):
                    pitch_list[index] = transpose_from_range(
                        pitch_list[index], gotten_register
                    )
                else:
                    temp = []
                    for p_ in pitch_list[index]:
                        temp.append(transpose_from_range(pitch_, gotten_register))
                    pitch_list[index] = temp
                gotten_register = get_register(
                    get_centroid(pitch_list[index]),
                    command[1].following_treatment_range,
                )
        else:
            raise Exception("Must be previous alteration or previous pitch.")

    else:
        raise Exception("Must be of type int, list, or tuple.")

    return pitch_list


def contour(
    ties, *commands, starting_range=abjad.PitchRange("[c', c'')")
):  # starting range should only be one octave!
    ties = abjad.select.logical_ties(ties, pitched=True)
    gotten_pitches = [list(abjad.get.pitches(tie)) for tie in ties]
    pitches = []
    for pitch in gotten_pitches:
        if len(pitch) == 1:
            ranged_pitch = transpose_from_range(pitch[0], starting_range)
            pitches.append(ranged_pitch)
        elif 1 < len(pitch):
            temp = []
            for pitch_ in pitch:
                ranged_pitch = transpose_from_range(pitch_, starting_range)
                temp.append(ranged_pitch)
            pitches.append(temp)
    for command in commands:
        pitches = do_contouring(pitches, command)
    for tie, pitch in zip(ties, pitches):
        for leaf in tie:
            if isinstance(leaf, abjad.Note):
                leaf.written_pitch = pitch
            elif isinstance(leaf, abjad.Chord):
                leaf.written_pitches = pitch


def carceri_pitches(
    melodic_series=[11, 10, 4, 6, 5, 7, 1, 3, 2, 0, 9, 8],
    *,
    source_chord=["b", "ds'", "fs'", "bf'", "ef''", "a''", "c'''", "g'''"],
    reordering_series=[
        "af'",
        "g'",
        "cs'",
        "ef'",
        "d'",
        "e'",
        "bf'",
        "c'",
        "b'",
        "a'",
        "fs'",
        "f'",
    ],
    reverse_reordering_stack=True,
):
    s = Sequence(
        [abjad.NumberedPitch(abjad.NamedPitch(_)).number for _ in source_chord]
    )
    if reordering_series is not None:
        order = s.order_pitch_sequence_by_tonerow(
            [abjad.NumberedPitch(abjad.NamedPitch(_)).number for _ in reordering_series]
        )
    if reverse_reordering_stack:
        order = order.reverse()
    vertical_stack = order.stack_pitches()
    melody = vertical_stack.order_pitch_sequence_by_tonerow(
        melodic_series,
        return_pitch_classes=False,
        prefer_lowest_pitch=True,
    )
    return [_ for _ in melody]


class TonnetzChord:
    def __init__(self, bottom=0, middle=4, top=7, klang=abjad.UP, exponential=False):
        if exponential is False:
            self.bottom = abjad.NumberedPitchClass(bottom).number
            self.middle = abjad.NumberedPitchClass(middle).number
            self.top = abjad.NumberedPitchClass(top).number
        else:
            self.bottom = RatioClassSet([quicktions.Fraction(bottom)])[
                0
            ]  # constrain to range!
            self.middle = RatioClassSet([quicktions.Fraction(middle)])[0]
            self.top = RatioClassSet([quicktions.Fraction(top)])[0]
        if exponential is False:
            self.intervals = [self.middle - self.bottom, self.top - self.middle]
            self.compound_interval = sum(self.intervals)
        else:
            self.intervals = [self.middle / self.bottom, self.top / self.middle]
            self.compound_interval = self.intervals[0] * self.intervals[1]
        try:
            assert klang is abjad.UP or klang is abjad.DOWN
            self.klang = klang
        except:
            raise Exception(
                f"the value of klang must be abjad.UP or abjad.DOWN not {klang}"
            )
        self.exponential = exponential

    def __call__(self, operations=["p", "l", "r"], as_lists=True):
        out = [self]
        for operation in operations:
            if len(operation) == 1:
                if operation == "h":
                    out.append(out[-1].hexpole())
                elif operation == "l":
                    out.append(out[-1].leittonwechsel())
                elif operation == "n":
                    out.append(out[-1].nebenverwandt())
                elif operation == "o":
                    out.append(out[-1].octpole())
                elif operation == "p":
                    out.append(out[-1].parallel())
                elif operation == "r":
                    out.append(out[-1].relative())
                elif operation == "s":
                    out.append(out[-1].slide())
                else:
                    raise Exception(
                        f"Operations must be h, l, n, o, p, r, or s not {operation}."
                    )
            else:
                print(out[-1])
                temp_list = out[-1]([_ for _ in operation], as_lists=False)
                print(temp_list)
                final_result = temp_list[-1]
                print(final_result)
                out.append(final_result)
                print("done")
        if as_lists is True:
            out = [_.to_list() for _ in out]
        return out

    def hexpole(self):
        step_1 = self.leittonwechsel()
        step_2 = step_1.parallel()
        step_3 = step_2.leittonwechsel()
        return step_3

    def leittonwechsel(self):
        if self.klang is abjad.UP:
            if self.exponential is False:
                new_chord = TonnetzChord(
                    bottom=self.middle,
                    middle=self.top,
                    top=self.bottom + self.intervals[0] + self.compound_interval,
                    klang=abjad.DOWN,
                )
            else:
                new_chord = TonnetzChord(
                    bottom=self.middle,
                    middle=self.top,
                    top=self.bottom * self.intervals[0] * self.compound_interval,
                    klang=abjad.DOWN,
                    exponential=True,
                )
        else:
            if self.exponential is False:
                new_chord = TonnetzChord(
                    bottom=self.top - self.compound_interval - self.intervals[1],
                    middle=self.bottom,
                    top=self.middle,
                    klang=abjad.UP,
                )
            else:
                new_chord = TonnetzChord(
                    bottom=self.top / self.compound_interval / self.intervals[1],
                    middle=self.bottom,
                    top=self.middle,
                    klang=abjad.UP,
                    exponential=True,
                )
        return new_chord

    def nebenverwandt(self):
        step_1 = self.relative()
        step_2 = step_1.leittonwechsel()
        step_3 = step_2.parallel()
        return step_3

    def octpole(self):
        step_1 = self.parallel()
        step_2 = step_1.relative()
        step_3 = step_2.parallel()
        step_4 = step_3.relative()
        return step_4

    def parallel(self):
        if self.klang is abjad.UP:
            if self.exponential is False:
                new_chord = TonnetzChord(
                    bottom=self.bottom,
                    middle=self.middle + self.intervals[1] - self.intervals[0],
                    top=self.top,
                    klang=abjad.DOWN,
                )
            else:
                new_chord = TonnetzChord(
                    bottom=self.bottom,
                    middle=self.middle * self.intervals[1] / self.intervals[0],
                    top=self.top,
                    klang=abjad.DOWN,
                    exponential=True,
                )
        else:
            if self.exponential is False:
                new_chord = TonnetzChord(
                    bottom=self.bottom,
                    middle=self.middle - self.intervals[0] + self.intervals[1],
                    top=self.top,
                    klang=abjad.UP,
                )
            else:
                new_chord = TonnetzChord(
                    bottom=self.bottom,
                    middle=self.middle / self.intervals[0] * self.intervals[1],
                    top=self.top,
                    klang=abjad.UP,
                    exponential=True,
                )
        return new_chord

    def relative(self):
        if self.klang is abjad.UP:
            if self.exponential is False:
                new_chord = TonnetzChord(
                    bottom=self.top - self.compound_interval - self.intervals[1],
                    middle=self.bottom,
                    top=self.middle,
                    klang=abjad.DOWN,
                )
            else:
                new_chord = TonnetzChord(
                    bottom=self.top / self.compound_interval / self.intervals[1],
                    middle=self.bottom,
                    top=self.middle,
                    klang=abjad.DOWN,
                    exponential=True,
                )
        else:
            if self.exponential is False:
                new_chord = TonnetzChord(
                    bottom=self.middle,
                    middle=self.top,
                    top=self.bottom + self.compound_interval + self.intervals[0],
                    klang=abjad.UP,
                )
            else:
                new_chord = TonnetzChord(
                    bottom=self.middle,
                    middle=self.top,
                    top=self.bottom * self.compound_interval * self.intervals[0],
                    klang=abjad.UP,
                    exponential=True,
                )
        return new_chord

    def slide(self):
        step_1 = self.leittonwechsel()
        step_2 = step_1.parallel()
        step_3 = step_2.relative()
        return step_3

    def to_list(self):
        out = [self.bottom, self.middle, self.top]
        return out
