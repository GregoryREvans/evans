import abjad
import evans
from abjadext import microtones

score = abjad.Score()

source = microtones.RatioSegment(
    [
        1,
        "5/4",
        "3/2",
    ]
)

triads = evans.tonnetz(
    source,
    "major",
    [
        "p",
        "h",
        "s",
        "n",
        "p",
        "l",
        "r",
        "r",
        "l",
        "l",
    ],
)

for chord in triads:
    staff = abjad.Staff([abjad.Note("c'8") for pitch in chord])
    for pitch, note in zip(chord, staff):
        m = microtones.return_cent_deviation_markup(
            ratio=pitch, fundamental=note.written_pitch
        )
        microtones.tune_to_ratio(note.note_head, pitch)
        abjad.attach(m, note)
    abjad.attach(abjad.Clef("treble"), staff[0])
    abjad.attach(abjad.TimeSignature((6, 4)), staff[0])
    score.append(staff)
#
# lilypond_file = abjad.LilyPondFile.new(
#     score,
#     includes=[
#         "/Users/evansdsg2/abjad/docs/source/_stylesheets/default.ily",
#         "/Users/evansdsg2/abjad/docs/source/_stylesheets/ekmelos-ji-accidental-markups.ily",
#     ],
# )
# style = '"dodecaphonic"'
# lilypond_file.layout_block.items.append(fr"\accidentalStyle {style}")
# abjad.show(lilypond_file)
#
# final_triads_hertz = []
# for s in triads:
#     hertz_list = [abjad.NamedPitch("e'").hertz * _ for _ in s]
#     final_triads_hertz.append(hertz_list)
#
# print(final_triads_hertz)

final = []
for i, chord in enumerate(triads[:-1]):
    temp = []
    for ratio in chord:
        temp.append(ratio)
    for ratio in triads[i + 1]:
        if ratio not in temp:
            temp.append(ratio)
    final.append(temp)
print(final)

# final = [
#     [Fraction(1, 1), Fraction(5, 4), Fraction(3, 2), Fraction(6, 5)],
#     [Fraction(1, 1), Fraction(6, 5), Fraction(3, 2), Fraction(4, 5)],
#     [Fraction(4, 5), Fraction(1, 1), Fraction(6, 5), Fraction(24, 25)],
#     [Fraction(4, 5), Fraction(24, 25), Fraction(6, 5), Fraction(16, 25)],
#     [Fraction(16, 25), Fraction(4, 5), Fraction(24, 25), Fraction(6, 5)],
#     [Fraction(4, 5), Fraction(24, 25), Fraction(6, 5), Fraction(1, 1)],
#     [Fraction(4, 5), Fraction(1, 1), Fraction(6, 5), Fraction(2, 3)],
#     [Fraction(2, 3), Fraction(4, 5), Fraction(1, 1), Fraction(6, 5)],
#     [Fraction(4, 5), Fraction(1, 1), Fraction(6, 5), Fraction(3, 2)],
#     [Fraction(1, 1), Fraction(6, 5), Fraction(3, 2), Fraction(5, 4)],
#     [Fraction(1, 1), Fraction(5, 4), Fraction(3, 2), Fraction(6, 5)],
#     [Fraction(1, 1), Fraction(6, 5), Fraction(3, 2), Fraction(4, 5)],
#     [Fraction(4, 5), Fraction(1, 1), Fraction(6, 5), Fraction(2, 3)],
#     [Fraction(2, 3), Fraction(4, 5), Fraction(1, 1), Fraction(6, 5)],
#     [Fraction(4, 5), Fraction(1, 1), Fraction(6, 5), Fraction(3, 2)],
#     [Fraction(1, 1), Fraction(6, 5), Fraction(3, 2), Fraction(4, 5)],
# ]

# final = [
#     [Fraction(1, 1), Fraction(4, 5), Fraction(9, 8), Fraction(3, 2), Fraction(4, 3), Fraction(15, 8)], [Fraction(1, 1), Fraction(4, 3), Fraction(15, 8), Fraction(3, 2), Fraction(5, 4), Fraction(45, 32)], [Fraction(5, 4), Fraction(1, 1), Fraction(45, 32), Fraction(15, 8), Fraction(5, 3), Fraction(75, 64)], [Fraction(5, 4), Fraction(5, 3), Fraction(75, 64), Fraction(15, 8), Fraction(25, 16), Fraction(225, 128)], [Fraction(25, 16), Fraction(5, 4), Fraction(225, 128), Fraction(75, 64), Fraction(5, 6), Fraction(15, 16)], [Fraction(5, 4), Fraction(5, 6), Fraction(75, 64), Fraction(15, 16), Fraction(1, 1), Fraction(45, 32), Fraction(15, 8)], [Fraction(5, 4), Fraction(1, 1), Fraction(45, 32), Fraction(15, 8), Fraction(3, 2), Fraction(9, 8)], [Fraction(3, 2), Fraction(1, 1), Fraction(45, 32), Fraction(9, 8), Fraction(5, 4), Fraction(15, 16)], [Fraction(5, 4), Fraction(1, 1), Fraction(45, 32), Fraction(15, 16), Fraction(4, 3), Fraction(3, 2)], [Fraction(1, 1), Fraction(4, 3), Fraction(15, 16), Fraction(3, 2), Fraction(8, 5), Fraction(9, 8)], [Fraction(1, 1), Fraction(8, 5), Fraction(9, 8), Fraction(3, 2), Fraction(4, 3), Fraction(15, 16)], [Fraction(1, 1), Fraction(4, 3), Fraction(15, 16), Fraction(3, 2), Fraction(5, 4), Fraction(45, 32), Fraction(15, 8)], [Fraction(5, 4), Fraction(1, 1), Fraction(45, 32), Fraction(15, 8), Fraction(3, 2), Fraction(9, 8)], [Fraction(3, 2), Fraction(1, 1), Fraction(45, 32), Fraction(9, 8), Fraction(5, 4), Fraction(15, 16)], [Fraction(5, 4), Fraction(1, 1), Fraction(45, 32), Fraction(15, 16), Fraction(4, 3), Fraction(3, 2)], [Fraction(1, 1), Fraction(4, 3), Fraction(15, 16), Fraction(3, 2), Fraction(5, 4), Fraction(45, 32), Fraction(15, 8)]
# ]

handler = evans.PitchHandler(final, as_ratios=True, forget=False)

s = abjad.Staff([abjad.Note() for _ in final])

handler(s)

lilypond_file = abjad.LilyPondFile.new(
    s,
    includes=[
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/default.ily",
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/ekmelos-ji-accidental-markups.ily",
    ],
)
style = '"dodecaphonic"'
lilypond_file.layout_block.items.append(fr"\accidentalStyle {style}")
abjad.show(lilypond_file)
