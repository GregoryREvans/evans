"""
Timespan classes and functions.
"""
import os
import re

import abjad
from abjadext import rmakers

from . import handlers
from .commands import RhythmCommand

env = os.path.expanduser("~")

assert isinstance(env, str)

abjad_stylesheet = os.path.join(env, "abjad/docs/source/_stylesheets/abjad.ily")

dir_path = os.path.split(__file__)[0]
rhythm_stylesheet = os.path.join(dir_path, "_rhythm_sketch_stylesheet.ily")


class SilentTimespan(abjad.Timespan):
    r"""
    Silent Timespan

    ..  container:: example

        >>> span = evans.SilentTimespan(0, 1)
        >>> abjad.show(span) # doctest: +SKIP

        .. docs::

            >>> print(abjad.storage(span))
            evans.SilentTimespan(
                abjad.Offset((0, 1)),
                abjad.Offset((1, 1))
                )

    """

    def __init__(self, start_offset, stop_offset, annotation=None):
        abjad.Timespan.__init__(self, start_offset, stop_offset)
        self.annotation = annotation

    def __str__(self):
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)

    def _as_postscript(
        self, postscript_x_offset, postscript_y_offset, postscript_scale
    ):
        start = float(self._start_offset) * postscript_scale
        start -= postscript_x_offset
        stop = float(self._stop_offset) * postscript_scale
        stop -= postscript_x_offset
        ps = abjad.Postscript()
        ps = ps.setdash([0.5])
        ps = ps.moveto(start, postscript_y_offset)
        ps = ps.lineto(stop, postscript_y_offset)
        ps = ps.stroke()
        ps = ps.moveto(start, postscript_y_offset + 0.75)
        ps = ps.lineto(start, postscript_y_offset - 0.75)
        ps = ps.setdash()
        ps = ps.stroke()
        ps = ps.moveto(stop, postscript_y_offset + 0.75)
        ps = ps.lineto(stop, postscript_y_offset - 0.75)
        ps = ps.stroke()
        return ps


class TimespanMaker:
    r"""

    ..  container:: example

        >>> timespan_maker = evans.TimespanMaker(
        ...     denominator=8,
        ...     total_duration=abjad.Duration(15, 2),
        ... )
        ...
        >>> counts = [3, 5, -3, 4, 7, -1]
        >>> timespan_list = timespan_maker(counts, max_duration=6, voice_name="A")
        >>> abjad.show(timespan_list, scale=0.5) # doctest: +SKIP

        .. docs::

            >>> print(abjad.storage(timespan_list))
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset((0, 1)),
                        stop_offset=abjad.Offset((3, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((3, 8)),
                        stop_offset=abjad.Offset((1, 1)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((11, 8)),
                        stop_offset=abjad.Offset((15, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((15, 8)),
                        stop_offset=abjad.Offset((21, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((23, 8)),
                        stop_offset=abjad.Offset((13, 4)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((13, 4)),
                        stop_offset=abjad.Offset((31, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((17, 4)),
                        stop_offset=abjad.Offset((19, 4)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((19, 4)),
                        stop_offset=abjad.Offset((11, 2)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((23, 4)),
                        stop_offset=abjad.Offset((49, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((49, 8)),
                        stop_offset=abjad.Offset((27, 4)),
                        annotation='A',
                        ),
                    ]
                )

    ..  container:: example

        >>> timespan_maker = evans.TimespanMaker(
        ...     denominator=8,
        ...     total_duration=abjad.Duration(15, 2),
        ... )
        ...
        >>> counts = [3, 1, -2, 2, 3, -1, 2, -2]
        >>> timespan_list_1 = timespan_maker(counts, max_duration=6, voice_name="A")
        >>> timespan_list_2 = timespan_maker(
        ...     counts,
        ...     max_duration=6,
        ...     voice_name="B",
        ...     rotation=2,
        ...     translation=1
        ... )
        ...
        >>> timespan_list_3 = timespan_maker(
        ...     counts,
        ...     max_duration=6,
        ...     voice_name="C",
        ...     rotation=5,
        ...     translation=3
        ... )
        ...
        >>> timespan_list_4 = timespan_maker(
        ...     counts,
        ...     max_duration=6,
        ...     voice_name="D",
        ...     rotation=3,
        ...     translation=2
        ... )
        ...
        >>> timespanlist = abjad.TimespanList()
        >>> for span in timespan_list_1:
        ...     timespanlist.append(span)
        ...
        >>> for span in timespan_list_2:
        ...     timespanlist.append(span)
        ...
        >>> for span in timespan_list_3:
        ...     timespanlist.append(span)
        ...
        >>> for span in timespan_list_4:
        ...     timespanlist.append(span)
        ...
        >>> abjad.show(timespanlist, scale=0.5, key="annotation") # doctest: +SKIP

        .. docs::

            >>> print(abjad.storage(timespanlist))
            abjad.TimespanList(
                [
                    abjad.Timespan(
                        start_offset=abjad.Offset((0, 1)),
                        stop_offset=abjad.Offset((3, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((3, 8)),
                        stop_offset=abjad.Offset((1, 2)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((3, 4)),
                        stop_offset=abjad.Offset((1, 1)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((1, 1)),
                        stop_offset=abjad.Offset((11, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((3, 2)),
                        stop_offset=abjad.Offset((7, 4)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((2, 1)),
                        stop_offset=abjad.Offset((19, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((19, 8)),
                        stop_offset=abjad.Offset((5, 2)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((11, 4)),
                        stop_offset=abjad.Offset((3, 1)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((3, 1)),
                        stop_offset=abjad.Offset((27, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((7, 2)),
                        stop_offset=abjad.Offset((15, 4)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((4, 1)),
                        stop_offset=abjad.Offset((35, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((35, 8)),
                        stop_offset=abjad.Offset((9, 2)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((19, 4)),
                        stop_offset=abjad.Offset((5, 1)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((5, 1)),
                        stop_offset=abjad.Offset((43, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((11, 2)),
                        stop_offset=abjad.Offset((23, 4)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((6, 1)),
                        stop_offset=abjad.Offset((51, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((51, 8)),
                        stop_offset=abjad.Offset((13, 2)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((27, 4)),
                        stop_offset=abjad.Offset((7, 1)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((7, 1)),
                        stop_offset=abjad.Offset((59, 8)),
                        annotation='A',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((3, 8)),
                        stop_offset=abjad.Offset((5, 8)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((5, 8)),
                        stop_offset=abjad.Offset((1, 1)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((9, 8)),
                        stop_offset=abjad.Offset((11, 8)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((13, 8)),
                        stop_offset=abjad.Offset((2, 1)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((2, 1)),
                        stop_offset=abjad.Offset((17, 8)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((19, 8)),
                        stop_offset=abjad.Offset((21, 8)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((21, 8)),
                        stop_offset=abjad.Offset((3, 1)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((25, 8)),
                        stop_offset=abjad.Offset((27, 8)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((29, 8)),
                        stop_offset=abjad.Offset((4, 1)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((4, 1)),
                        stop_offset=abjad.Offset((33, 8)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((35, 8)),
                        stop_offset=abjad.Offset((37, 8)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((37, 8)),
                        stop_offset=abjad.Offset((5, 1)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((41, 8)),
                        stop_offset=abjad.Offset((43, 8)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((45, 8)),
                        stop_offset=abjad.Offset((6, 1)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((6, 1)),
                        stop_offset=abjad.Offset((49, 8)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((51, 8)),
                        stop_offset=abjad.Offset((53, 8)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((53, 8)),
                        stop_offset=abjad.Offset((7, 1)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((57, 8)),
                        stop_offset=abjad.Offset((59, 8)),
                        annotation='B',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((1, 2)),
                        stop_offset=abjad.Offset((3, 4)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((1, 1)),
                        stop_offset=abjad.Offset((11, 8)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((11, 8)),
                        stop_offset=abjad.Offset((3, 2)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((7, 4)),
                        stop_offset=abjad.Offset((2, 1)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((2, 1)),
                        stop_offset=abjad.Offset((19, 8)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((5, 2)),
                        stop_offset=abjad.Offset((11, 4)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((3, 1)),
                        stop_offset=abjad.Offset((27, 8)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((27, 8)),
                        stop_offset=abjad.Offset((7, 2)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((15, 4)),
                        stop_offset=abjad.Offset((4, 1)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((4, 1)),
                        stop_offset=abjad.Offset((35, 8)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((9, 2)),
                        stop_offset=abjad.Offset((19, 4)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((5, 1)),
                        stop_offset=abjad.Offset((43, 8)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((43, 8)),
                        stop_offset=abjad.Offset((11, 2)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((23, 4)),
                        stop_offset=abjad.Offset((6, 1)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((6, 1)),
                        stop_offset=abjad.Offset((51, 8)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((13, 2)),
                        stop_offset=abjad.Offset((27, 4)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((7, 1)),
                        stop_offset=abjad.Offset((59, 8)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((59, 8)),
                        stop_offset=abjad.Offset((15, 2)),
                        annotation='C',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((1, 4)),
                        stop_offset=abjad.Offset((1, 2)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((1, 2)),
                        stop_offset=abjad.Offset((7, 8)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((1, 1)),
                        stop_offset=abjad.Offset((5, 4)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((3, 2)),
                        stop_offset=abjad.Offset((15, 8)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((15, 8)),
                        stop_offset=abjad.Offset((2, 1)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((9, 4)),
                        stop_offset=abjad.Offset((5, 2)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((5, 2)),
                        stop_offset=abjad.Offset((23, 8)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((3, 1)),
                        stop_offset=abjad.Offset((13, 4)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((7, 2)),
                        stop_offset=abjad.Offset((31, 8)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((31, 8)),
                        stop_offset=abjad.Offset((4, 1)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((17, 4)),
                        stop_offset=abjad.Offset((9, 2)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((9, 2)),
                        stop_offset=abjad.Offset((39, 8)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((5, 1)),
                        stop_offset=abjad.Offset((21, 4)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((11, 2)),
                        stop_offset=abjad.Offset((47, 8)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((47, 8)),
                        stop_offset=abjad.Offset((6, 1)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((25, 4)),
                        stop_offset=abjad.Offset((13, 2)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((13, 2)),
                        stop_offset=abjad.Offset((55, 8)),
                        annotation='D',
                        ),
                    abjad.Timespan(
                        start_offset=abjad.Offset((7, 1)),
                        stop_offset=abjad.Offset((29, 4)),
                        annotation='D',
                        ),
                    ]
                )

    """

    __slots__ = ["_denominator", "_total_duration"]

    def __init__(self, denominator, total_duration):
        self._denominator = denominator
        self._total_duration = abjad.Duration(total_duration)

    def __str__(self):
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)

    def __call__(
        self, counts, max_duration=None, translation=0, rotation=None, voice_name=None
    ):
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
                abjad.Timespan(
                    start_offset=(start, denominator),
                    stop_offset=(stop, denominator),
                    annotation=voice_name,
                )
            )
            increment_total += count
        return timespan_list

    def _ready_counts(self, counts, translation):
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


class TimespanSpecifier:
    def __init__(self, voice_name=None, handler=None):
        self.voice_name = voice_name
        self.handler = handler

    def __str__(self):
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)


def make_split_list(timespan_list, offsets):
    return abjad.TimespanList(
        [
            timespan
            for timespanlist in timespan_list.split_at_offsets(offsets)
            for timespan in timespanlist
        ]
    )


def collect_offsets(timespan_list):
    offsets = [timespan.start_offset for timespan in timespan_list]
    for stop_offset in [timespan.stop_offset for timespan in timespan_list]:
        if stop_offset not in offsets:
            offsets.append(stop_offset)
    offsets.sort()
    return offsets


def make_showable_list(timespan_lists):
    master_list = abjad.TimespanList([])
    for i, timespan_list in enumerate(timespan_lists):
        for timespan in timespan_list:
            if isinstance(timespan, SilentTimespan):
                new_span = SilentTimespan(
                    start_offset=timespan.start_offset,
                    stop_offset=timespan.stop_offset,
                    annotation=str(i + 1),
                )
            else:
                new_span = abjad.Timespan(
                    start_offset=timespan.start_offset,
                    stop_offset=timespan.stop_offset,
                    annotation=str(i + 1),
                )
            master_list.extend([new_span])
    master_list.sort()
    return master_list


def add_silent_timespans(timespan_list, specifier=None):
    silent_timespans = abjad.TimespanList(
        [
            abjad.Timespan(
                start_offset=0, stop_offset=max(_.stop_offset for _ in timespan_list)
            )
        ]
    )
    for timespan in timespan_list:
        silent_timespans -= timespan
    for silent_timespan in silent_timespans:
        timespan_list.extend(
            [
                SilentTimespan(
                    start_offset=silent_timespan.start_offset,
                    stop_offset=silent_timespan.stop_offset,
                    annotation=specifier,
                )
            ]
        )
    return timespan_list


def add_silences_to_timespan_lists(timespan_lists):
    for timespan_list in timespan_lists:
        timespan_list = add_silent_timespans(timespan_list)
        timespan_list.sort()


def add_silences_to_timespan_dict(timespan_dict, specifier=None):
    max_stop_offset = max(_.stop_offset for _ in timespan_dict.values())
    for timespan_list in timespan_dict.values():
        silences = SilentTimespan(0, max_stop_offset)
        for timespan in timespan_list:
            silences -= timespan
        for silence in silences:
            silence.annotation = specifier
            timespan_list.extend([silence])
        timespan_list.sort()


def talea_timespans(talea, advancement=0):
    talea = abjad.new(talea)
    talea = talea.advance(advancement)
    timespans = abjad.TimespanList([])
    total_duration = 0
    for duration in talea:
        start = total_duration
        stop = total_duration + abs(duration)
        if duration < 0:
            timespan = SilentTimespan(
                start_offset=start, stop_offset=stop, annotation=None
            )
        else:
            timespan = abjad.Timespan(
                start_offset=start, stop_offset=stop, annotation=None
            )
        timespans.append(timespan)
        total_duration += abs(duration)
    return timespans


def to_digit(string):
    r"""

    ..  container:: example

        >>> evans.to_digit("2")
        2

    """
    return int(string) if string.isdigit() else string


def sorted_keys(text):
    """

    ..  container:: example

        >>> evans.sorted_keys("Voice 1")
        ['Voice ', 1, '']

    """
    return [to_digit(_) for _ in re.split(r"(\d+)", text)]


def human_sorted_keys(pair):
    key, timespan = pair
    values = [to_digit(_) for _ in key.split()]
    hashable_key = tuple(values)
    return hashable_key


def intercalate_silences(rhythm_command_list, voice_names=None):
    global_timespan = abjad.Timespan(
        start_offset=0,
        stop_offset=max(_.timespan.stop_offset for _ in rhythm_command_list),
    )
    silence_maker = handlers.RhythmHandler(
        rmakers.stack(
            rmakers.NoteRhythmMaker(),
            rmakers.force_rest(lambda _: abjad.Selection(_).leaves(pitched=True)),
        ),
        name="silence_maker",
    )
    if voice_names is None:
        voice_names = sorted(set(_.voice_name for _ in rhythm_command_list))
    for voice_name in voice_names:
        timespan_list = abjad.TimespanList(
            [_.timespan for _ in rhythm_command_list if _.voice_name == voice_name]
        )
        silences = abjad.TimespanList([global_timespan])
        for timespan in timespan_list:
            silences -= timespan
        for timespan in silences:
            new_command = RhythmCommand(
                voice_name,
                timespan,
                silence_maker,
            )
            rhythm_command_list.append(new_command)
