import abjad
import evans
from abjadext import microtones

# from abjadext.microtones import RatioSegment

segment_one = microtones.PitchSegment(
    [
        "39/4",
        "31/4",
        "17/2",
        2,
        0,
        "21/5",
        "37/6",
        "27/5",
        2,
        "29/3",
        "21/2",
        "47/4",
    ]
)

segment_two = evans.combination_multiples(
    [1, 1, 7, 9, 13, 25], combination_size=2
).sorted()

staff = abjad.Staff("c'4 c'4 c'4 c'4")
handler_one = evans.PitchHandler(
    pitch_list=segment_one,
    forget=False,
    apply_all=True,
    chord_boolean_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    chord_groups=[2],
)

handler_one(staff)

staff_two = abjad.Staff("c'4 c'4 c'4 c'4")
handler_two = evans.PitchHandler(
    pitch_list=segment_two,
    forget=False,
    as_ratios=True,
    chord_boolean_vector=[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    chord_groups=[2],
)

handler_two(staff_two)

trills = evans.TrillHandler(boolean_vector=[1])

trills(staff)
trills(staff_two)

abjad.f(staff)
print("")
print("")
abjad.f(staff_two)

score = abjad.Score([staff, staff_two])

lilypond_file = abjad.LilyPondFile.new(
    score,
    includes=[
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/default.ily",
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/ekmelos-ji-accidental-markups.ily",
    ],
)
style = '"dodecaphonic"'
lilypond_file.layout_block.items.append(fr"\accidentalStyle {style}")
abjad.show(lilypond_file)
