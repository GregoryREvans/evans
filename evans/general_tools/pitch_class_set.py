import fractions


def return_pitch_class_set(pitches):
    """
    return_pitch_class_set([15, 10, 8, -5, 3, 11])
    [0, 1, 3, 4, 8]

    """

    pitches = [i % 12 for i in pitches]
    pitches = set(pitches)
    pitches = sorted(pitches)
    pitches = list(pitches)
    if pitches[1] - pitches[0] > pitches[-1] - pitches[-2]:
        pitches.reverse()
        intervals = [pitches[0] - i for i in pitches]
    else:
        intervals = [i - pitches[0] for i in pitches]
    root = 0
    pitches = [root + interval for interval in intervals]
    return pitches


# print(return_pitch_class_set([15, 10, 8, -5, 3, 11]))
# rotate to smallest outer interval
# filter to inner intervals if outer intervals match
print(
    [
        str(x)
        for x in return_pitch_class_set(
            [
                fractions.Fraction(31, 2),
                10,
                fractions.Fraction(33, 4),
                -5,
                fractions.Fraction(36, 10),
                fractions.Fraction(113, 10),
            ]
        )
    ]
)
