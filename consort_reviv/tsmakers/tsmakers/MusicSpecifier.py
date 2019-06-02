import abjad
import collections
import os
import tsmakers
from abjadext import rmakers 


class MusicSpecifier(tsmakers.HashCachingObject):
    r'''A music specifier.

    ::

        >>> music_specifier = tsmakers.MusicSpecifier()
        >>> print(format(music_specifier))
        tsmakers.MusicSpecifier()

    ..  container:: example

        MusicSpecifier can accept CompositeRhythmMakers in their `rhythm_maker`
        slot:

        ::

            >>> music_specifier = tsmakers.MusicSpecifier(
            ...     rhythm_maker=tsmakers.CompositeRhythmMaker(),
            ...     )

    '''

    ### CLASS VARIABLES ###

    __is_terminal_ajv_list_item__ = True

    __slots__ = (
        '_attachment_handler',
        '_color',
        '_comment',
        '_grace_handler',
        '_instrument',
        '_labels',
        '_minimum_phrase_duration',
        '_pitch_handler',
        '_register_handler',
        '_rhythm_maker',
        '_seed',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        attachment_handler=None,
        color=None,
        comment=None,
        grace_handler=None,
        instrument=None,
        labels=None,
        minimum_phrase_duration=None,
        pitch_handler=None,
        register_handler=None,
        rhythm_maker=None,
        seed=None,
        ):
        import tsmakers
        HashCachingObject.__init__(self)
        if attachment_handler is not None:
            assert isinstance(attachment_handler, tsmakers.AttachmentHandler)
        self._attachment_handler = attachment_handler
        self._color = color
        if grace_handler is not None:
            assert isinstance(grace_handler, tsmakers.GraceHandler)
        self._grace_handler = grace_handler
        if instrument is not None:
            assert isinstance(instrument, abjad.Instrument)
        self._instrument = instrument
        if labels is not None:
            if isinstance(labels, str):
                labels = (labels,)
            labels = tuple(str(_) for _ in labels)
        self._labels = labels
        if minimum_phrase_duration is not None:
            minimum_phrase_duration = \
                abjad.Duration(minimum_phrase_duration)
            assert 0 <= minimum_phrase_duration
        self._minimum_phrase_duration = minimum_phrase_duration
        if pitch_handler is not None:
            assert isinstance(pitch_handler, tsmakers.PitchHandler)
        self._pitch_handler = pitch_handler
        if register_handler is not None:
            assert isinstance(register_handler, tsmakers.RegisterHandler)
        self._register_handler = register_handler
        if rhythm_maker is not None:
            prototype = (
                rmakers.RhythmMaker,
                tsmakers.CompositeRhythmMaker,
                )
            assert isinstance(rhythm_maker, prototype)
        self._rhythm_maker = rhythm_maker
        if seed is not None:
            seed = int(seed)
        self._seed = seed
        if comment is not None:
            comment = str(comment)
        self._comment = comment

    ### PUBLIC METHODS ###

    def rotate(self, rotation):
        seed = self.seed or 0
        seed = seed + rotation
        return abjad.new(self, seed=seed)

    def transpose(self, expr):
        r'''Transposes music specifier.

        ::

            >>> music_specifier = tsmakers.MusicSpecifier(
            ...     pitch_handler=tsmakers.AbsolutePitchHandler(
            ...         pitch_specifier = tsmakers.PitchSpecifier(
            ...             pitch_segments=(
            ...                 "c' e' g'",
            ...                 "fs' gs'",
            ...                 "b",
            ...                 ),
            ...             ratio=(1, 2, 3),
            ...             ),
            ...         ),
            ...     )
            >>> transposed_music_specifier = music_specifier.transpose('-M2')
            >>> print(format(transposed_music_specifier))
            tsmakers.MusicSpecifier(
                pitch_handler=tsmakers.AbsolutePitchHandler(
                    pitch_specifier=tsmakers.PitchSpecifier(
                        pitch_segments=(
                            abjad.PitchSegment(
                                (
                                    abjad.NamedPitch('bf'),
                                    abjad.NamedPitch("d'"),
                                    abjad.NamedPitch("f'"),
                                    ),
                                item_class=abjad.NamedPitch,
                                ),
                            abjad.PitchSegment(
                                (
                                    abjad.NamedPitch("e'"),
                                    abjad.NamedPitch("fs'"),
                                    ),
                                item_class=abjad.NamedPitch,
                                ),
                            abjad.PitchSegment(
                                (
                                    abjad.NamedPitch('a'),
                                    ),
                                item_class=abjad.NamedPitch,
                                ),
                            ),
                        ratio=abjad.Ratio((1, 2, 3)),
                        ),
                    ),
                )

        Returns new music specifier.
        '''
        if isinstance(expr, str):
            try:
                pitch = abjad.NamedPitch(expr)
                expr = abjad.NamedPitch('C4') - pitch
            except:
                expr = abjad.NamedInterval(expr)
        pitch_handler = self.pitch_handler
        if pitch_handler is not None:
            pitch_handler = pitch_handler.transpose(expr)
        return abjad.new(
            self,
            pitch_handler=pitch_handler,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def attachment_handler(self):
        return self._attachment_handler

    @property
    def color(self):
        return self._color

    @property
    def comment(self):
        return self._comment

    @property
    def grace_handler(self):
        return self._grace_handler

    @property
    def instrument(self):
        return self._instrument

    @property
    def labels(self):
        return self._labels

    @property
    def minimum_phrase_duration(self):
        return self._minimum_phrase_duration

    @property
    def pitch_handler(self):
        return self._pitch_handler

    @property
    def register_handler(self):
        return self._register_handler

    @property
    def rhythm_maker(self):
        return self._rhythm_maker

    @property
    def seed(self):
        return self._seed
