import abjad
import abjadext.rmakers
#an example of iterating
rhythm_maker = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[1, 2, 1, 1, 4, 1, 1],
        denominator=16,
        ),
    )

divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
selections = rhythm_maker(divisions)
pitches = [0, 11, 5, 15, 6, 7, 1, -5, 26, 0] * 2

logical_ties = [tie for tie in abjad.iterate(selections).logical_ties(pitched=True)]
for tie, pitch in zip(logical_ties, pitches):
    for leaf in tie:
        leaf.written_pitch = pitch

lilypond_file = abjad.LilyPondFile.rhythm(
    selections,
    divisions,
    )

abjad.show(lilypond_file)
