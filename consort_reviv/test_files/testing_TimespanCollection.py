import abjad
from evans.consort_reviv.TimespanCollection import TimespanCollection

timespans = (
    abjad.Timespan(0, 3),
    abjad.Timespan(1, 3),
    abjad.Timespan(1, 2),
    abjad.Timespan(2, 5),
    abjad.Timespan(6, 9),
    )
timespan_collection = TimespanCollection(timespans)

for x in timespan_collection.find_timespans_overlapping_offset(1.5):
    print(x)

timespan = abjad.Timespan(2, 4)
for x in timespan_collection.find_timespans_intersecting_timespan(timespan):
    print(x)

print(timespan_collection.all_offsets)

print(timespan_collection.all_start_offsets)

print(timespan_collection.all_stop_offsets)
