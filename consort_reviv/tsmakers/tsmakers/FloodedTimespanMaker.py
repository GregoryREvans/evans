import abjad
import tsmakers


class FloodedTimespanMaker(tsmakers.TimespanMaker):
    r'''A flooded timespan maker.

    ::

        >>> timespan_maker = tsmakers.FloodedTimespanMaker()
        >>> print(format(timespan_maker))
        tsmakers.FloodedTimespanMaker()

    ::

        >>> music_specifiers = {
        ...     'Violin Voice': 'violin music',
        ...     'Cello Voice': 'cello music',
        ...     }
        >>> target_timespan = abjad.Timespan((1, 2), (2, 1))
        >>> timespan_list = timespan_maker(
        ...     music_specifiers=music_specifiers,
        ...     target_timespan=target_timespan,
        ...     )
        >>> print(format(timespan_list))
        abjad.TimespanList(
            [
                tsmakers.PerformedTimespan(
                    start_offset=abjad.Offset(1, 2),
                    stop_offset=abjad.Offset(2, 1),
                    music_specifier='cello music',
                    voice_name='Cello Voice',
                    ),
                tsmakers.PerformedTimespan(
                    start_offset=abjad.Offset(1, 2),
                    stop_offset=abjad.Offset(2, 1),
                    music_specifier='violin music',
                    voice_name='Violin Voice',
                    ),
                ]
            )

    ::

        >>> music_specifier = tsmakers.CompositeMusicSpecifier(
        ...     primary_music_specifier='one',
        ...     primary_voice_name='Viola 1 RH',
        ...     rotation_indices=(0, 1, -1),
        ...     secondary_voice_name='Viola 1 LH',
        ...     secondary_music_specifier=tsmakers.MusicSpecifierSequence(
        ...         application_rate='phrase',
        ...         music_specifiers=['two', 'three', 'four'],
        ...         ),
        ...     )
        >>> music_specifiers = {
        ...     'Viola 1 Performer Group': music_specifier,
        ...     }
        >>> timespan_list = timespan_maker(
        ...     music_specifiers=music_specifiers,
        ...     target_timespan=target_timespan,
        ...     )
        >>> print(format(timespan_list))
        abjad.TimespanList(
            [
                tsmakers.PerformedTimespan(
                    start_offset=abjad.Offset(1, 2),
                    stop_offset=abjad.Offset(2, 1),
                    music_specifier='two',
                    voice_name='Viola 1 LH',
                    ),
                tsmakers.PerformedTimespan(
                    start_offset=abjad.Offset(1, 2),
                    stop_offset=abjad.Offset(2, 1),
                    music_specifier='one',
                    voice_name='Viola 1 RH',
                    ),
                ]
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        division_masks=None,
        padding=None,
        seed=None,
        timespan_specifier=None,
        ):
        tsmakers.TimespanMaker.__init__(
            self,
            division_masks=division_masks,
            padding=padding,
            seed=seed,
            timespan_specifier=timespan_specifier,
            )

    ### PRIVATE METHODS ###

    def _make_timespans(
        self,
        layer=None,
        music_specifiers=None,
        target_timespan=None,
        timespan_list=None,
        ):
        start_offset = target_timespan.start_offset
        durations = [target_timespan.duration]
        new_timespans = abjad.TimespanList()
        for context_name, music_specifier in music_specifiers.items():
            timespans = music_specifier(
                durations=durations,
                layer=layer,
                division_masks=self.division_masks,
                padding=self.padding,
                seed=self.seed,
                start_offset=start_offset,
                timespan_specifier=self.timespan_specifier,
                voice_name=context_name,
                )
            new_timespans.extend(timespans)
        return new_timespans
