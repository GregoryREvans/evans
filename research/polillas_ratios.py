import pathlib
from fractions import Fraction

import abjad
import evans

###
###
###
maker = abjad.makers.make_leaves

tempo_pair = ((1, 4), 10)
metronome_mark = abjad.MetronomeMark(tempo_pair[0], tempo_pair[1])

source = ["1/1", "5/4", "11/8", "7/4", "3/2"]
triads = evans.tonnetz(
    source, "major", ["p", "l", "r", "r", "r7", "l7", "p", "l11", "r11", "p"]
)
# raise Exception(type(triads[0][0]))
# for triad in triads:
#     print(triad)

triads = [[str(x) for x in _] for _ in triads]

voice = abjad.Staff([abjad.Note("d'1") for _ in range(len(triads))])

handler = evans.PitchHandler(triads, forget=False, as_ratios=True)

handler(voice)

score = abjad.Score([voice])
# abjad.attach(metronome_mark, voice[0])


moment = "#(ly:make-moment 1 1)"
abjad.setting(score).proportional_notation_duration = moment

block = abjad.Block(name="score")
block.items.append(score)

style = '"dodecaphonic"'
layout = abjad.Block(name="layout")
layout.items.append(rf"\accidentalStyle {style}")

file = abjad.LilyPondFile(
    items=[
        r'\include "/Users/gregoryevans/abjad-ext-microtones/abjadext/microtones/lilypond/ekmelos-ji-accidental-markups.ily"',
        # r'\include "/Users/gregoryevans/scores/polillas/polillas/build/score_stylesheet.ily"',
        '#(set-default-paper-size "letterportrait")',
        "#(set-global-staff-size 16)",
        layout,
        block,
    ]
)

abjad.show(file)
