import os

import abjad

env = os.path.expanduser('~')

assert isinstance(env, str)

abjad_stylesheet = os.path.join(env, "abjad/docs/source/_stylesheets/abjad.ily")

dir_path = os.path.split(__file__)[0]
rhythm_stylesheet = os.path.join(dir_path, "_rhythm_sketch_stylesheet.ily")


class SilentTimespan(abjad.Timespan):
    """
    Silent Timespan
    """

    def __init__(self, start_offset, stop_offset, annotation=None):
        """Initializer

        Arguments:
            start_offset
            stop_offset

        Keyword Arguments:
            annotation -- (default: {None})
        """

        abjad.Timespan.__init__(self, start_offset, stop_offset)
        self.annotation = annotation

    def _as_postscript(
        self, postscript_x_offset, postscript_y_offset, postscript_scale
    ):
        import abjad

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


class TimespanSpecifier:
    """Generic specifier for annotation
    """

    def __init__(self, voice_name=None, handler=None):
        self.voice_name = voice_name
        self.handler = handler

        def __repr__(self):
            return f"TimespanSpecifier(voice_name={self.voice_name})"


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


def collect_offsets(timespan_list):
    """Collects start and stop offsets from timespans in list (without repetition)

    Returns:
        List of offsets
    """

    offsets = [timespan.start_offset for timespan in timespan_list]
    for stop_offset in [timespan.stop_offset for timespan in timespan_list]:
        if stop_offset not in offsets:
            offsets.append(stop_offset)
    offsets.sort()
    return offsets


def make_showable_list(timespan_lists):
    """Renders multiple timespan lists into single list for viewing purposes,
    using each Timespan's MusicSpecifier's voice_name as annotation for key sorting.

    Arguments:
        timespan_lists {list} -- List of timespan lists

    Returns:
        New timespan list
    """

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
                new_span = abjad.AnnotatedTimespan(
                    start_offset=timespan.start_offset,
                    stop_offset=timespan.stop_offset,
                    annotation=str(i + 1),
                )
            master_list.extend([new_span])
    master_list.sort()
    return master_list


def add_silent_timespans(timespan_list, specifier=None):
    """Adds silent timespans to timespan list

    Arguments:
        timespan_list {abjad.TimespanList}

    Returns:
        abjad.TimespanList -- New timespan list containing SilentTimespans
    """

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
    """Adds silent timespans to all timespan_lists in timespan_lists

    Returns:
        None
    """

    for timespan_list in timespan_lists:
        timespan_list = add_silent_timespans(timespan_list)
        timespan_list.sort()


def add_silences_to_timespan_dict(timespan_dict, specifier=None):
    """Adds silent timespans to timespans in dictionary

    Returns:
        None
    """

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
    """Makes Timespans from Talea

    Arguments:
        talea {abjadext.rmakers.Talea} -- Talea used to generate timespans

    Keyword Arguments:
        advancement {int} -- Advancement of the talea (default: {0})

    Returns:
        TimespanList
    """

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
            timespan = abjad.AnnotatedTimespan(
                start_offset=start, stop_offset=stop, annotation=None
            )
        timespans.append(timespan)
        total_duration += abs(duration)
    return timespans
