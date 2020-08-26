import abjad
from abjadext import microtones
from quicktions import Fraction

from .. import evans

print("calculating basic ratios")
fundamental_pitch = abjad.NumberedPitch(-9)
fundamental_hertz = fundamental_pitch.hertz
ratios = ["1/1", "2/1", "3/2", "5/3", "8/5", "13/8", "21/13"]
staff_1 = abjad.Staff([abjad.Note(fundamental_pitch, (1, 4)) for ratio in ratios])
for ratio, leaf in zip(ratios, abjad.select(staff_1).leaves()):
    microtones.tune_to_ratio(leaf.note_head, ratio)
    mark = abjad.Markup(ratio, direction=abjad.Up)
    abjad.attach(mark, leaf)
print("calculating combination tones")
ratios_to_hertz = [fundamental_hertz * Fraction(ratio) for ratio in ratios]

combination_ratios = evans.herz_combination_tone_ratios(
    fundamental=fundamental_hertz,
    pitches=ratios_to_hertz,
    depth=1,
)
combination_ratios = [
    "1/2",
    "5/8",
    "1",
    "3/2",
    "13/8",
    "2",
    "5/2",
    "21/8",
    "3",
    "25/8",
    "7/2",
]
for _ in ratios:
    print(fundamental_hertz * Fraction(_))
print("")
for _ in combination_ratios:
    print(fundamental_hertz * Fraction(_))
print("assembling combination tones")
staff_2 = abjad.Staff([abjad.Note(fundamental_pitch, (1, 4)) for ratio in ratios])
for ratio, leaf in zip(combination_ratios, abjad.select(staff_2).leaves()):
    microtones.tune_to_ratio(leaf.note_head, ratio)
    mark = abjad.Markup(ratio, direction=abjad.Up)
    abjad.attach(mark, leaf)
print("handling clefs")
handler = evans.ClefHandler(
    clef="bass",
    add_extended_clefs=True,
    add_ottavas=True,
)
handler(staff_1)
handler(staff_2)
print("preparing score")
score = abjad.Score([staff_1, staff_2])
print("preparing file")
lilypond_file = abjad.LilyPondFile.new(
    score,
    includes=[
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/default.ily",
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/microtones/ekmelos-ji-accidental-markups.ily",
    ],
)
style = '"dodecaphonic"'
lilypond_file.layout_block.items.append(fr"\accidentalStyle {style}")
print("rendering file")
abjad.show(lilypond_file)


###

print("calculating basic ratios")
ratios = ["1/1", "2/1", "5/2", "12/5", "169/70", "408/169"]
staff_1 = abjad.Staff([abjad.Note(fundamental_pitch, (1, 4)) for ratio in ratios])
for ratio, leaf in zip(ratios, abjad.select(staff_1).leaves()):
    microtones.tune_to_ratio(leaf.note_head, ratio)
    mark = abjad.Markup(ratio, direction=abjad.Up)
    abjad.attach(mark, leaf)
print("calculating combination tones")
ratios_to_hertz = [fundamental_hertz * Fraction(ratio) for ratio in ratios]

combination_ratios = evans.herz_combination_tone_ratios(
    fundamental=fundamental_hertz,
    pitches=ratios_to_hertz,
    depth=1,
)
combination_ratios = [
    "1",
    "2",
    "5/2",
    "3",
    "7/2",
    "9/2",
]
for _ in ratios:
    print(fundamental_hertz * Fraction(_))
print("")
for _ in combination_ratios:
    print(fundamental_hertz * Fraction(_))
print("assembling combination tones")
staff_2 = abjad.Staff([abjad.Note(fundamental_pitch, (1, 4)) for ratio in ratios])
for ratio, leaf in zip(combination_ratios, abjad.select(staff_2).leaves()):
    microtones.tune_to_ratio(leaf.note_head, ratio)
    mark = abjad.Markup(ratio, direction=abjad.Up)
    abjad.attach(mark, leaf)
print("handling clefs")
handler = evans.ClefHandler(
    clef="bass",
    add_extended_clefs=True,
    add_ottavas=True,
)
handler(staff_1)
handler(staff_2)
print("preparing score")
score = abjad.Score([staff_1, staff_2])
print("preparing file")
lilypond_file = abjad.LilyPondFile.new(
    score,
    includes=[
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/default.ily",
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/microtones/ekmelos-ji-accidental-markups.ily",
    ],
)
style = '"dodecaphonic"'
lilypond_file.layout_block.items.append(fr"\accidentalStyle {style}")
print("rendering file")
abjad.show(lilypond_file)
