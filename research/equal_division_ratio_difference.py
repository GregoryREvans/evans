import math

import abjad
import evans
import quicktions
from abjadext import microtones


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
        "7/4",
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
        "7/4",
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


###
###
###


p1 = [
    evans.ETPitch(
        "a'",
        "5/2",
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
        "5/2",
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


###
###
###


# p1 = [
#     evans.ETPitch(
#         "a'",
#         "9/8",
#         100,
#         _,
#         transposition=None,
#         with_quarter_tones=False,
#     )
#     for _ in range(101)
# ]
#
# h1 = evans.PitchHandler(p1, forget=False)
# s1 = abjad.Staff([abjad.Note() for _ in range(len(p1))])
# h1(s1)
# annotate_hertz(s1)
#
#
# s = abjad.Score([s1])
#
#
# moment = "#(ly:make-moment 1 15)"
# abjad.setting(s).proportional_notation_duration = moment
# file = abjad.LilyPondFile(
#     items=[
#         '#(set-default-paper-size "a4" \'portrait)',
#         r"#(set-global-staff-size 16)",
#         '\\include "/Users/gregoryevans/abjad/abjad/scm/abjad.ily"',
#         s,
#         abjad.Block(name="layout"),
#     ],
# )
# style = '"dodecaphonic"'
# file["layout"].items.append(rf"\accidentalStyle {style}")
# abjad.show(file)
