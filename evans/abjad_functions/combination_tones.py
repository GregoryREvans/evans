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


# print(combination_tones(pitches=[0, 5.25, 6.5], depth=2))
