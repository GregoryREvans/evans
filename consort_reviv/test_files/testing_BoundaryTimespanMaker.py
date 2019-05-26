import abjad
import abjadext.rmakers
from evans.consort_reviv.BoundaryTimespanMaker import BoundaryTimespanMaker
from evans.consort_reviv.PerformedTimespan import PerformedTimespan

timespan_maker = BoundaryTimespanMaker(
    start_talea=abjadext.rmakers.Talea(
        counts=[1],
        denominator=2,
        ),
    stop_talea=abjadext.rmakers.Talea(
        counts=[1],
        denominator=4,
        ),
    voice_names=('Violin 1 Voice', 'Violin 2 Voice'),
    )
print(format(timespan_maker))

###### The following does not work yet
#
# timespan_inventory = abjad.TimespanList([
#     PerformedTimespan(
#         start_offset=0,
#         stop_offset=1,
#         voice_name='Violin 1 Voice',
#         ),
#     PerformedTimespan(
#         start_offset=(1, 2),
#         stop_offset=(3, 2),
#         voice_name='Violin 2 Voice',
#         ),
#     PerformedTimespan(
#         start_offset=3,
#         stop_offset=4,
#         voice_name='Violin 2 Voice',
#         ),
# ])
# music_specifiers = {'Cello Voice': None}
# target_timespan = abjad.Timespan(0, 10)
# timespan_inventory = timespan_maker(
#     music_specifiers=music_specifiers,
#     target_timespan=target_timespan,
#     timespan_inventory=timespan_inventory,
#     )
# print(format(timespan_inventory))
