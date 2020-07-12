from fractions import Fraction

import abjad


def beam_meter(components, meter, offset_depth, include_rests=True):
    r"""
    >>> pre_tuplet_notes = abjad.Staff("c'8 c'8 c'8")
    >>> tuplet = abjad.Tuplet((2, 3), "c'8 r8 c'8")
    >>> post_tuplet_notes = abjad.Staff("c'8 c'8 c'8")
    >>> staff = abjad.Staff()
    >>> for _ in [pre_tuplet_notes[:], tuplet, post_tuplet_notes[:]]:
    ...     staff.append(_)
    ...
    >>> evans.beam_meter(components=staff[:], meter=abjad.Meter((4, 4)), offset_depth=1)
    >>> abjad.f(staff)
    \new Staff
    {
        \override Staff.Stem.stemlet-length = 0.75
        c'8
        [
        \revert Staff.Stem.stemlet-length
        c'8
        ]
        c'8
        \times 2/3 {
            \override Staff.Stem.stemlet-length = 0.75
            c'8
            [
            r8
            \revert Staff.Stem.stemlet-length
            c'8
            ]
        }
        c'8
        \override Staff.Stem.stemlet-length = 0.75
        c'8
        [
        \revert Staff.Stem.stemlet-length
        c'8
        ]
    }

    """
    offsets = meter.depthwise_offset_inventory[offset_depth]
    offset_pairs = []
    for i, _ in enumerate(offsets[:-1]):
        offset_pair = [offsets[i], offsets[i + 1]]
        offset_pairs.append(offset_pair)
    initial_offset = abjad.inspect(components[0]).timespan().start_offset
    for i, pair in enumerate(offset_pairs):
        for i_, item in enumerate(pair):
            offset_pairs[i][i_] = item + initial_offset
    offset_timespans = [
        abjad.timespan(start_offset=pair[0], stop_offset=pair[1])
        for pair in offset_pairs
    ]

    tup_list = [tup for tup in abjad.select(components).components(abjad.Tuplet)]
    for t in tup_list:
        if (
            isinstance(abjad.inspect(t).parentage().components[1], abjad.Tuplet)
            is False
        ):
            abjad.beam(
                t[:],
                beam_rests=include_rests,
                stemlet_length=0.75,
                beam_lone_notes=False,
                selector=abjad.select().leaves(grace=False),
            )
        else:
            continue

    non_tup_list = []
    for leaf in abjad.select(components).leaves():
        if (
            isinstance(abjad.inspect(leaf).parentage().components[1], abjad.Tuplet)
            is False
        ):
            non_tup_list.append(leaf)

    beamed_groups = []
    for i in enumerate(offset_timespans):
        beamed_groups.append([])

    for i, span in enumerate(offset_timespans):
        for group in (
            abjad.select(non_tup_list[:])
            .leaves()
            .group_by(
                predicate=lambda x: abjad.inspect(x)
                .timespan()
                .happens_during_timespan(span)
            )
        ):
            if abjad.inspect(group).timespan().happens_during_timespan(span) is True:
                beamed_groups[i].append(group[:])

    for subgroup in beamed_groups:
        subgrouper = abjad.select(subgroup).group_by_contiguity()
        for beam_group in subgrouper:
            # if not all(isinstance(leaf, abjad.Rest) for leaf in beam_group)
            abjad.beam(
                beam_group[:],
                beam_rests=include_rests,
                stemlet_length=0.75,
                beam_lone_notes=False,
                selector=abjad.select().leaves(grace=False),
            )


def combination_tones(pitches=[0, 5, 7], depth=1):
    """
    >>> print(evans.combination_tones(pitches=[8.25, 18.75, 23.5], depth=1))
    [-2.0, 6.0, 8.0, 14.5, 19.0, 23.5, 26.0, 29.5, 33.5]

    >>> print(evans.combination_tones(pitches=[7.75, 19, 25.25, 28.5], depth=1))
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
    >>> print(
    ...     herz_combination_tone_ratios(
    ...     fundamental=261.625565,
    ...     pitches=[
    ...         327.03195625,
    ...         392.43834749999996
    ...         ],
    ...     depth=1,
    ...     )
    ... )
    ...
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
        returned_list.append(str(Fraction(freq / fundamental)))
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
    return abjad.mathtools.integer_equivalent_number_to_integer(div)


def to_nearest_quarter_tone(number):
    number = round(float(number) * 4) / 4
    div, mod = divmod(number, 1)
    if mod == 0.75:
        div += 1
    elif mod == 0.5:
        div += 0.5
    return abjad.mathtools.integer_equivalent_number_to_integer(div)


def to_nearest_sixth_tone(number):
    semitones = Fraction(int(round(6 * number)), 6)
    if semitones.denominator == 6:
        semitones = Fraction(int(round(3 * number)), 3)
    return abjad.mathtools.integer_equivalent_number_to_integer(semitones)


def to_nearest_third_tone(number):
    semitones = Fraction(int(round(3 * number)), 3)
    if semitones.denominator == 3:
        semitones = Fraction(int(round(1.5 * number)), 1.5)
    return abjad.mathtools.integer_equivalent_number_to_integer(semitones)


def to_nearest_twelfth_tone(number):
    semitones = Fraction(int(round(12 * number)), 12)
    if semitones.denominator == 12:
        semitones = Fraction(int(round(6 * number)), 6)
    return abjad.mathtools.integer_equivalent_number_to_integer(semitones)
