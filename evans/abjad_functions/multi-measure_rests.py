import itertools
import abjad
import abjadext.rmakers


# Define the time signatures we would like to apply against the timespan structure.


time_signatures = [
    abjad.TimeSignature(pair)
    for pair in [
        (5, 4),
        (4, 4),
        (3, 4),
        (5, 4),
        (4, 4),
        (3, 4),
        (3, 4),
        (4, 4),
        (5, 4),
        (3, 4),
        (4, 4),
        (5, 4),
    ]
]

bounds = abjad.mathtools.cumulative_sums([_.duration for _ in time_signatures])


# Define rhythm-makers: two for actual music, one for silence.


rmaker_one = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(counts=[1, 2, 3, 4], denominator=16),
    beam_specifier=abjadext.rmakers.BeamSpecifier(
        beam_divisions_together=True, beam_rests=False
    ),
)

rmaker_two = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(counts=[4, 3, -1, 2], denominator=8),
    beam_specifier=abjadext.rmakers.BeamSpecifier(
        beam_divisions_together=True, beam_rests=False
    ),
)

silence_maker = abjadext.rmakers.NoteRhythmMaker(
    division_masks=[abjadext.rmakers.SilenceMask(pattern=abjad.index([0], 1))]
)


# Define a small class so that we can annotate timespans with additional
# information:


class MusicSpecifier:
    def __init__(self, rhythm_maker, voice_name):
        self.rhythm_maker = rhythm_maker
        self.voice_name = voice_name


# Define an initial timespan structure, annotated with music specifiers. This
# structure has not been split along meter boundaries. This structure does not
# contain timespans explicitly representing silence. Here I make four, one
# for each voice, using Python's list comprehension syntax to save some
# space.


voice_1_timespan_list = abjad.TimespanList(
    [
        abjad.AnnotatedTimespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            annotation=MusicSpecifier(rhythm_maker=rhythm_maker, voice_name="Voice 1"),
        )
        for start_offset, stop_offset, rhythm_maker in [
            [(0, 4), (3, 4), rmaker_one],
            [(5, 4), (8, 4), rmaker_one],
            [(12, 4), (15, 4), rmaker_two],
            [(17, 4), (20, 4), rmaker_one],
            [(28, 4), (31, 4), rmaker_two],
            [(33, 4), (36, 4), rmaker_two],
            [(40, 4), (43, 4), rmaker_one],
            [(45, 4), (48, 4), rmaker_two],
        ]
    ]
)

voice_2_timespan_list = abjad.TimespanList(
    [
        abjad.AnnotatedTimespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            annotation=MusicSpecifier(rhythm_maker=rhythm_maker, voice_name="Voice 2"),
        )
        for start_offset, stop_offset, rhythm_maker in [
            [(4, 4), (7, 4), rmaker_two],
            [(9, 4), (12, 4), rmaker_one],
            [(16, 4), (19, 4), rmaker_two],
            [(21, 4), (24, 4), rmaker_one],
            [(24, 4), (27, 4), rmaker_one],
            [(29, 4), (32, 4), rmaker_two],
            [(36, 4), (39, 4), rmaker_one],
            [(41, 4), (44, 4), rmaker_two],
        ]
    ]
)

voice_3_timespan_list = abjad.TimespanList(
    [
        abjad.AnnotatedTimespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            annotation=MusicSpecifier(rhythm_maker=rhythm_maker, voice_name="Voice 3"),
        )
        for start_offset, stop_offset, rhythm_maker in [
            [(2, 4), (5, 4), rmaker_one],
            [(9, 4), (12, 4), rmaker_two],
            [(14, 4), (17, 4), rmaker_two],
            [(21, 4), (24, 4), rmaker_one],
            [(24, 4), (27, 4), rmaker_two],
            [(31, 4), (34, 4), rmaker_one],
            [(36, 4), (39, 4), rmaker_one],
            [(43, 4), (46, 4), rmaker_two],
        ]
    ]
)

voice_4_timespan_list = abjad.TimespanList(
    [
        abjad.AnnotatedTimespan(
            start_offset=start_offset,
            stop_offset=stop_offset,
            annotation=MusicSpecifier(rhythm_maker=rhythm_maker, voice_name="Voice 4"),
        )
        for start_offset, stop_offset, rhythm_maker in [
            [(0, 4), (3, 4), rmaker_two],
            [(6, 4), (9, 4), rmaker_two],
            [(10, 4), (13, 4), rmaker_one],
            [(17, 4), (21, 4), rmaker_two],
            [(25, 4), (29, 4), rmaker_one],
            [(33, 4), (36, 4), rmaker_one],
            [(38, 4), (41, 4), rmaker_two],
            [(45, 4), (48, 4), rmaker_one],
        ]
    ]
)


# Create a dictionary mapping voice names to timespan lists so we can
# maintain the association in later operations:


all_timespan_lists = {
    "Voice 1": voice_1_timespan_list,
    "Voice 2": voice_2_timespan_list,
    "Voice 3": voice_3_timespan_list,
    "Voice 4": voice_4_timespan_list,
}


# Determine the "global" timespan of all voices combined:


global_timespan = abjad.Timespan(
    start_offset=0, stop_offset=max(_.stop_offset for _ in all_timespan_lists.values())
)


# Using the global timespan, create silence timespans for each timespan list.
# We don't need to create any silences by-hand if we now the global start and
# stop offsets of all voices combined:

for voice_name, timespan_list in all_timespan_lists.items():
    # Here is another technique for finding where the silence timespans are. We
    # create a new timespan list consisting of the global timespan and all the
    # timespans from our current per-voice timespan list. Then we compute an
    # in-place logical XOR. The XOR will replace the contents of the "silences"
    # timespan list with a set of timespans representing those periods of time
    # where only one timespan from the original was present. This has the
    # effect of cutting out holes from the global timespan wherever a per-voice
    # timespan was found, but also preserves any silence before the first
    # per-voice timespan or after the last per-voice timespan. Then we merge
    # the newly-created silences back into the per-voice timespan list.
    silences = abjad.TimespanList([global_timespan])
    silences.extend(timespan_list)
    silences.sort()
    silences.compute_logical_xor()
    # Add the silences into the voice timespan list. We create new *annotated*
    # timespans so we can maintain the voice name information:
    for silence_timespan in silences:
        timespan_list.append(
            abjad.AnnotatedTimespan(
                start_offset=silence_timespan.start_offset,
                stop_offset=silence_timespan.stop_offset,
                annotation=MusicSpecifier(rhythm_maker=None, voice_name=voice_name),
            )
        )
    timespan_list.sort()


# Split the timespan list via the time signatures and collect the shards into a
# new timespan list


for voice_name, timespan_list in all_timespan_lists.items():
    shards = timespan_list.split_at_offsets(bounds)
    split_timespan_list = abjad.TimespanList()
    for shard in shards:
        split_timespan_list.extend(shard)
    split_timespan_list.sort()
    # We can replace the original timespan list in the dictionary of
    # timespan lists because we know the key it was stored at (its voice
    # name):
    all_timespan_lists[voice_name] = timespan_list


# Create a score structure


score = abjad.Score(
    [
        abjad.Staff(name="Global Context"),
        abjad.StaffGroup(
            [
                abjad.Staff([abjad.Voice(name="Voice 1")], name="Staff 1"),
                abjad.Staff([abjad.Voice(name="Voice 2")], name="Staff 2"),
                abjad.Staff([abjad.Voice(name="Voice 3")], name="Staff 3"),
                abjad.Staff([abjad.Voice(name="Voice 4")], name="Staff 4"),
            ],
            name="Staff Group",
        ),
    ]
)


# Teach each of the staves how to draw analysis brackets


for staff in score["Staff Group"]:
    staff.consists_commands.append("Horizontal_bracket_engraver")


# Add skips and time signatures to the global context


for time_signature in time_signatures:
    skip = abjad.Skip(1)
    abjad.attach(abjad.Multiplier(time_signature), skip)
    abjad.attach(time_signature, skip)
    score["Global Context"].append(skip)


# Define a helper function that takes a rhythm maker and some durations and
# outputs a container. This helper function also adds LilyPond analysis
# brackets to make it clearer where the phrase and sub-phrase boundaries are.


def make_container(rhythm_maker, durations):
    selections = rhythm_maker(durations)
    container = abjad.Container(selections)
    # Add analysis brackets so we can see the phrasing graphically
    start_indicator = abjad.LilyPondLiteral("\startGroup", format_slot="after")
    stop_indicator = abjad.LilyPondLiteral("\stopGroup", format_slot="after")
    for cell in selections:
        cell_first_leaf = abjad.select(cell).leaves()[0]
        cell_last_leaf = abjad.select(cell).leaves()[-1]
        abjad.attach(start_indicator, cell_first_leaf)
        abjad.attach(stop_indicator, cell_last_leaf)
    # The extra space in the literals is a hack around a check for whether an
    # identical object has already been attached
    start_indicator = abjad.LilyPondLiteral("\startGroup ", format_slot="after")
    stop_indicator = abjad.LilyPondLiteral("\stopGroup ", format_slot="after")
    phrase_first_leaf = abjad.select(container).leaves()[0]
    phrase_last_leaf = abjad.select(container).leaves()[-1]
    abjad.attach(start_indicator, phrase_first_leaf)
    abjad.attach(stop_indicator, phrase_last_leaf)
    return container


# Loop over the timespan list dictionaries, spitting out pairs of voice
# names and per-voice timespan lists. Group timespans into phrases, with
# all timespans in each phrase having an identical rhythm maker. Run the
# rhythm maker against the durations of the timespans in the phrase and
# add the output to the voice with the timespan lists's voice name.


def key_function(timespan):
    """
    Get the timespan's annotation's rhythm-maker.

    If the annotation's rhythm-maker is None, return the silence maker.
    """
    return timespan.annotation.rhythm_maker or silence_maker


for voice_name, timespan_list in all_timespan_lists.items():
    for rhythm_maker, grouper in itertools.groupby(timespan_list, key=key_function):
        # We know the voice name of each timespan because a) the timespan
        # list is in a dictionary, associated with that voice name and b)
        # each timespan's annotation is a MusicSpecifier instance which
        # knows the name of the voice the timespan should be used for.
        # This double-reference to the voice is redundant here, but in a
        # different implementation we could put *all* the timespans into
        # one timespan list, split them, whatever, and still know which
        # voice they belong to because their annotation records that
        # information.
        durations = [timespan.duration for timespan in grouper]
        container = make_container(rhythm_maker, durations)
        voice = score[voice_name]
        voice.append(container)


# Loop over the voices and replace full-measure single rests (lowercase
# "r") with proper multi-measure rests (upper-case "R"). The easiest way
# to loop over time-signature-sized chunks is to use
# abjad.mutate(...).split(), even if the contents of the voice are already
# split:


for voice in abjad.iterate(score).components(abjad.Voice):
    leaves = abjad.select(voice).leaves()
    for shard in abjad.mutate(leaves).split(time_signatures):
        if not all(isinstance(leaf, abjad.Rest) for leaf in shard):
            continue
        multiplier = abjad.Multiplier(abjad.inspect(shard).duration())
        multimeasure_rest = abjad.MultimeasureRest(1)
        abjad.attach(multiplier, multimeasure_rest)
        abjad.mutate(shard).replace(multimeasure_rest)


# Make a lilypond file and show it:


lilypond_file = abjad.LilyPondFile.new(score)

abjad.show(score)
