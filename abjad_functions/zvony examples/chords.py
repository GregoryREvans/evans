import abjad
import abjadext.rmakers

# you can use leafmaker to make notes and chords via rmaker output
rhythm_maker = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(counts=[1, 2, 1, 1, 4, 1, 1], denominator=16)
)
divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
selections = rhythm_maker(divisions)
pitches = [0, [11, 5], 15, 6, 7, [1, -5], 26, 0] * 2
durations = []
for leaf in abjad.iterate(selections).leaves(pitched=True):
    duration = abjad.inspect(leaf).duration()
    durations.append(duration)

maker = abjad.LeafMaker()
leaves = maker(pitches, durations)
staff = abjad.Staff(leaves)
abjad.show(staff)
