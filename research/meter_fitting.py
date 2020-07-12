import collections

import abjad
import tsmakers
from abjadext import rmakers as rmakers

music_specifiers = collections.OrderedDict(
    [
        ("Voice 1", "music specifier"),
        ("Voice 2", None),
        ("Voice 3", None),
        ("Voice 4", None),
        ("Voice 5", None),
        ("Voice 6", None),
        ("Voice 7", None),
        ("Voice 8", None),
        ("Voice 9", None),
        ("Voice 9+1", None),
    ]
)

target_timespan = abjad.Timespan(0, 8)

timespan_maker = tsmakers.TaleaTimespanMaker(
    initial_silence_talea=rmakers.Talea(counts=(0, 5, 3, 6, 2), denominator=8),
    # synchronize_step=True, #goes down voices instead of across? maybe not consistent...
    # synchronize_groupings=True, #goes down voices instead of across? maybe not consistent...
    playing_talea=rmakers.Talea(counts=(5, 3, 1, 2, 6), denominator=4),
    playing_groupings=(
        1,
        2,
        3,
        2,
    ),  # smashes timespans together without intermittent silence
    silence_talea=rmakers.Talea(counts=(2, 1, 1), denominator=4),
    # fuse_groups=False, #turns groups from multiple timespans into one large timespan
)

timespan_list = timespan_maker(
    music_specifiers=music_specifiers, target_timespan=target_timespan
)

# abjad.show(timespan_list, scale=0.7, key='voice_name')
timespan_list
#
offset_counter = abjad.OffsetCounter(timespan_list)

# abjad.show(offset_counter, scale=0.7)
####
permitted_meters = abjad.MeterList([(3, 4), (4, 4), (5, 16), (7, 8)])

# abjad.show(permitted_meters, scale=0.7)
#
fitted_meters = abjad.Meter.fit_meters(
    argument=offset_counter, meters=permitted_meters, maximum_run_length=1
)

# abjad.show(fitted_meters, scale=0.7)

# groups = [timespan.voice_name for timespan in timespan_list]
# input = [(span, group) for span, group in zip(timespan_list, groups)]
#
# from collections import defaultdict
# res = defaultdict(list)
# for v, k in input: res[k].append(v)
# x = [{'type':k, 'items':v} for k,v in res.items()]
# print(x[1])
