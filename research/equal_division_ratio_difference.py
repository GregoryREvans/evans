import math

import abjad
import evans
import quicktions
from abjadext import microtones


# s = evans.Sequence.equal_divisions(440, 3 / 2, 31)
#
# temp_val = s[5]
#
# p = abjad.NumberedPitch.from_hertz(temp_val)
#
# p_cents = evans.Sequence.equal_divisions(p.hertz, (2 ** (1 / 12)), 100)
#
#
# def return_nearest_approximation(target, candidates):
#     nearest_approximation = candidates[0]
#     difference_size = abs(candidates[0] - target)
#     for candidate in candidates[1:]:
#         test_val = abs(candidate - target)
#         if test_val < difference_size:
#             nearest_approximation = candidate
#             difference_size = test_val
#     return nearest_approximation, candidates.index(nearest_approximation)
#
#
# nearest = return_nearest_approximation(temp_val, p_cents)
#
# print(f"Real Herts: {temp_val}\n")
# print(f"Semitone Hertz: {p.hertz}\n")
# print(f"Semitone Cents in Hertz: {p_cents}\n")
# print(f"Calculated Nearest Approximation: {nearest[0]}\n")
# print(f"Deviation in cents: {nearest[1]}")
def annotate_hertz(selections):
    for tie in abjad.select.logical_ties(selections):
        try:
            hertz = abjad.get.annotation(tie[0], "ratio")
            hertz = round(float(hertz), 1)
            m = abjad.Markup(rf"\markup \center-align {hertz}")
            bundle = abjad.bundle(m, r"\tweak color #red")
            abjad.attach(bundle, tie[0], direction=abjad.DOWN)
        except:
            continue


p1 = [
    evans.ETPitch(
        "a'",
        "7/2",
        9,
        _,
        transposition=None,
        with_quarter_tones=False,
    )
    for _ in range(10)
]

h1 = evans.PitchHandler(p1, forget=False)
s1 = abjad.Staff([abjad.Note() for _ in range(len(p1))])
h1(s1)
annotate_hertz(s1)

p2 = [
    evans.ETPitch(
        "a'",
        "7/2",
        9,
        _,
        transposition=None,
        with_quarter_tones=True,
    )
    for _ in range(10)
]

h2 = evans.PitchHandler(p2, forget=False)
s2 = abjad.Staff([abjad.Note() for _ in range(len(p2))])
h2(s2)

s = abjad.Score([s1, s2])


moment = "#(ly:make-moment 1 15)"
abjad.setting(s).proportional_notation_duration = moment
file = abjad.LilyPondFile(
    items=[
        '#(set-default-paper-size "a4" \'portrait)',
        r"#(set-global-staff-size 16)",
        '\\include "/Users/gregoryevans/abjad/abjad/scm/abjad.ily"',
        s,
        abjad.Block(name="layout"),
    ],
)
style = '"dodecaphonic"'
file["layout"].items.append(rf"\accidentalStyle {style}")
abjad.show(file)
