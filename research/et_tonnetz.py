from fractions import Fraction

import abjad
import evans

# tonnetz = evans.TonnetzChord(0, 4, 7, klang=abjad.UP)
# tonnetz_sequence = tonnetz(["p", "l", "r", "p", "l", "r"])
# compound_chords = [set(evans.flatten(_)) for _ in evans.consort.iterate_nwise(tonnetz_sequence, 2)]
# staff = abjad.Staff([abjad.Chord(_, (1, 1)) for _ in compound_chords])
# abjad.show(staff)

tonnetz = evans.TonnetzChord(
    Fraction(1, 1), Fraction(5, 4), Fraction(3, 2), klang=abjad.UP, exponential=True
)
tonnetz_sequence = tonnetz(["p", "l", "r", "p", "l", "r"])
compound_chords = [
    list(set(evans.flatten(_)))
    for _ in evans.consort.iterate_nwise(tonnetz_sequence, 2)
]
handler = evans.PitchHandler(compound_chords, as_ratios=True)
staff = abjad.Staff([abjad.Note(0, (1, 1)) for _ in tonnetz_sequence])
handler(staff)

score = abjad.Score([staff])

moment = "#(ly:make-moment 1 10)"
abjad.setting(score).proportional_notation_duration = moment

block = abjad.Block(name="score")
block.items.append(score)

style = '"dodecaphonic"'
layout = abjad.Block(name="layout")
layout.items.append(rf"\accidentalStyle {style}")

file = abjad.LilyPondFile(
    items=[
        r'\include "/Users/gregoryevans/abjad/abjad/_stylesheets/ekmelos-ji-accidental-markups.ily"',
        r'\include "/Users/gregoryevans/scores/polillas/polillas/build/score_stylesheet.ily"',
        layout,
        block,
    ]
)

# evans.make_sc_file(
#     score=score,
#     tempo=metronome_mark,
#     current_directory=pathlib.Path(__file__).parent,
# )

# abjad.mutate.transpose(group_2, abjad.NamedInterval("+P8"))

abjad.show(file)
