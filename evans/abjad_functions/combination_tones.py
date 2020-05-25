from fractions import Fraction

import abjad


def combination_tones(pitches=[0, 5, 7], depth=1):
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


# print(combination_tones(pitches=[8.25, 18.75, 23.5], depth=1))
# print(combination_tones(pitches=[7.75, 19, 25.25, 28.5], depth=1))
# combs = combination_tones(pitches=[7.75, 8.25, 18.75, 19, 23.5, 25.25, 28.5], depth=1)
# staff = abjad.Staff([abjad.Note() for _ in combs])
# for note, pitch in zip(abjad.select(staff).leaves(), combs):
#     note.written_pitch = pitch
# abjad.show(staff)

# print(
#     herz_combination_tone_ratios(
#     fundamental=261.625565,
#     pitches=[
#         327.03195625,
#         392.43834749999996
#         ],
#     depth=3,
#     )
# )
