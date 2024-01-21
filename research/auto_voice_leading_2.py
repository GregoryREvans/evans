import pathlib
from fractions import Fraction

import abjad
import evans
from abjadext import rmakers

###
###
###

tempo_pair = ((1, 4), 10)
metronome_mark = abjad.MetronomeMark(tempo_pair[0], tempo_pair[1])

maker = abjad.makers.make_leaves

# quartet
voices = {
    "voice 1": [],
    "voice 2": [],
    "voice 3": [],
    "voice 4": [],
}

s = evans.RatioSegment(["1/1", "7/8", "9/8", "11/8", "13/8", "3/2"])

out_ = evans.tonnetz(
    s,
    "major", # only 7, 3, 11, and 13
    [
        "p",
        "l7",
        "r7",
        "p",
        "l11",
        "r11",
        "p",
        "l13",
        "r13",
        "p",
        "l7",
        "r13",
        "p",
        "l7",
        "r7",
        "p",
        "l13",
        "r7",
        "l7",
        "r11",
        "l11",
        "r7",
        "l11",
        "r11",
        "p",
        "l7",

        # "p",
        # "r11",
        # "l11",
        # "r7",
        # "l11",
        # "r11",
        # "l7",
    ],
)  # revise

out_ = [evans.RatioClassSegment(_[1:-1]).ratio_classes for _ in out_]
out_[0] = out_[0][::-1]
voicewise_ratios = evans.sort_voices(out_, voices)

handlers_3 = []
fundamentals = ["c'", "c'", "c", "c,"]
voice_length = 0
for fundamental, voice in zip(fundamentals, voicewise_ratios):
    # handlers_3.append(
    #     evans.PitchHandler(
    #         [evans.JIPitch(fundamental, ratio) for ratio in voicewise_ratios[voice]],
    #         forget=False,
    #     )
    # )
    handlers_3.append(
        evans.PitchHandler(
            [fundamental for ratio in voicewise_ratios[voice]],
            forget=False,
        )
    )
    handlers_3.append(
        evans.PitchHandler(
            [ratio for ratio in voicewise_ratios[voice]],
            forget=False,
            as_ratios=True
        )
    )
    voice_length = len(voicewise_ratios[voice])

cyc_durs = evans.CyclicList(
    [
        abjad.Duration((4, 8)),
        abjad.Duration((6, 8)),
        # abjad.Duration((2, 8)),
        abjad.Duration((3, 8)),
        abjad.Duration((5, 8)),
        abjad.Duration((7, 8)),
    ],
    forget=False,
)
durations = cyc_durs(r=len(out_))
# leaves_1 = maker(["c'"], durations)
leaves_1 = rmakers.multiplied_duration(durations, duration=(1, 4))

durations = cyc_durs(r=len(out_))
# leaves_2 = maker(["c'"], durations)
leaves_2 = rmakers.multiplied_duration(durations, duration=(1, 4))

durations = cyc_durs(r=len(out_))
# leaves_3 = maker(["c'"], durations)
leaves_3 = rmakers.multiplied_duration(durations, duration=(1, 4))

durations = cyc_durs(r=len(out_))
# leaves_4 = maker(["c'"], durations)
leaves_4 = rmakers.multiplied_duration(durations, duration=(1, 4))

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


score = abjad.Score([quartet_group])
abjad.attach(metronome_mark, quartet_group[0][0][0])
for voice in abjad.select.components(score, abjad.Voice):
    voice_dur = abjad.get.duration(voice)
    comparison_dur = abjad.get.duration(quartet_group[1][0])
    if voice_dur < comparison_dur:
        new_dur = comparison_dur - voice_dur
        rest_leaves = maker([None], [new_dur])
        for leaf in rest_leaves:
            voice.append(leaf)
# for voice in abjad.select.components(score, abjad.Voice): # for traditional notation
#     for i, shard in enumerate(
#         abjad.mutate.split(voice[:], [abjad.Meter((4, 4))], cyclic=True)
#     ):
#         abjad.Meter.rewrite_meter(shard, abjad.Meter((4, 4)))
#     abjad.label.with_start_offsets(voice, clock_time=True)

for voice in abjad.select.components(score, abjad.Voice): # for proportional notation
    abjad.label.with_start_offsets(voice, clock_time=True)
    for leaf in abjad.select.leaves(voice):
        abjad.attach(abjad.BendAfter(0), leaf)


cyc_handlers = evans.CyclicList(handlers_3, forget=False)
for staff in quartet_group:
    handler = cyc_handlers(r=1)[0]
    handler(staff)
    handler = cyc_handlers(r=1)[0]
    handler(staff)


moment = "#(ly:make-moment 1 13)"
abjad.setting(score).proportional_notation_duration = moment

block = abjad.Block(name="score")
block.items.append(score)

style = '"dodecaphonic"'
layout = abjad.Block(name="layout")
layout.items.append(rf"\accidentalStyle {style}")

file = abjad.LilyPondFile(
    items=[
        r'\include "/Users/gregoryevans/abjad/abjad/scm/ekmelos-ji-accidental-markups.ily"',
        # r'\include "/Users/gregoryevans/scores/polillas/polillas/build/score_stylesheet.ily"',
        layout,
        block,
    ]
)

evans.make_sc_file(
    score=score,
    tempo=metronome_mark,
    current_directory=pathlib.Path(__file__).parent,
)

abjad.show(file)
