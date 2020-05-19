from fractions import Fraction
from math import log10


def hertz_to_ratio(value_1, value_2):
    val = value_1 / value_2
    return Fraction(val).limit_denominator(23)


def ratio_to_cents(ratio):
    log_ratio = log10(ratio)
    log_2 = 1200 / log10(2)
    return log_ratio * log_2


def return_difference(cents):
    ratio_dict = {
        "pythagorean_fifth": ratio_to_cents(ratio=(3 / 2)),
        "syntonic_comma": ratio_to_cents(ratio=(81 / 80)),
        "septimal_comma": ratio_to_cents(ratio=(64 / 63)),
        "eleven_limit_undecimal_quarter_tone": ratio_to_cents(ratio=(33 / 32)),
        "thirteen_limit_tridecimal_third_tone": ratio_to_cents(ratio=(27 / 26)),
        "seventeen_limit_schisma": ratio_to_cents(ratio=(256 / 255)),
        "nineteen_limit_schisma": ratio_to_cents(ratio=(513 / 512)),
        "twenty_three_limit_comma": ratio_to_cents(ratio=(736 / 729)),
    }
    temp = None
    for item, value in ratio_dict.items():
        if cents % value == 0.0:
            temp = (item, value)
    if temp is not None:
        return f"{cents / temp[1]} {temp[0]}s"
    else:
        return "Requires compound accidental"


print(hertz_to_ratio(660, 440))

print(ratio_to_cents(hertz_to_ratio(660, 440)))

print(return_difference(ratio_to_cents(hertz_to_ratio(660, 440))))

print(return_difference(ratio_to_cents(ratio=(7 / 4))))

print(return_difference(ratio_to_cents(ratio=(16 / 15))))

for ratio in [
    (1 / 1),
    (5 / 4),
    (3 / 2),
    (7 / 4),
    (11 / 8),
    (13 / 8),
    (17 / 6),
    (19 / 16),
]:  # requires pythagorean fifths with deviations?
    print(return_difference(ratio_to_cents(ratio)))

for ratio in [
    (3 / 2),
    (81 / 80),
    (64 / 63),
    (33 / 32),
    (27 / 26),
    (256 / 255),
    (513 / 512),
    (736 / 729),
]:
    print(return_difference(ratio_to_cents(ratio)))

print(return_difference(ratio_to_cents((9 / 4))))

print(return_difference(ratio_to_cents((24 / 23))))
