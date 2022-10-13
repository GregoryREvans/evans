import abjad
import evans

s = evans.Sequence.equal_divisions(440, 3 / 2, 31)

temp_val = s[5]

p = abjad.NumberedPitch.from_hertz(temp_val)

p_cents = evans.Sequence.equal_divisions(p.hertz, (2 ** (1 / 12)), 100)


def return_nearest_approximation(target, candidates):
    nearest_approximation = candidates[0]
    difference_size = abs(candidates[0] - target)
    for candidate in candidates[1:]:
        test_val = abs(candidate - target)
        if test_val < difference_size:
            nearest_approximation = candidate
            difference_size = test_val
    return nearest_approximation, candidates.index(nearest_approximation)


nearest = return_nearest_approximation(temp_val, p_cents)

print(f"Real Herts: {temp_val}\n")
print(f"Semitone Hertz: {p.hertz}\n")
print(f"Semitone Cents in Hertz: {p_cents}\n")
print(f"Calculated Nearest Approximation: {nearest[0]}\n")
print(f"Deviation in cents: {nearest[1]}")
