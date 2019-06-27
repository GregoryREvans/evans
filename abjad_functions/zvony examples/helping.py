import abjad
import abjadext.rmakers

rhythm_maker = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(counts=[1, 2, -1, 1, 4, 1, 1], denominator=16)
)

divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
time_signatures = [abjad.TimeSignature(pair) for pair in divisions]
print(time_signatures)
selections = rhythm_maker(divisions)

pitch_list = [0, 11, [5, 15], 6, 7, 1, -5, 26, 2] * 2
staff = abjad.Staff()
staff.extend(selections)
logical_ties = abjad.iterate(staff).logical_ties(pitched=True)

for pitch, logical_tie in zip(pitch_list, logical_ties):
    for old_leaf in logical_tie:
        if isinstance(pitch, int):
            old_leaf.written_pitch = pitch
        elif isinstance(pitch, list):
            new_leaf = abjad.Chord(pitch, old_leaf.written_duration)
            indicators = abjad.inspect(old_leaf).indicators()
            if indicators != None:
                for indicator in indicators:
                    abjad.attach(indicator, new_leaf)
            abjad.mutate(old_leaf).replace(new_leaf)

leaves = abjad.select(staff).leaves()
abjad.attach(time_signatures[0], leaves[0])
abjad.attach(time_signatures[1], leaves[5])
abjad.attach(time_signatures[2], leaves[10])
abjad.attach(time_signatures[3], leaves[13])

lilypond_file = abjad.LilyPondFile.new(staff)

abjad.show(lilypond_file)
