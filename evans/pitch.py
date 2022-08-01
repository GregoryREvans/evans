"""
Pitch functions.
"""
import collections
import math

import abjad
import baca
import quicktions

from .sequence import RatioSegment, flatten


class JIPitch(abjad.Pitch):
    r"""

    Just Intonation Pitch

    .. container:: example

        >>> pitch = evans.JIPitch("c'", "7/4", with_quarter_tones=True)
        >>> note = abjad.Note(pitch, (1, 4))
        >>> mark = abjad.Markup(fr"\markup {str(pitch.deviation)}", direction=abjad.UP)
        >>> abjad.attach(mark, note)
        >>> abjad.show(note) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(note))
            aqs'4
            ^ \markup 19

    .. container:: example

        >>> pitch = evans.JIPitch("c'", "7/4", with_quarter_tones=False)
        >>> note = abjad.Note(pitch, (1, 4))
        >>> mark = abjad.Markup(fr"\markup {str(pitch.deviation)}", direction=abjad.UP)
        >>> abjad.attach(mark, note)
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
    mark = abjad.Markup(rf"\markup \center-align {cent_string}", direction=abjad.UP)
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
        ...     markup = abjad.Markup(fr"\markup {string}", direction=abjad.UP)
        ...     abjad.attach(markup, tie[0])
        ...
        >>> handler(vm_ties)
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
                    ^ \markup 1
                    cs'2
                    ^ \markup 6
                    d'4
                    ^ \markup 12
                }
                \new Staff
                {
                    d'4
                    ^ \markup 2
                    c'4
                    ^ \markup 5
                    e'2
                    ^ \markup 9
                }
                \new Staff
                {
                    c'8
                    ^ \markup 0
                    ef'8
                    ^ \markup 3
                    e'8
                    ^ \markup 4
                    d'8
                    ^ \markup 7
                    ef'8
                    ^ \markup 8
                    c'8
                    ^ \markup 10
                    cs'8
                    ^ \markup 11
                    ef'8
                    ^ \markup 13
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
        ...     markup = abjad.Markup(fr"\markup {string}", direction=abjad.UP)
        ...     abjad.attach(markup, tie[0])
        ...     handler(tie)
        ...
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
                    ^ \markup 2
                    ~
                    d'2
                    cs'4
                    ^ \markup 11
                }
                \new Staff
                {
                    cs'4
                    ^ \markup 1
                    c'4
                    ^ \markup 5
                    ef'2
                    ^ \markup 8
                }
                \new Staff
                {
                    c'8
                    ^ \markup 0
                    ef'8
                    ^ \markup 3
                    e'8
                    ^ \markup 4
                    cs'8
                    ^ \markup 6
                    d'8
                    ^ \markup 7
                    e'8
                    ^ \markup 9
                    c'8
                    ^ \markup 10
                    d'8
                    ^ \markup 12
                }
            >>

    """
    moments = [_ for _ in abjad.iterate_vertical_moments(score)]
    new_moments = []
    for i, moment in enumerate(moments):
        new_moment = []
        new_moment_notes = []
        for note in moment.start_notes:
            new_moment_notes.append(note)
        if 0 < len(new_moment_notes):
            new_moment.append(
                [_ for _ in abjad.select.logical_ties(new_moment_notes)]
            )
            new_moments.append(new_moment)
    flat_moments = flatten(new_moments)
    flat_moments.sort(key=lambda _: abjad.get.timespan(_))
    return flat_moments


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


class Loop(abjad.CyclicTuple):

    ### CLASS VARIABLES ###

    __slots__ = ("_intervals", "_items")

    ### INITIALIZER ###

    def __init__(self, items=None, *, intervals=None):
        if items is not None:
            assert isinstance(items, collections.abc.Iterable), repr(items)
            items = [abjad.NamedPitch(_) for _ in items]
            items = abjad.CyclicTuple(items)
        abjad.CyclicTuple.__init__(self, items=items)
        if intervals is not None:
            assert isinstance(items, collections.abc.Iterable), repr(items)
            intervals = abjad.CyclicTuple(intervals)
        self._intervals = intervals

    ### SPECIAL METHODS ###

    def __getitem__(self, i) -> abjad.Pitch:
        if isinstance(i, slice):
            raise NotImplementedError
        iteration = i // len(self)
        if self.intervals is None:
            transposition = 0
        else:
            transposition = sum(self.intervals[:iteration])
        pitch_ = abjad.CyclicTuple(list(self))[i]
        pitch = type(pitch_)(pitch_.number + transposition)
        return pitch

    ### PUBLIC PROPERTIES ###

    @property
    def intervals(self):
        return self._intervals

    @property
    def items(self):
        return self._items


def loop(
    items: baca.typing.Sequence,
    intervals: baca.typing.Sequence,
    selector=lambda _: baca.select.plts(_, exclude=baca.enums.HIDDEN),
) -> baca.PitchCommand:
    loop = Loop(items=items, intervals=intervals)
    return baca.pitches(loop, selector=selector)


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
        style="#'harmonic",
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
            are_cautionary = [None] * len(written_pitches)
        if not are_forced:
            are_forced = [None] * len(written_pitches)
        if not are_parenthesized:
            are_parenthesized = [None] * len(written_pitches)
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

        self.written_pitches = abjad.PitchSegment(
            items=(note_head.written_pitch for note_head in self._note_heads),
            item_class=abjad.NamedPitch,
        )

        if self.is_parenthesized:
            first_head = self._note_heads[0]
            first_head.is_parenthesized = self.is_parenthesized
            abjad.tweak(self._note_heads[0]).ParenthesesItem__font_size = -4

        if with_sounding_pitch is True:
            written_pitch_list = [_ for _ in written_pitches]
            written_pitch_list.append(self.sounding_pitch())
            self.written_pitches = abjad.PitchSegment(written_pitch_list)

        second_head = self._note_heads[1]
        abjad.tweak(second_head).style = self.style

        if len(self._note_heads) == 3:
            third_head = self._note_heads[2]
            third_head.is_parenthesized = True
            abjad.tweak(third_head).font_size = -4

    ### PUBLIC METHODS ###

    def sounding_pitch(self):
        r"Returns the sounding pitch of the harmonic as an |abjad.Pitch|."
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
