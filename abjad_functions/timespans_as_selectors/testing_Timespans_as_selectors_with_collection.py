import abjad
from evans.consort_reviv.LogicalTieCollection import LogicalTieCollection

clef = abjad.Clef('treble')

staff = abjad.Staff("c'4 d' e' f' g' a' b' c''")

abjad.attach(clef, staff[0])

selection = abjad.select(staff[:2]).leaves(pitched=True)
for note in selection:
    abjad.override(note).note_head.color = 'red'

target_timespan = abjad.Timespan(start_offset=(2, 4), stop_offset=(4, 4))

tie_selection = abjad.select(staff).logical_ties() #.goup_by(predicate=abjad.Voice)
leaf_selection = abjad.select(staff).leaves()
tie_selection_timespans = []
for _ in tie_selection:
    tie_selection_timespans.append(abjad.inspect(_).timespan())

# tie_collection = LogicalTieCollection(leaf_selection[:])
tie_collection = LogicalTieCollection(tie_selection)
# tie_collection = LogicalTieCollection(tie_selection_timespans)

for selection in tie_collection.find_logical_ties_intersecting_timespan(target_timespan):
    for tie in selection:
        print(abjad.inspect(tie).timespan())

# print(' ')
#
# for _ in leaf_selection:
#     if hasattr(_, '_get_timespan'):
#         abjad.f(_)

# abjad.f(staff)/
