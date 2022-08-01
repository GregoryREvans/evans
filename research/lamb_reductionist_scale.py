import numpy
import abjad
import evans


def primes_below_n(n):
    sieve = numpy.ones(n // 3 + (n % 6 == 2), dtype=bool)
    for i in range(1, int(n ** 0.5) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[       k*k//3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)//3::2*k] = False
    return numpy.r_[2, 3, ((3 * numpy.nonzero(sieve)[0][1:] + 1) | 1)]

primes = primes_below_n(24)
print(primes)

integer_multipliers = [_ + 1 for _ in range(len(primes))]

integer_multipliers.reverse()
print(integer_multipliers)

# prime_multipliers = [_ for _ in primes]
# prime_multipliers.reverse()
# print(prime_multipliers)

mulitpliers = integer_multipliers

max = 200

primewise_multiples = []

for prime, multiplier in zip(primes, mulitpliers):
    print(prime, multiplier)
    cap_reached = False
    out = [prime]
    while cap_reached is False:
        test_case = out[-1] * multiplier
        print(test_case)
        if test_case in out:
            break
        if test_case < max:
            out.append(test_case)
            print("\nAPPENDED!\n\n")
        else:
            cap_reached = True
            primewise_multiples.append(out)
    continue

print(primewise_multiples)

union_spectrum = []
for sub_list in primewise_multiples:
    union_spectrum.extend(sub_list)

union_spectrum.sort()

print(union_spectrum)

def force_accidental(selections):
    ties = abjad.select.logical_ties(selections, pitched=True)
    for tie in ties:
        first_leaf = tie[0]
        if isinstance(first_leaf, abjad.Note):
            first_leaf.note_head.is_forced = True
        elif isinstance(first_leaf, abjad.Chord):
            heads = first_leaf.note_heads
            for head in heads:
                head.is_forced = True
        else:
            ex = f"Object must be of type {type(abjad.Note())} or {type(abjad.Chord())}"
            raise Exception(ex)

staff = abjad.Staff([abjad.Note("c,,,4") for _ in union_spectrum])
handler = evans.PitchHandler([f"{_}/1" for _ in union_spectrum], forget=False, as_ratios=True)
handler(staff)
staff.append(abjad.Rest("r4"))
clef = evans.ClefHandler(clef="bass", add_extended_clefs=True, add_ottavas=True,)
clef(staff)
force_accidental(staff)
score = abjad.Score([staff])
moment = "#(ly:make-moment 1 25)"
abjad.setting(score).proportional_notation_duration = moment
file = abjad.LilyPondFile(
    items=[
        r'\include "/Users/gregoryevans/abjad/abjad/_stylesheets/abjad.ily"',
        r'\include "/Users/gregoryevans/abjad/abjad/_stylesheets/ekmelos-ji-accidental-markups.ily"',
        score,
    ],
)
abjad.show(file)
