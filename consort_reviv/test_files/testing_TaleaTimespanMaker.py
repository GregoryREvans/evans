import abjad
import collections
import abjadext.rmakers
from evans.consort_reviv.TaleaTimespanMaker import TaleaTimespanMaker

timespan_maker = TaleaTimespanMaker(
    initial_silence_talea=abjadext.rmakers.Talea(
        counts=(0, 4),
        denominator=16,
        )
    )
print(format(timespan_maker))

######

# music_specifiers = collections.OrderedDict([ ###DOES NOT WORK DUE TO LINE 149 IN TIMESPANMAKER
#     ('Violin', None),
#     ('Viola', None),
#     ])
# target_timespan = abjad.Timespan(0, 1)
# timespan_inventory = timespan_maker(
#     music_specifiers=music_specifiers,
#     target_timespan=target_timespan,
#     )
# print(format(timespan_inventory))

######

# timespan_maker = abjad.new(timespan_maker, ###DOES NOT WORK DUE TO LINE 149 IN TIMESPANMAKER
#     initial_silence_talea=None,
#     synchronize_step=True,
#     )
# timespan_inventory = timespan_maker(
#     music_specifiers=music_specifiers,
#     target_timespan=target_timespan,
#     )
# print(format(timespan_inventory))

######

# timespan_maker = abjad.new(timespan_maker,  ###DOES NOT WORK DUE TO LINE 149 IN TIMESPANMAKER
#     initial_silence_talea=abjadext.rmakers.Talea(
#         counts=(0, 2),
#         denominator=16,
#         ),
#     )
# timespan_inventory = timespan_maker(
#     music_specifiers=music_specifiers,
#     target_timespan=target_timespan,
#     )
# print(format(timespan_inventory))
