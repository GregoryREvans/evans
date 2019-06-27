import abjad


def make_split_list(timespan_list, offsets):
    """Splits Timespans within TimespanList by offsets

    Returns:
        TimespanList
    """
    return abjad.TimespanList(
        [
            timespan
            for timespanlist in timespan_list.split_at_offsets(offsets)
            for timespan in timespanlist
        ]
    )


class TimespanMaker(object):
    """Timespan Maker"""

    __slots__ = ["_denominator", "_total_duration"]

    def __init__(self, denominator, total_duration):
        self._denominator = denominator
        self._total_duration = abjad.Duration(total_duration)

    def __call__(self, counts, max_duration=None, translation=0, rotation=None):
        """Call timespan maker on series of counts
        """
        if rotation:
            counts = counts[rotation:] + counts[:rotation]
        counts = self._ready_counts(counts, translation)
        denominator = self.denominator
        increment_total = 0 + translation
        timespan_list = abjad.TimespanList([])
        for count in counts:
            if count < 0:
                increment_total += abs(count)
                continue
            start = increment_total
            stop = start + count
            if max_duration is not None:
                stop = (max_duration + start) if count > max_duration else stop
            timespan_list.append(
                abjad.AnnotatedTimespan(
                    start_offset=(start, denominator),
                    stop_offset=(stop, denominator),
                    annotation=None,
                )
            )
            increment_total += count
        return timespan_list

    def _ready_counts(self, counts, translation):
        """Repeats counts to fill total duration
        """
        total_duration = self.total_duration
        normalized_duration = total_duration.with_denominator(self.denominator)
        total_numerator = normalized_duration.numerator - translation
        counts = abjad.CyclicTuple(counts)
        repeated_counts = []
        increment = 0
        previous_sum = 0
        while previous_sum < total_numerator:
            new_sum = sum(abs(_) for _ in repeated_counts)
            count = counts[increment]
            if new_sum + count <= total_numerator:
                repeated_counts.append(count)
                increment += 1
                continue
            break
        return repeated_counts

    @property
    def denominator(self):
        return self._denominator

    @property
    def total_duration(self):
        return self._total_duration


### DEMO ###

# timespan_maker = TimespanMaker(
#     denominator=8,
#     total_duration=abjad.Duration(15, 2),
# )
# counts = [3, 5, -3, 4, 7, -1]
#
# timespan_list = timespan_maker(counts, max_duration=6)
# timespan_list_1 = timespan_maker(counts, max_duration=1)
# timespan_list_2 = timespan_maker(counts, max_duration=2, translation=5)
# timespan_list_3 = timespan_maker(
#     counts, max_duration=3, translation=5, rotation=2)
#
# # for tspan_list in [timespan_list, timespan_list_1, timespan_list_2, timespan_list_3]:
# #     abjad.show(tspan_list, scale=0.65)
# timespan_list.extend(timespan_list_1)
# timespan_list.extend(timespan_list_2)
# timespan_list.extend(timespan_list_3)
# abjad.show(timespan_list, scale=0.5)
