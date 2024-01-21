import random
import abjad
import evans

def generate_basic_sequence(number_of_sets=5, size_of_sets=3, sizes=[1, 2, 3], seed=1):
    random.seed(seed)
    out = [None]
    for _ in range(number_of_sets):
        for x in range(size_of_sets):
            filtered_sequence = abjad.sequence.filter(sizes, lambda _: _ != out[-1])
            chosen_value = random.choice(filtered_sequence)
            out.append(chosen_value)
    out = out[1:]
    return out

def generate_basic_transpositions(length, intervals=["+P1", "+P8", "-P8"], seed=1):
    random.seed(seed)
    out = []
    for _ in range(length):
        chosen_value = random.choice(intervals)
        out.append(chosen_value)
    return out

def generate_basic_contour(starting_pitch=12, interval_sequence=None, seed=1):
    random.seed(seed)
    out = [starting_pitch]
    for interval in interval_sequence:
        direction = random.choice([abjad.UP, abjad.DOWN])
        if direction is abjad.DOWN:
            interval = 0 - interval
        out.append(out[-1] + interval)
    return out

def generate_octavated_sequence(
    number_of_sets=5,
    size_of_sets=3,
    starting_pitch=12,
    sizes=[1, 2, 3],
    intervals=["+P1", "+P8", "-P8"],
    interval_seed=1,
    contour_seed=1,
    octave_seed=1,
):
    octavated_pitches = []

    interval_sequence = generate_basic_sequence(number_of_sets, size_of_sets, sizes, interval_seed)

    pitch_sequence = generate_basic_contour(starting_pitch, interval_sequence, contour_seed)

    classed_s = [abjad.NumberedPitch(_) for _ in pitch_sequence]

    transpositions = generate_basic_transpositions(len(classed_s), intervals, octave_seed)

    for pitch, transposition in zip(classed_s, transpositions):
        new_pitch = abjad.NamedInterval(transposition).transpose(pitch)
        octavated_pitches.append(new_pitch)

    return octavated_pitches

pitches = generate_octavated_sequence(
    number_of_sets=5,
    size_of_sets=3,
    starting_pitch=12,
    sizes=[1, 2, 3],
    intervals=["+P1", "+P8", "-P8"],
    interval_seed=1,
    contour_seed=1,
    octave_seed=1,
)

s = abjad.Staff([abjad.Note("c'32") for _ in range(len(pitches))])
handler = evans.PitchHandler([float(_) for _ in pitches], forget=False)
handler(s)
abjad.show(s)

### This octavation system seems to produce overly chaotic voicings
### Instead of encapsulating the whole process into a SINGLE function,
### maybe deploy them individually in order to produce octavations in different way
### IDEA 1: choose octavation pattern from finite list of set of patterns
### IDEA 2: use a markov chain to constrain likelihood of register change and whether it stays in the changed register
### IDEA 3: Keep as is, just add more intervals by hand in order to weight the system
###
### Performing each operation separately allows user to create interval sequence, pitch sequence, or octave sequence by hand
### Any combination of by-hand composing and generative composing could be valuable.
