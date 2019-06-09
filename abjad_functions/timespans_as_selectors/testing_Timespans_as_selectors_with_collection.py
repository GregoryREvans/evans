import abjad
from evans.consort_reviv.TimespanCollection import TimespanCollection

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

tie_collection = TimespanCollection(leaf_selection[:])
# tie_collection = TimespanCollection(tie_selection)
# tie_collection = TimespanCollection(tie_selection_timespans)

for _ in tie_collection:
    abjad.f(_)

print(' ')

for _ in leaf_selection:
    if hasattr(_, '_get_timespan'):
        abjad.f(_)

# abjad.f(staff)/
