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
