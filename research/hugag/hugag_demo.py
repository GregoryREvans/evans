import abjad
import evans
import tsmakers
from abjadext import rmakers

v1_tsl = abjad.TimespanList(
    [
        abjad.AnnotatedTimespan(0, 2, annotation="Voice 1"),  # silent
        abjad.AnnotatedTimespan(2, 7, annotation="Voice 1"),
        abjad.AnnotatedTimespan(7, 8, annotation="Voice 1"),  # silent
    ]
)
v2_tsl = abjad.TimespanList(
    [
        abjad.AnnotatedTimespan(0, 3, annotation="Voice 2"),
        abjad.AnnotatedTimespan(3, 5, annotation="Voice 2"),  # silent
        abjad.AnnotatedTimespan(5, 6, annotation="Voice 2"),
        abjad.AnnotatedTimespan(6, 8, annotation="Voice 2"),  # silent
    ]
)
v3_tsl = abjad.TimespanList(
    [
        abjad.AnnotatedTimespan(0, 2, annotation="Voice 3"),
        abjad.AnnotatedTimespan(2, 4, annotation="Voice 3"),  # silent
        abjad.AnnotatedTimespan(4, (9, 2), annotation="Voice 3"),
        abjad.AnnotatedTimespan((9, 2), 8, annotation="Voice 3"),  # silent
    ]
)
v4_tsl = abjad.TimespanList([abjad.AnnotatedTimespan(0, 8, annotation="Voice 4")])
v5_tsl = abjad.TimespanList(
    [
        abjad.AnnotatedTimespan(0, (1, 2), annotation="Voice 5"),  # silent
        abjad.AnnotatedTimespan((1, 2), (3, 2), annotation="Voice 5"),
        abjad.AnnotatedTimespan((3, 2), 8, annotation="Voice 5"),  # silent
    ]
)
#
# provisional_tsl = abjad.TimespanList()
# for timespanlist in (v2_tsl, v3_tsl):
#     for timespan in timespanlist:
#         provisional_tsl.append(timespan)
#
# provisional_tsl = provisional_tsl.compute_logical_xor()
#
# v2_tsl = abjad.TimespanList([_ for _ in provisional_tsl if _.annotation == "Voice 2"])

timespans = [v1_tsl, v2_tsl, v3_tsl, v4_tsl, v5_tsl]
tsl = abjad.TimespanList()
for timespanlist in timespans:
    for timespan in timespanlist:
        tsl.append(timespan)

pairs = [
    (7, 6),
    (3, 2),
    (1, 3),
    (2, 4),
    (2, 3),
    (3, 5),
    (5, 6),
    (3, 4),
    (5, 4),
    (2, 5),
]

sigs = [abjad.TimeSignature(_) for _ in pairs]

rhythm_handler = evans.RhythmHandler(
    evans.RTMMaker(
        [
            "(1 (1 1 1))",
            "(1 (1 1 1 1))",
            # "(1 (1 1 (1 (1 1)) 1))",
            # "(1 (1 1 (1 (1 1 1)) 1 1))",
        ]
    ),
    forget=False,
)

silence_handler = evans.RhythmHandler(
    rmakers.Stack(
        rmakers.NoteRhythmMaker(),
        rmakers.ForceRestCommand(selector=abjad.select().leaves(pitched=True)),
    ),
    forget=True,
    name="silence_maker",
)

material_list = evans.CyclicList(
    [
        silence_handler,
        rhythm_handler,
        silence_handler,
        rhythm_handler,
        silence_handler,
        rhythm_handler,
        silence_handler,
        rhythm_handler,
        silence_handler,
        rhythm_handler,
        silence_handler,
        rhythm_handler,
        silence_handler,
        rhythm_handler,
        silence_handler,
    ],
    forget=False,
)

tsl = sorted(tsl)

tsl = sorted(tsl, key=lambda x: x.annotation)

tsl = abjad.TimespanList(
    [
        tsmakers.PerformedTimespan(
            timespan.start_offset,
            timespan.stop_offset,
            voice_name=timespan.annotation,
            handler=material_list(r=1)[0],
        )
        for timespan in tsl
    ]
)

bounds = abjad.mathx.cumulative_sums([_.duration for _ in sigs])

tsl = evans.timespan.make_split_list(tsl, bounds)

tsl = sorted(tsl)

tsl = sorted(tsl, key=lambda x: x.voice_name)

rhythm_commands = []
for _ in tsl:
    command = evans.RhythmCommand(
        voice_name=_.voice_name,
        timespan=_,
        handler=_.handler,
    )
    rhythm_commands.append(command)

rhythm_commands = sorted(rhythm_commands, key=lambda x: x.timespan)

rhythm_commands = sorted(rhythm_commands, key=lambda x: x.voice_name)

score_template = abjad.Score(
    [
        abjad.Staff(
            [abjad.Skip((1, 1), multiplier=abjad.Multiplier(_)) for _ in pairs],
            lilypond_type="TimeSignatureContext",
            name="Global Context",
        ),
        abjad.StaffGroup(
            [
                abjad.Staff(
                    [
                        abjad.Voice(name="Voice 1"),
                    ],
                    lilypond_type="StringContactStaff",
                    name="SCStaff",
                ),
                abjad.StaffGroup(
                    [
                        abjad.Staff(
                            [
                                abjad.Voice(name="Voice 2"),
                            ],
                            lilypond_type="BowContactStaff",
                            name="BCStaff",
                        ),
                        abjad.Staff(
                            [
                                abjad.Voice(name="Voice 2 copy"),
                            ],
                            lilypond_type="BeamStaff",
                            name="BCStaff copy",
                        ),
                    ],
                    lilypond_type="SubGroup",
                    name="SubGroup 1",
                ),
                abjad.StaffGroup(
                    [
                        abjad.Staff(
                            [
                                abjad.Voice(name="Voice 3"),
                            ],
                            lilypond_type="BowAngleStaff",
                            name="BAStaff",
                        ),
                        abjad.Staff(
                            [
                                abjad.Voice(name="Voice 3 copy"),
                            ],
                            lilypond_type="BeamStaff",
                            name="BAStaff copy",
                        ),
                    ],
                    lilypond_type="SubGroup",
                    name="SubGroup 2",
                ),
                abjad.Staff(
                    [
                        abjad.Voice(name="Voice 4"),
                    ],
                    lilypond_type="Staff",
                    name="Staff 4",
                ),
                abjad.Staff(
                    [
                        abjad.Voice(name="Voice 5"),
                    ],
                    lilypond_type="DynamicStaff",
                    name="DStaff",
                ),
            ],
            lilypond_type="StaffGroup",
            name="Staff Group",
        ),
    ]
)

for sig, skip in zip(sigs, abjad.select(score_template["Global Context"]).leaves()):
    abjad.attach(sig, skip)


def make_container(handler, durations):
    selections = handler(durations)
    container = abjad.Container([])
    container.extend(selections)
    return container


for command in rhythm_commands:
    timespan = command.timespan
    d = timespan.duration
    voice_name = command.voice_name
    handler = command.handler
    container = make_container(handler, [d])
    voice = score_template[voice_name]
    voice.append(container[:])

for voice in abjad.select(score_template["Staff Group"]).components(abjad.Voice):
    if voice.name == "Voice 2":
        score_template["Voice 2 copy"].extend(abjad.mutate.copy(voice))
    if voice.name == "Voice 3":
        score_template["Voice 3 copy"].extend(abjad.mutate.copy(voice))

for staff in abjad.select(score_template["Staff Group"]).components(abjad.Staff):
    bracket_maker = evans.NoteheadBracketMaker()
    bracket_maker(staff[:])
    shards = abjad.mutate.split(staff[:], sigs)
    for shard, sig in zip(shards, sigs):
        abjad.Meter.rewrite_meter(shard, meter=abjad.Meter(sig), rewrite_tuplets=False)

bcps = evans.CyclicList(
    [
        abjad.BowContactPoint((0, 7)),
        abjad.BowContactPoint((1, 7)),
        abjad.BowContactPoint((3, 7)),
        abjad.BowContactPoint((6, 7)),
        abjad.BowContactPoint((4, 7)),
        abjad.BowContactPoint((2, 7)),
        abjad.BowContactPoint((7, 7)),
    ],
    forget=False,
)

baps = evans.CyclicList(
    [
        evans.BowAnglePoint(-15),
        evans.BowAnglePoint(45),
        evans.BowAnglePoint(0),
        evans.BowAnglePoint(5),
        evans.BowAnglePoint(20),
    ],
    forget=False,
)

for leaf in abjad.select(score_template["BCStaff"]).leaves():
    point = bcps(r=1)[0]
    abjad.attach(point, leaf)
    tech = abjad.BowMotionTechnique("ordinario")
    abjad.attach(tech, leaf)

for run in abjad.select(score_template["BCStaff"]).runs():
    abjad.bow_contact_spanner(run)

for leaf in abjad.select(score_template["BAStaff"]).leaves():
    point = baps(r=1)[0]
    abjad.attach(point, leaf)
    tech = abjad.BowMotionTechnique("ordinario")
    abjad.attach(tech, leaf)

for run in abjad.select(score_template["BAStaff"]).runs():
    evans.bow_angle_spanner(run)

for staff in abjad.select(score_template["Staff Group"]).components(abjad.Staff):
    if staff.lilypond_type != "BeamStaff":
        shards = abjad.mutate.split(staff[:], sigs)
        for shard, sig in zip(shards, sigs):
            evans.beam_meter(components=shard, meter=abjad.Meter(sig), offset_depth=1)
    else:  # was commented out
        shards = abjad.mutate.split(staff[:], sigs)
        for shard, sig in zip(shards, sigs):
            evans.beam_meter(components=shard, meter=abjad.Meter(sig), offset_depth=1)
        handler = evans.PitchHandler(["a'''''"], forget=False)
        handler(shard)
        for run in abjad.select(shard).runs():
            abjad.attach(abjad.Ottava(n=(-15)), abjad.select(run).leaf(0, pitched=True))
            abjad.attach(
                abjad.Ottava(n=0, format_slot="after"),
                abjad.select(run).leaf(-1, pitched=True),
            )

cyc_names = evans.CyclicList(["BCP", "bcp.", "Bow Angle", "ba."], forget=False)
for staffgroup in abjad.select(score_template).components(abjad.StaffGroup):
    if staffgroup.lilypond_type == "SubGroup":
        abjad.setting(staffgroup).instrumentName = abjad.Markup(cyc_names(r=1)[0])
        abjad.setting(staffgroup).shortInstrumentName = abjad.Markup(cyc_names(r=1)[0])

start_mark = abjad.StartMarkup(abjad.Markup("Left Hand"))
margin_mark = abjad.MarginMarkup(markup=abjad.Markup("lh."))
selector = abjad.select(score_template["Staff 4"]).leaf(0)
abjad.attach(start_mark, selector)
abjad.attach(margin_mark, selector)

file = abjad.LilyPondFile.new(
    score_template,
    includes=[
        "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily",
        "/Users/evansdsg2/evans/research/hugag/stylesheet.ily",
    ],
)

abjad.show(file)
