import abjad
from abjadext import rmakers
import timespan_functions

talea = rmakers.Talea(counts=[5, 3, -1, 6, -7, 2], denominator=4)

timespans = timespan_functions.talea_timespans(talea)
abjad.show(timespans, scale=0.65)

time_signatures = [abjad.TimeSignature((n, 8)) for n in [3, 4, 3, 4, 3, 5, 3, 4]] * 2
offsets = abjad.mathtools.cumulative_sums(
    [abjad.Offset(t_s.duration) for t_s in time_signatures]
)

split_list = timespan_functions.make_split_list(timespans, offsets)
abjad.show(split_list, scale=0.65)
