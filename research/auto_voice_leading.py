import pathlib
from fractions import Fraction

import abjad
import evans

###
###
###

tempo_pair = ((1, 4), 10)
metronome_mark = abjad.MetronomeMark(tempo_pair[0], tempo_pair[1])

# trio 1
voices = {
    "voice 1": [],
    "voice 2": [],
    "voice 3": [],
}

s = evans.RatioSegment(["1/1", "6/5", "3/2"])

instructions = [
    "3/2",
    "4/5",
    "3/2",
    "4/5",
    "3/2",
    "4/5",
    "3/2",
    "4/5",
    "3/2",
    "4/5",
    "3/2",
    "4/5",
    "3/2",
    "4/5",
    "3/2",
    "4/5",
]

out = [s]

for i in instructions:
    new = out[-1].multiply(i)
    out.append(new)

out_ = []
for sub_list in out:
    out_.append(list(sub_list))

voicewise_ratios = evans.sort_voices(out_, voices)

handlers = []
fundamentals = ["c", "c'", "c'"]
voice_length = 0
for fundamental, voice in zip(fundamentals, voicewise_ratios):
    handlers.append(
        evans.PitchHandler(
            [evans.JIPitch(fundamental, ratio) for ratio in voicewise_ratios[voice]],
            forget=False,
        )
    )
    voice_length = len(voicewise_ratios[voice])

handlers.reverse()

maker = abjad.LeafMaker()
durations = [abjad.Duration((10, 4)) for _ in range(len(out_))]
leaves_1 = [abjad.Rest((3, 8))] + [maker(["c'"], durations)]
leaves_2 = [abjad.Rest((3, 4))] + [maker(["c'"], durations)] + [abjad.Rest((3, 4))]
leaves_3 = [maker(["c"], durations)]

group = abjad.StaffGroup(
    [
        abjad.Staff([abjad.Voice(leaves_1, name="violin 3")]),
        abjad.Staff([abjad.Voice(leaves_2, name="violin 4")]),
        abjad.Staff([abjad.Voice(leaves_3, name="viola 2")]),
    ]
)
abjad.attach(abjad.Clef("treble"), group[0][0][0])
abjad.attach(abjad.Clef("treble"), group[1][0][0])
abjad.attach(abjad.Clef("alto"), group[2][0][0])


# trio 2
voices = {
    "voice 1": [],
    "voice 2": [],
    "voice 3": [],
}

s = evans.RatioSegment(["1/1", "7/6", "3/2"])

instructions = [
    "2/3",
    "5/4",
    "2/3",
    "5/4",
    "2/3",
    "5/4",
    "2/3",
    "5/4",
    "2/3",
    "5/4",
    "2/3",
    "5/4",
    "2/3",
    "5/4",
    "2/3",
    "5/4",
]

out = [s]

for i in instructions:
    new = out[-1].multiply(i)
    out.append(new)

out_ = []
for sub_list in out:
    out_.append(list(sub_list))

voicewise_ratios = evans.sort_voices(out_, voices)

handlers_2 = []
fundamentals = ["c", "c'", "c'"]
voice_length = 0
for fundamental, voice in zip(fundamentals, voicewise_ratios):
    handlers_2.append(
        evans.PitchHandler(
            [evans.JIPitch(fundamental, ratio) for ratio in voicewise_ratios[voice]],
            forget=False,
        )
    )
    voice_length = len(voicewise_ratios[voice])

handlers_2.reverse()


durations = [abjad.Duration((10, 4)) for _ in range(len(out_))]
leaves_1 = [abjad.Rest((1, 8))] + [maker(["c''"], durations)]
leaves_2 = [abjad.Rest((1, 4))] + [maker(["c''"], durations)]
leaves_3 = [maker(["c'"], durations)]

group_2 = abjad.StaffGroup(
    [
        abjad.Staff([abjad.Voice(leaves_1, name="bass 1")]),
        abjad.Staff([abjad.Voice(leaves_2, name="bass 2")]),
        abjad.Staff([abjad.Voice(leaves_3, name="cello 2")]),
    ]
)
abjad.attach(abjad.Clef("bass"), group_2[0][0][0])
abjad.attach(abjad.Clef("bass"), group_2[1][0][0])
abjad.attach(abjad.Clef("bass"), group_2[2][0][0])


# quartet
voices = {
    "voice 1": [],
    "voice 2": [],
    "voice 3": [],
    "voice 4": [],
}

s = evans.RatioSegment(["1/1", "7/4", "9/8", "3/2"])  # revise

out_ = evans.tonnetz(
    s,
    "major",
    [
        "p",
        "l7",
        "r7",
        "p",
        "l11",
        "r11",
        "p",
        "l",
        "r",
        "p",
        "l",
        "r",
        "p",
        "l7",
        "r7",
        "p",
        "l",
        "r",
        "l",
        "r",
        "l",
        "r",
        "l11",
        "r11",
        "p",
        "l",
    ],
)  # revise

preamble = [
    (Fraction("7/4"), Fraction("5/4"), Fraction("3/2"), Fraction("1/1")),
    (Fraction("11/8"), Fraction("9/4"), Fraction("5/2"), Fraction("3/1")),
    (Fraction("7/8"), Fraction("3/2"), Fraction("6/5"), Fraction("6/5")),
    (Fraction("16/12"), Fraction("13/12"), Fraction("11/8"), Fraction("11/8")),
    (Fraction("9/4"), Fraction("7/2"), Fraction("6/1"), Fraction("2/1")),
]

out_ = preamble + out_


voicewise_ratios = evans.sort_voices(out_, voices)

handlers_3 = []
fundamentals = ["c''", "c''", "c'", "c"]
voice_length = 0
for fundamental, voice in zip(fundamentals, voicewise_ratios):
    handlers_3.append(
        evans.PitchHandler(
            [evans.JIPitch(fundamental, ratio) for ratio in voicewise_ratios[voice]],
            forget=False,
        )
    )
    voice_length = len(voicewise_ratios[voice])

cyc_durs = evans.CyclicList(
    [abjad.Duration((5, 4)), abjad.Duration((3, 4)), abjad.Duration((7, 4))],
    forget=False,
)
durations = cyc_durs(r=len(out_))

leaves_1 = [abjad.Rest((2, 1))] + [
    maker(["c'", "c'", None, "c'", None, "c'", "c'", "c'", None], durations)
]
leaves_2 = [abjad.Rest((2, 1))] + [
    maker(["c'", "c'", None, "c'", None, "c'", "c'", "c'", None], durations)
]
leaves_3 = [abjad.Rest((2, 1))] + [
    maker(["c'", "c'", None, "c'", None, "c'", "c'", "c'", None], durations)
]
leaves_4 = [abjad.Rest((2, 1))] + [
    maker(["c'", "c'", None, "c'", None, "c'", "c'", "c'", None], durations)
]

quartet_group = abjad.StaffGroup(
    [
        abjad.Staff([abjad.Voice(leaves_1, name="violin 1")]),
        abjad.Staff([abjad.Voice(leaves_2, name="violin 2")]),
        abjad.Staff([abjad.Voice(leaves_3, name="viola 1")]),
        abjad.Staff([abjad.Voice(leaves_4, name="cello 1")]),
    ]
)

abjad.attach(abjad.Clef("treble"), quartet_group[0][0][0])
abjad.attach(abjad.Clef("treble"), quartet_group[1][0][0])
abjad.attach(abjad.Clef("alto"), quartet_group[2][0][0])
abjad.attach(abjad.Clef("bass"), quartet_group[3][0][0])


score = abjad.Score([quartet_group, group, group_2])
abjad.attach(metronome_mark, group[0][0][0])
for voice in abjad.Selection(score).components(abjad.Voice):
    voice_dur = abjad.get.duration(voice)
    comparison_dur = abjad.get.duration(group[1][0])
    if voice_dur < comparison_dur:
        new_dur = comparison_dur - voice_dur
        rest_leaves = maker([None], [new_dur])
        for leaf in rest_leaves:
            voice.append(leaf)
for voice in abjad.Selection(score).components(abjad.Voice):
    for i, shard in enumerate(
        abjad.mutate.split(voice[:], [abjad.Meter((4, 4))], cyclic=True)
    ):
        abjad.Meter.rewrite_meter(shard, abjad.Meter((4, 4)))
    abjad.label.with_start_offsets(voice, clock_time=True)

for handler, staff in zip(handlers, group):
    handler(staff)

for handler, staff in zip(handlers_2, group_2):
    handler(staff)

for handler, staff in zip(handlers_3, quartet_group):
    handler(staff)


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

evans.make_sc_file(
    score=score,
    tempo=tempo_pair,
    current_directory=pathlib.Path(__file__).parent,
)

abjad.mutate.transpose(group_2, abjad.NamedInterval("+P8"))

abjad.show(file)
