import abjad 
import tsmakers
from abjadext import rmakers 


timespan_maker = tsmakers.BoundaryTimespanMaker(
    start_talea=rmakers.Talea(
        counts=[1],
        denominator=2,
    ),
    stop_talea=rmakers.Talea(
        counts=[1],
        denominator=4,
    ),
    voice_names=('Violin 1 Voice', 'Violin 2 Voice'),
)

abjad.f(timespan_maker)


initial_list = abjad.TimespanList([
    tsmakers.PerformedTimespan(
        start_offset=0,
        stop_offset=1,
        voice_name='Violin 1 Voice',
    ),
    tsmakers.PerformedTimespan(
        start_offset=(1, 2),
        stop_offset=(3, 2),
        voice_name='Violin 2 Voice',
    ),
    tsmakers.PerformedTimespan(
        start_offset=3,
        stop_offset=4,
        voice_name='Violin 2 Voice',
    ),
])


music_specifiers = {'Cello Voice': None}
target_timespan = abjad.Timespan(0, 10)
timespan_list = timespan_maker(
    music_specifiers=music_specifiers,
    target_timespan=target_timespan,
    timespan_list=initial_list,
)


abjad.f(timespan_list)
abjad.show(timespan_list, scale=0.65)
