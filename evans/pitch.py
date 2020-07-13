import abjad
import quicktions


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
