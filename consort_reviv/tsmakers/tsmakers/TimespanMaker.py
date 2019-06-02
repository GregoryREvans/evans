import abc
import abjad
import collections
import tsmakers


class TimespanMaker():
    r'''Abstract base class for timespan makers.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_output_masks',
        '_padding',
        '_seed',
        '_timespan_specifier',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        division_masks=None,
        padding=None,
        seed=None,
        timespan_specifier=None,
        ):
        if division_masks is not None:
            if isinstance(division_masks, abjad.Pattern):
                division_masks = (division_masks,)
            division_masks = abjad.PatternList(
                items=division_masks,
                )
        self._output_masks = division_masks
        if padding is not None:
            padding = abjad.Duration(padding)
        self._padding = padding
        if seed is not None:
            seed = int(seed)
        self._seed = seed
        if timespan_specifier is not None:
            assert isinstance(timespan_specifier, tsmakers.TimespanSpecifier)
        self._timespan_specifier = timespan_specifier

    ### SPECIAL METHODS ###

    def __call__(
        self,
        layer=None,
        music_specifiers=None,
        rotation=None,
        silenced_context_names=None,
        target_timespan=None,
        timespan_list=None,
        ):
        if not isinstance(timespan_list, abjad.TimespanList):
            timespan_list = abjad.TimespanList(
                timespan_list,
                )
        if target_timespan is None:
            if timespan_list:
                target_timespan = timespan_list.timespan
            else:
                raise TypeError
        assert isinstance(timespan_list, abjad.TimespanList)
        if not music_specifiers:
            return timespan_list
        music_specifiers = self._coerce_music_specifiers(music_specifiers)
        new_timespans = self._make_timespans(
            layer=layer,
            music_specifiers=music_specifiers,
            target_timespan=target_timespan,
            timespan_list=timespan_list,
            )
        self._cleanup_silent_timespans(
            layer=layer,
            silenced_context_names=silenced_context_names,
            timespans=new_timespans,
            )
        timespan_list.extend(new_timespans)
        timespan_list.sort()
        return timespan_list

    def __illustrate__(self, scale=None, target_timespan=None, **kwargs):
        target_timespan = target_timespan or abjad.Timespan(0, 16)
        assert isinstance(target_timespan, abjad.Timespan)
        assert 0 < target_timespan.duration
        scale = scale or 1.5
        music_specifiers = abjad.OrderedDict([
            ('A', 'A music'),
            ('B', 'B music'),
            ('C', 'C music'),
            ('D', 'D music'),
            ('E', 'E music'),
            ('F', 'F music'),
            ('G', 'G music'),
            ('H', 'H music'),
            ('I', 'I music'),
            ('J', 'J music'),
            ])
        timespan_list = self(
            layer=0,
            music_specifiers=music_specifiers,
            target_timespan=target_timespan,
            )
        ti_lilypond_file = timespan_list.__illustrate__(
            key='voice_name',
            range_=target_timespan,
            scale=scale,
            )
        ti_markup = ti_lilypond_file.items[-1]
        offset_counter = abjad.OffsetCounter(timespan_list)
        oc_lilypond_file = offset_counter.__illustrate__(
            range_=target_timespan,
            scale=scale,
            )
        oc_markup = oc_lilypond_file.items[-1]
        lilypond_file = abjad.LilyPondFile.new(
            default_paper_size=['tabloid', 'landscape'],
            date_time_token=False,
            )
        lilypond_file.items.extend([
            abjad.String.normalize('''
            % Backport for pre 2.19.20 versions of LilyPond
            #(define-markup-command (overlay layout props args)
                (markup-list?)
                (apply ly:stencil-add (interpret-markup-list layout props args)))
            '''),
            ti_markup,
            abjad.Markup.null().pad_around(2),
            oc_markup,
            ])
        lilypond_file.header_block.tagline = False
        return lilypond_file
    
    def __format__(self, format_specification=''):
        return abjad.StorageFormatManager(self).get_storage_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _coerce_music_specifiers(music_specifiers):
        # from MusicSpecifier import MusicSpecifier
        # from MusicSpecifierSequence import MusicSpecifierSequence
        result = collections.OrderedDict()
        prototype = (
            tsmakers.MusicSpecifierSequence,
            tsmakers.CompositeMusicSpecifier,
            )
        for context_name, music_specifier in music_specifiers.items():
            if music_specifier is None:
                music_specifier = [None]
            if not isinstance(music_specifier, prototype):
                music_specifier = tsmakers.MusicSpecifierSequence(
                    music_specifiers=music_specifier,
                    )
            result[context_name] = music_specifier
        return result

    def _cleanup_silent_timespans(
        self,
        layer,
        silenced_context_names,
        timespans,
        ):
        if not silenced_context_names or not timespans:
            return

        silent_timespans_by_context = {}
        for context_name in silenced_context_names:
            if context_name not in silent_timespans_by_context:
                silent_timespans_by_context[context_name] = \
                    abjad.TimespanList()

        sounding_timespans_by_context = {}
        sounding_timespans = abjad.TimespanList()

        for timespan in timespans:
            voice_name = timespan.voice_name
            if isinstance(timespan, PerformedTimespan):
                if voice_name not in sounding_timespans_by_context:
                    sounding_timespans_by_context[voice_name] = \
                        abjad.TimespanList()
                sounding_timespans_by_context[voice_name].append(timespan)
                sounding_timespans.append(timespan)
            else:
                if voice_name not in silent_timespans_by_context:
                    silent_timespans_by_context[voice_name] = \
                        abjad.TimespanList()
                silent_timespans_by_context[voice_name].append(timespan)

        sounding_timespans.sort()
        sounding_timespans.compute_logical_or()

        # Create silences.
        for shard in sounding_timespans.partition(True):
            for context_name in silenced_context_names:
                timespan = SilentTimespan(
                    layer=layer,
                    voice_name=context_name,
                    start_offset=shard.start_offset,
                    stop_offset=shard.stop_offset,
                    )
                silent_timespans_by_context[context_name].append(timespan)

        # Remove any overlap between performed and silent timespans.
        # Then add the silent timespans into the original timespan inventory.
        for context_name, silent_timespans in \
            sorted(silent_timespans_by_context.items()):
            silent_timespans.sort()
            if context_name in sounding_timespans_by_context:
                for timespan in sounding_timespans_by_context[context_name]:
                    silent_timespans - timespan
            timespans.extend(silent_timespans)

    ### PUBLIC METHODS ###

    def rotate(self, rotation):
        seed = self.seed or 0
        seed = seed + rotation
        return abjad.new(self, seed=seed)

    ### PUBLIC PROPERTIES ###

    @property
    def is_dependent(self):
        return False

    @property
    def division_masks(self):
        return self._output_masks

    @property
    def padding(self):
        return self._padding

    @property
    def seed(self):
        return self._seed

    @property
    def timespan_specifier(self):
        return self._timespan_specifier
