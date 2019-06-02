import abjad 
import tsmakers
from abjadext import rmakers

timespan_maker = tsmakers.DependentTimespanMaker(
    include_inner_starts=True,
    include_inner_stops=True,
    voice_names=(
        'Viola Voice',
    ),
)

abjad.f(timespan_maker)



timespan_list = abjad.TimespanList([
    tsmakers.PerformedTimespan(
        voice_name='Viola Voice',
        start_offset=(1, 4),
        stop_offset=(1, 1),
    ),
    tsmakers.PerformedTimespan(
        voice_name='Viola Voice',
        start_offset=(3, 4),
        stop_offset=(3, 2),
    ),
])

music_specifiers = {
    'Violin Voice': None,
    'Cello Voice': None,
}
target_timespan = abjad.Timespan((1, 2), (2, 1))
timespan_list = timespan_maker(
    music_specifiers=music_specifiers,
    target_timespan=target_timespan,
    timespan_list=timespan_list,
)

abjad.f(timespan_list)
abjad.show(timespan_list, scale=0.65)
