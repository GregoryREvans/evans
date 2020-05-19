import itertools

import abjad
import timespan_functions
from TimespanMaker_for_greg import TimespanMaker
from abjadext import rmakers
from evans.AttachmentHandlers.ArticulationHandler import ArticulationHandler
from evans.AttachmentHandlers.ClefHandler import ClefHandler
from evans.AttachmentHandlers.DynamicHandler import DynamicHandler
from evans.AttachmentHandlers.MusicMaker import MusicMaker
from evans.AttachmentHandlers.PitchHandler import PitchHandler

rmaker_one = rmakers.TaleaRhythmMaker(
    talea=rmakers.Talea(counts=[7], denominator=8),
    beam_specifier=rmakers.BeamSpecifier(
        beam_divisions_together=True, beam_rests=False
    ),
    extra_counts_per_division=[0, 1, -1, 1, 0, -1, 0],
    # burnish_specifier=rmakers.BurnishSpecifier(
    #     left_classes=[abjad.Rest],
    #     left_counts=[1],
    #     right_classes=[abjad.Rest],
    #     right_counts=[2],
    #     outer_divisions_only=True,
    #     ),
    # logical_tie_masks=[
    #     rmakers.silence([2], 7),
    #     ],
    tie_specifier=rmakers.TieSpecifier(tie_across_divisions=True),
    tuplet_specifier=rmakers.TupletSpecifier(
        trivialize=True,
        extract_trivial=True,
        rewrite_rest_filled=True,
        rewrite_dots=True,
        rewrite_sustained=True,
        denominator="divisions",
    ),
)
rmaker_two = rmakers.TaleaRhythmMaker(
    talea=rmakers.Talea(counts=[1, 1, 3, -1, 2, 5, 4, 1, 3, 1, 2, 2], denominator=16),
    beam_specifier=rmakers.BeamSpecifier(
        beam_divisions_together=True, beam_rests=False
    ),
    extra_counts_per_division=[0, 1, -1, 1, 0, -1, 0],
    # burnish_specifier=rmakers.BurnishSpecifier(
    #     left_classes=[abjad.Rest],
    #     left_counts=[1],
    #     right_classes=[abjad.Rest],
    #     right_counts=[2],
    #     outer_divisions_only=True,
    #     ),
    # logical_tie_masks=[
    #     rmakers.silence([2], 7),
    #     ],
    tie_specifier=rmakers.TieSpecifier(tie_across_divisions=True),
    tuplet_specifier=rmakers.TupletSpecifier(
        trivialize=True,
        extract_trivial=True,
        rewrite_rest_filled=True,
        rewrite_dots=True,
        rewrite_sustained=True,
        denominator="divisions",
    ),
)

attachment_handler_one = DynamicHandler(
    starting_dynamic="p", ending_dynamic="mp", hairpin="--"
)
articulation_handler_one = ArticulationHandler(
    articulation_list=["accent"], continuous=True
)

attachment_handler_two = DynamicHandler(
    starting_dynamic="fff", ending_dynamic="mf", hairpin=">"
)
articulation_handler_two = ArticulationHandler(
    articulation_list=["tenuto"], continuous=True
)

rmodel_one = MusicMaker(
    rmaker=rmaker_one,
    pitch_handler=PitchHandler(pitch_list=[12, 13, 14, 15, 16], continuous=True),
    continuous=True,
    dynamic_handler=attachment_handler_one,
    articulation_handler=articulation_handler_one,
    clef_handler=ClefHandler(clef="treble", add_ottavas=True),
)
rmodel_two = MusicMaker(
    rmaker=rmaker_one,
    pitch_handler=PitchHandler(pitch_list=[1, 2, 3, 4, 5], continuous=True),
    continuous=True,
    dynamic_handler=attachment_handler_one,
    articulation_handler=articulation_handler_one,
    clef_handler=ClefHandler(clef="treble", add_ottavas=True),
)
rmodel_three = MusicMaker(
    rmaker=rmaker_one,
    pitch_handler=PitchHandler(pitch_list=[10, 9, 8, 7, 6], continuous=True),
    continuous=True,
    dynamic_handler=attachment_handler_two,
    articulation_handler=articulation_handler_two,
    clef_handler=ClefHandler(clef="treble", add_ottavas=True),
)

silence_maker = rmakers.NoteRhythmMaker(
    division_masks=[rmakers.SilenceMask(pattern=abjad.index([0], 1))]
)

timespan_maker = TimespanMaker(denominator=8, total_duration=abjad.Duration(15, 2))
counts = [3, 5, 3, 4, 7]

timespan_list = timespan_maker(counts, max_duration=7)
initial_list = [timespan_list]

rmakers_cycle_1 = timespan_functions.cyc([rmodel_one])
rhythm_models = [rmakers_cycle_1]
# Timespan list
master_list = []
for i, timespan_list, cycle in zip(
    enumerate(initial_list), initial_list, rhythm_models
):
    for timespan in timespan_list:
        if isinstance(timespan, abjad.AnnotatedTimespan):
            timespan.annotation = timespan_functions.TimespanSpecifier(
                voice_name=f"Voice {i}", rhythm_maker=next(cycle)
            )
        else:
            timespan.annotation = timespan_functions.TimespanSpecifier(
                voice_name=f"Voice {i}", rhythm_maker=silence_maker
            )
    timespan_list.sort()
    master_list.append(timespan_list)

master_length = len(master_list)
voices = [f"Voice {i + 1}" for i in range(master_length)]
all_timespans = {
    voice: timespan_list for voice, timespan_list in zip(voices, master_list)
}
silence_specifier = timespan_functions.TimespanSpecifier(rhythm_maker=silence_maker)
timespan_functions.add_silences_to_timespan_dict(all_timespans, silence_specifier)

time_signatures = [
    abjad.TimeSignature(timespan.duration) for timespan in all_timespans["Voice 1"]
]
offsets = abjad.mathtools.cumulative_sums(
    [abjad.Offset(t_s.duration) for t_s in time_signatures]
)

for voice, timespan_list in all_timespans.items():
    all_timespans[voice] = timespan_functions.make_split_list(timespan_list, offsets)

# Score
voice_staff_names = [[f"Voice {i + 1}", f"Staff {i + 1}"] for i in range(master_length)]
score = abjad.Score(
    [
        abjad.Staff(lilypond_type="TimeSignatureContext", name="Global Context"),
        abjad.StaffGroup(
            [
                abjad.Staff(
                    [abjad.Voice(name=voice_name)],
                    name=staff_name,
                    lilypond_type="Staff",
                )
                for voice_name, staff_name in voice_staff_names
            ],
            name="Staff Group",
        ),
    ]
)

# Timespan -> Rhythm
# for voice_name, timespan_list in all_timespans.items():
#     for timespan in timespan_list:
#         container = abjad.Container([])
#         durations = [timespan.duration]
#         selections = timespan.annotation.rhythm_maker(durations)
#         container.extend(selections)
#         specifier = rmakers.BeamSpecifier(beam_each_division=True, beam_rests=True)
#         specifier(abjad.select(container))
#         voice = score[voice_name]
#         voice.append(container)


def key_function(timespan):
    return timespan.annotation.rhythm_maker or silence_maker


def make_container(music_maker, durations):
    selections = music_maker(durations)
    container = abjad.Container([])
    container.extend(selections)
    return container


for voice_name, timespan_list in all_timespans.items():
    for music_maker, grouper in itertools.groupby(timespan_list, key=key_function):
        durations = [timespan.duration for timespan in grouper]
        container = make_container(music_maker, durations)
        voice = score[voice_name]
        voice.append(container)

# stop hairpins
for staff in abjad.iterate(score["Staff Group"]).components(abjad.Staff):
    for rest in abjad.iterate(staff).components(abjad.Rest):
        previous_leaf = abjad.inspect(rest).leaf(-1)
        if isinstance(previous_leaf, abjad.Note):
            abjad.attach(abjad.StopHairpin(), rest)
        elif isinstance(previous_leaf, abjad.Chord):
            abjad.attach(abjad.StopHairpin(), rest)
        elif isinstance(previous_leaf, abjad.Rest):
            pass

# Add Time Signatures
for time_signature in time_signatures:
    skip = abjad.Skip(1, multiplier=(time_signature))
    abjad.attach(time_signature, skip)
    score["Global Context"].append(skip)

for voice in abjad.select(score).components(abjad.Voice):
    specifier = rmakers.BeamSpecifier(beam_each_division=False)
    specifier(voice[:])
    abjad.beam(voice[:], beam_lone_notes=False, beam_rests=False)

# Label staves
for i, staff in enumerate(abjad.iterate(score["Staff Group"]).components(abjad.Staff)):
    markup_label = "Voice " + f"{i + 1}"
    name_abbrev = [
        abjad.StartMarkup(markup=abjad.Markup(markup_label)),
        abjad.MarginMarkup(markup=abjad.Markup(markup_label)),
    ]
    for label in name_abbrev:
        abjad.attach(label, abjad.select(staff).leaves()[0])


# Lilyfile
lilyfile = abjad.LilyPondFile.new(
    score,
    includes=[
        # timespan_functions.rhythm_stylesheet,
        timespan_functions.abjad_stylesheet,
        "/Users/evansdsg2/evans/abjad_functions/talea_timespan/first_stylesheet.ily",
    ],
)

abjad.show(lilyfile)
# abjad.play(lilyfile)
