import abjad

clef = abjad.Clef("treble")

staff = abjad.Staff("c'4 d' e' f' g' a' b' c''")

abjad.attach(clef, staff[0])

selection = abjad.select(staff[:2]).leaves(pitched=True)
for note in selection:
    abjad.override(note).note_head.color = "red"

target_timespan = abjad.Timespan(start_offset=(2, 4), stop_offset=(4, 4))

# for tie in abjad.select(staff).logical_ties(pitched=True): ##THIS WORKS
#     if abjad.inspect(tie).timespan().happens_during_timespan(target_timespan) is True:
#         for note in abjad.select(tie).leaves():
#             note.written_pitch = note.written_pitch + 2

# bool = lambda x: abjad.inspect(x).timespan().happens_during_timespan(target_timespan)
# print(bool(staff[0]))

for group in (
    abjad.select(staff)
    .logical_ties(pitched=True)
    .group_by(
        predicate=lambda x: abjad.inspect(x)
        .timespan()
        .happens_during_timespan(target_timespan)
    )
):
    if (
        abjad.inspect(group).timespan().happens_during_timespan(target_timespan) is True
    ):  ##THIE WORKS TOO, BUT IS IT FASTER?
        for tie in abjad.select(group).logical_ties(pitched=True):
            for leaf in abjad.select(tie).leaves():
                leaf.written_pitch = leaf.written_pitch + 6
                abjad.override(leaf).note_head.color = "blue"

abjad.f(staff)
