import abjad
import collections
from abjadext import rmakers
import tsmakers



class BoundaryTimespanMaker(tsmakers.TimespanMaker):
    r'''A boundary timespan-maker.

    ::

        >>> timespan_maker = tsmakers.BoundaryTimespanMaker(
        ...     start_talea=rmakers.Talea(
        ...         counts=[1],
        ...         denominator=2,
        ...         ),
        ...     stop_talea=rmakers.Talea(
        ...         counts=[1],
        ...         denominator=4,
        ...         ),
        ...     voice_names=('Violin 1 Voice', 'Violin 2 Voice'),
        ...     )
        >>> print(format(timespan_maker))
        tsmakers.BoundaryTimespanMaker(
            start_talea=rmakers.Talea(
                counts=[1],
                denominator=2,
                ),
            stop_talea=rmakers.Talea(
                counts=[1],
                denominator=4,
                ),
            start_anchor=abjad.abjad.Left,
            stop_anchor=abjad.abjad.Left,
            voice_names=('Violin 1 Voice', 'Violin 2 Voice'),
            )

    ::

        >>> timespan_list = abjad.TimespanList([
        ...     tsmakers.PerformedTimespan(
        ...         start_offset=0,
        ...         stop_offset=1,
        ...         voice_name='Violin 1 Voice',
        ...         ),
        ...     tsmakers.PerformedTimespan(
        ...         start_offset=(1, 2),
        ...         stop_offset=(3, 2),
        ...         voice_name='Violin 2 Voice',
        ...         ),
        ...     tsmakers.PerformedTimespan(
        ...         start_offset=3,
        ...         stop_offset=4,
        ...         voice_name='Violin 2 Voice',
        ...         ),
        ...     ])

    ::

        >>> music_specifiers = {'Cello Voice': None}
        >>> target_timespan = abjad.Timespan(0, 10)
        >>> timespan_list = timespan_maker(
        ...     music_specifiers=music_specifiers,
        ...     target_timespan=target_timespan,
        ...     timespan_list=timespan_list,
        ...     )
        >>> print(format(timespan_list))
        abjad.TimespanList(
            [
                tsmakers.PerformedTimespan(
                    start_offset=abjad.Offset(0, 1),
                    stop_offset=abjad.Offset(1, 2),
                    voice_name='Cello Voice',
                    ),
                tsmakers.PerformedTimespan(
                    start_offset=abjad.Offset(0, 1),
                    stop_offset=abjad.Offset(1, 1),
                    voice_name='Violin 1 Voice',
                    ),
                tsmakers.PerformedTimespan(
                    start_offset=abjad.Offset(1, 2),
                    stop_offset=abjad.Offset(3, 2),
                    voice_name='Violin 2 Voice',
                    ),
                tsmakers.PerformedTimespan(
                    start_offset=abjad.Offset(3, 2),
                    stop_offset=abjad.Offset(7, 4),
                    voice_name='Cello Voice',
                    ),
                tsmakers.PerformedTimespan(
                    start_offset=abjad.Offset(3, 1),
                    stop_offset=abjad.Offset(7, 2),
                    voice_name='Cello Voice',
                    ),
                tsmakers.PerformedTimespan(
                    start_offset=abjad.Offset(3, 1),
                    stop_offset=abjad.Offset(4, 1),
                    voice_name='Violin 2 Voice',
                    ),
                tsmakers.PerformedTimespan(
                    start_offset=abjad.Offset(4, 1),
                    stop_offset=abjad.Offset(17, 4),
                    voice_name='Cello Voice',
                    ),
                ]
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_labels',
        '_start_anchor',
        '_start_talea',
        '_start_groupings',
        '_stop_anchor',
        '_stop_talea',
        '_stop_groupings',
        '_voice_names',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        start_talea=None,
        stop_talea=None,
        start_groupings=None,
        stop_groupings=None,
        start_anchor=abjad.Left,
        stop_anchor=abjad.Left,
        labels=None,
        division_masks=None,
        padding=None,
        seed=None,
        timespan_specifier=None,
        voice_names=None,
        ):
        tsmakers.TimespanMaker.__init__(
            self,
            division_masks=division_masks,
            padding=padding,
            seed=seed,
            timespan_specifier=timespan_specifier,
            )

        if start_talea is not None:
            if not isinstance(start_talea, rmakers.Talea):
                start_duration = abjad.Duration(start_talea)
                counts = [start_duration.numerator]
                denominator = start_duration.denominator
                start_talea = rmakers.Talea(
                    counts=counts,
                    denominator=denominator,
                    )
            assert isinstance(start_talea, rmakers.Talea)
            assert start_talea.counts
            assert all(0 < x for x in start_talea.counts)
        self._start_talea = start_talea

        if start_groupings is not None:
            if not isinstance(start_groupings, collections.Sequence):
                start_groupings = (start_groupings,)
            start_groupings = tuple(int(x) for x in start_groupings)
            assert len(start_groupings)
            assert all(0 < x for x in start_groupings)
        self._start_groupings = start_groupings

        if stop_talea is not None:
            if not isinstance(stop_talea, rmakers.Talea):
                stop_duration = abjad.Duration(stop_talea)
                counts = [stop_duration.numerator]
                denominator = stop_duration.denominator
                stop_talea = rmakers.Talea(
                    counts=counts,
                    denominator=denominator,
                    )
            assert isinstance(stop_talea, rmakers.Talea)
            assert stop_talea.counts
            assert all(0 < x for x in stop_talea.counts)
        self._stop_talea = stop_talea

        if stop_groupings is not None:
            if not isinstance(stop_groupings, collections.Sequence):
                stop_groupings = (stop_groupings,)
            stop_groupings = tuple(int(x) for x in stop_groupings)
            assert len(stop_groupings)
            assert all(0 < x for x in stop_groupings)
        self._stop_groupings = stop_groupings

        if labels is not None:
            if isinstance(labels, str):
                labels = (labels,)
            labels = tuple(str(_) for _ in labels)
        self._labels = labels

        if voice_names is not None:
            voice_names = tuple(voice_names)
        self._voice_names = voice_names

        assert start_anchor in (abjad.Left, abjad.Right)
        self._start_anchor = start_anchor
        assert stop_anchor in (abjad.Left, abjad.Right)
        self._stop_anchor = stop_anchor

    ### PRIVATE METHODS ###

    def _collect_preexisting_timespans(
        self,
        target_timespan=None,
        timespan_list=None,
        ):
        
        preexisting_timespans = abjad.TimespanList()
        for timespan in timespan_list:
            assert isinstance(timespan, (
                tsmakers.PerformedTimespan,
                tsmakers.SilentTimespan,
                ))
            if isinstance(timespan, tsmakers.SilentTimespan):
                continue
            if (
                self.voice_names and
                timespan.voice_name not in self.voice_names
                ):
                continue
            if self.labels:
                if not timespan.music_specifier:
                    continue
                music_specifier_labels = timespan.music_specifier.labels or ()
                for label in self.labels:
                    if label in music_specifier_labels:
                        preexisting_timespans.append(timespan)
                        break
            else:
                preexisting_timespans.append(timespan)
        preexisting_timespans & target_timespan
        return preexisting_timespans

    def _make_timespans(
        self,
        layer=None,
        music_specifiers=None,
        target_timespan=None,
        timespan_list=None,
        ):
        

        new_timespans = abjad.TimespanList()
        if not self.voice_names and not self.labels:
            return new_timespans

        start_talea = self.start_talea
        if start_talea is None:
            start_talea = rmakers.Talea((0,), 1)
        start_talea = tsmakers.Cursor(start_talea)

        start_groupings = self.start_groupings
        if start_groupings is None:
            start_groupings = (1,)
        start_groupings = tsmakers.Cursor(start_groupings)

        stop_talea = self.stop_talea
        if stop_talea is None:
            stop_talea = rmakers.Talea((0,), 1)
        stop_talea = tsmakers.Cursor(stop_talea)

        stop_groupings = self.stop_groupings
        if stop_groupings is None:
            stop_groupings = (1,)
        stop_groupings = tsmakers.Cursor(stop_groupings)

        if self.seed:
            if self.seed < 0:
                for _ in range(abs(self.seed)):
                    start_talea.backtrack()
                    start_groupings.backtrack()
                    stop_talea.backtrack()
                    stop_groupings.backtrack()
            else:
                    next(start_talea)
                    next(start_groupings)
                    next(stop_talea)
                    next(stop_groupings)

        context_counter = collections.Counter()
        preexisting_timespans = self._collect_preexisting_timespans(
            target_timespan=target_timespan,
            timespan_list=timespan_list,
            )
        new_timespan_mapping = {}
        for group_index, group in enumerate(
            preexisting_timespans.partition(True)
            ):
            for context_name, music_specifier in music_specifiers.items():
                if context_name not in new_timespan_mapping:
                    continue
                new_timespan_mapping[context_name] - group.timespan
            for context_name, music_specifier in music_specifiers.items():
                if context_name not in new_timespan_mapping:
                    new_timespan_mapping[context_name] = \
                        abjad.TimespanList()
                context_seed = context_counter[context_name]
                start_durations = []
                for _ in range(next(start_groupings)):
                    start_durations.append(next(start_talea))
                stop_durations = []
                for _ in range(next(stop_groupings)):
                    stop_durations.append(next(stop_talea))
                start_timespans, stop_timespans = (), ()
                if start_durations:
                    group_start = group.start_offset
                    if self.start_anchor is abjad.Right:
                        #print('!!!', float(group_start), float(group_start -
                        #    sum(start_durations)))
                        group_start -= sum(start_durations)
                    start_timespans = music_specifier(
                        durations=start_durations,
                        layer=layer,
                        division_masks=self.division_masks,
                        padding=self.padding,
                        seed=context_seed,
                        start_offset=group_start,
                        timespan_specifier=self.timespan_specifier,
                        voice_name=context_name,
                        )
                    context_counter[context_name] += 1
                if stop_durations:
                    group_stop = group.stop_offset
                    if self.stop_anchor is abjad.Right:
                        group_stop -= sum(stop_durations)
                    stop_timespans = music_specifier(
                        durations=stop_durations,
                        layer=layer,
                        division_masks=self.division_masks,
                        padding=self.padding,
                        seed=context_seed,
                        start_offset=group_stop,
                        timespan_specifier=self.timespan_specifier,
                        voice_name=context_name,
                        )
                    context_counter[context_name] += 1
                #if start_timespans and stop_timespans:
                #    start_timespans & group.timespan
                new_timespan_mapping[context_name].extend(start_timespans)
                new_timespan_mapping[context_name].extend(stop_timespans)
        for context_name, timespans in new_timespan_mapping.items():
            timespans.compute_logical_or()
            new_timespans.extend(timespans)
        return new_timespans

    ### PUBLIC PROPERTIES ###

    @property
    def labels(self):
        return self._labels

    @property
    def start_anchor(self):
        return self._start_anchor

    @property
    def start_talea(self):
        return self._start_talea

    @property
    def stop_anchor(self):
        return self._stop_anchor

    @property
    def stop_talea(self):
        return self._stop_talea

    @property
    def start_groupings(self):
        return self._start_groupings

    @property
    def stop_groupings(self):
        return self._stop_groupings

    @property
    def voice_names(self):
        return self._voice_names
