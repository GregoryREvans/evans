import abjad
import tsmakers
from abjadext import rmakers

timespan_maker = tsmakers.CascadingTimespanMaker()
abjad.f(timespan_maker)
music_specifiers = abjad.OrderedDict([
    ('A', None),
    ('B', None),
    ('C', None),
    ('D', None),
])
target_timespan = abjad.Timespan(0, 2)
timespan_list = timespan_maker(
    music_specifiers=music_specifiers,
    target_timespan=target_timespan,
)

abjad.f(timespan_list)


timespan_maker = abjad.new(
    timespan_maker,
    playing_groupings=(1, 2),
    cascade_pattern=(2, -1),
)
timespan_list = timespan_maker(
    music_specifiers=music_specifiers,
    target_timespan=target_timespan,
)

abjad.f(timespan_list)
abjad.show(timespan_list, scale=0.65)
