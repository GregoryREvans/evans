import abjad 
import tsmakers
from abjadext import rmakers 

timespan_maker = tsmakers.TaleaTimespanMaker(
    initial_silence_talea=rmakers.Talea(
        counts=(1, 4, 1), 
        denominator=16
    ),
    silence_talea=rmakers.Talea(
        counts=(0, 5),
        denominator=(32)
    )
)
abjad.f(timespan_maker)

music_specifiers = abjad.OrderedDict([
    ('Violin', None),
    ('Viola', None),
])

target_timespan = abjad.Timespan(0, 10)

timespan_list = timespan_maker(
    music_specifiers=music_specifiers,
    target_timespan=target_timespan,
)

abjad.f(timespan_list)
abjad.show(timespan_list)

