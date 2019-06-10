import abjad
from evans.consort_reviv.LogicalTieCollection import LogicalTieCollection

clef = abjad.Clef('treble')

staff = abjad.Staff("c'4 d' e' f' g' a' b' c''")

abjad.attach(clef, staff[0])

selection = abjad.select(staff[:2]).leaves(pitched=True)
for note in selection:
    abjad.override(note).note_head.color = 'red'

target_timespan = abjad.Timespan(start_offset=(2, 4), stop_offset=(4, 4))

tie_selection = abjad.select(staff).logical_ties()
tie_collection = LogicalTieCollection()
for tie in tie_selection:
    tie_collection.insert(tie)

for tie in tie_collection.find_logical_ties_intersecting_timespan(target_timespan):
    for leaf in tie:
        leaf.written_pitch = leaf.written_pitch + 6
        abjad.override(leaf).note_head.color = 'blue'

abjad.show(staff)
