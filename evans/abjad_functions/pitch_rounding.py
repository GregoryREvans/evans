import abjad
from fractions import Fraction


def to_nearest_quarter_tone(number):
    number = round(float(number) * 4) / 4
    div, mod = divmod(number, 1)
    if mod == 0.75:
        div += 1
    elif mod == 0.5:
        div += 0.5
    return abjad.mathtools.integer_equivalent_number_to_integer(div)


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


def to_nearest_third_tone(number):
    semitones = Fraction(int(round(3 * number)), 3)
    if semitones.denominator == 3:
        semitones = Fraction(int(round(1.5 * number)), 1.5)
    return abjad.mathtools.integer_equivalent_number_to_integer(semitones)


def to_nearest_sixth_tone(number):
    semitones = Fraction(int(round(6 * number)), 6)
    if semitones.denominator == 6:
        semitones = Fraction(int(round(3 * number)), 3)
    return abjad.mathtools.integer_equivalent_number_to_integer(semitones)


def to_nearest_twelfth_tone(number):
    semitones = Fraction(int(round(12 * number)), 12)
    if semitones.denominator == 12:
        semitones = Fraction(int(round(6 * number)), 6)
    return abjad.mathtools.integer_equivalent_number_to_integer(semitones)
