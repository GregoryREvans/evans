"""
Pitch functions.
"""
import abjad
import quicktions

from .sequence import flatten


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


def to_nearest_eighth_tone(number):
    number = round(float(number) * 4) / 4
    div, mod = divmod(number, 1)
    if mod == 0.75:
        div += 0.75
    elif mod == 0.5:
        div += 0.5
    elif mod == 0.25:
        div += 0.25
    return abjad.mathx.integer_equivalent_number_to_integer(div)


def to_nearest_quarter_tone(number):
    number = round(float(number) * 4) / 4
    div, mod = divmod(number, 1)
    if mod == 0.75:
        div += 1
    elif mod == 0.5:
        div += 0.5
    return abjad.mathx.integer_equivalent_number_to_integer(div)


def to_nearest_sixth_tone(number):
    semitones = quicktions.Fraction(int(round(6 * number)), 6)
    if semitones.denominator == 6:
        semitones = quicktions.Fraction(int(round(3 * number)), 3)
    return abjad.mathx.integer_equivalent_number_to_integer(semitones)


def to_nearest_third_tone(number):
    semitones = quicktions.Fraction(int(round(3 * number)), 3)
    if semitones.denominator == 3:
        semitones = quicktions.Fraction(int(round(1.5 * number)), 1.5)
    return abjad.mathx.integer_equivalent_number_to_integer(semitones)


def to_nearest_twelfth_tone(number):
    semitones = quicktions.Fraction(int(round(12 * number)), 12)
    if semitones.denominator == 12:
        semitones = quicktions.Fraction(int(round(6 * number)), 6)
    return abjad.mathx.integer_equivalent_number_to_integer(semitones)


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
        LogicalTie([Note("d'8")])
        LogicalTie([Note("c'4")])
        LogicalTie([Note("cs'4")])
        LogicalTie([Note("d'8")])
        LogicalTie([Note("d'8")])
        LogicalTie([Note("cs'4")])
        LogicalTie([Note("c'2")])
        LogicalTie([Note("d'8")])
        LogicalTie([Note("d'8")])
        LogicalTie([Note("cs'2")])
        LogicalTie([Note("d'8")])
        LogicalTie([Note("d'8")])
        LogicalTie([Note("c'4")])
        LogicalTie([Note("d'8")])

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
        >>> handler = evans.PitchHandler(
        ...     pitch_list=[0, 1, 2, 3, 4],
        ...     continuous=True,
        ...     to_ties=True,
        ... )
        >>> vm_ties = evans.return_vertical_moment_ties(score)
        >>> for i, tie in enumerate(vm_ties):
        ...     string = f"{i}"
        ...     markup = abjad.Markup(string, direction=abjad.Up)
        ...     abjad.attach(markup, tie[0])
        ...
        >>> handler(vm_ties)
        >>> abjad.show(score) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(score))
            \new Score
            <<
                \new Staff
                {
                    cs'4
                    ^ \markup { 1 }
                    cs'2
                    ^ \markup { 6 }
                    d'4
                    ^ \markup { 12 }
                }
                \new Staff
                {
                    d'4
                    ^ \markup { 2 }
                    c'4
                    ^ \markup { 5 }
                    e'2
                    ^ \markup { 9 }
                }
                \new Staff
                {
                    c'8
                    ^ \markup { 0 }
                    ef'8
                    ^ \markup { 3 }
                    e'8
                    ^ \markup { 4 }
                    d'8
                    ^ \markup { 7 }
                    ef'8
                    ^ \markup { 8 }
                    c'8
                    ^ \markup { 10 }
                    cs'8
                    ^ \markup { 11 }
                    ef'8
                    ^ \markup { 13 }
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
        >>> handler = evans.PitchHandler(pitch_list=[0, 1, 2, 3, 4], continuous=True)
        >>> for i, tie in enumerate(evans.return_vertical_moment_ties(score)):
        ...     string = f"{i}"
        ...     markup = abjad.Markup(string, direction=abjad.Up)
        ...     abjad.attach(markup, tie[0])
        ...     handler(tie)
        ...
        >>> abjad.show(score) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(score))
            \new Score
            <<
                \new Staff
                {
                    d'4
                    ^ \markup { 2 }
                    ~
                    d'2
                    cs'4
                    ^ \markup { 11 }
                }
                \new Staff
                {
                    cs'4
                    ^ \markup { 1 }
                    c'4
                    ^ \markup { 5 }
                    ef'2
                    ^ \markup { 8 }
                }
                \new Staff
                {
                    c'8
                    ^ \markup { 0 }
                    ef'8
                    ^ \markup { 3 }
                    e'8
                    ^ \markup { 4 }
                    cs'8
                    ^ \markup { 6 }
                    d'8
                    ^ \markup { 7 }
                    e'8
                    ^ \markup { 9 }
                    c'8
                    ^ \markup { 10 }
                    d'8
                    ^ \markup { 12 }
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
                [_ for _ in abjad.select(new_moment_notes).logical_ties()]
            )
            new_moments.append(new_moment)
    flat_moments = flatten(new_moments)
    flat_moments.sort(key=lambda _: abjad.inspect(_).timespan())
    return flat_moments
