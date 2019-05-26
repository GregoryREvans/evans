import abjad
from evans.consort_reviv.AbjadValueObject import AbjadValueObject
from abjad import mathtools
import abjadext.rmakers


class CompositeRhythmMaker(AbjadValueObject):
    r'''A composite rhythm-maker.

    ::

        >>> composite_rhythm_maker = consort.CompositeRhythmMaker(
        ...     default=abjadext.rmakers.EvenDivisionRhythmMaker(),
        ...     first=abjadext.rmakers.NoteRhythmMaker(),
        ...     last=abjadext.rmakers.IncisedRhythmMaker(
        ...         incise_specifier=abjadext.rmakers.InciseSpecifier(
        ...             prefix_counts=[0],
        ...             suffix_talea=[1],
        ...             suffix_counts=[1],
        ...             talea_denominator=16,
        ...             ),
        ...         ),
        ...     only=abjadext.rmakers.EvenDivisionRhythmMaker(
        ...         denominators=[32],
        ...         ),
        ...     )
        >>> print(format(composite_rhythm_maker))
        consort.tools.CompositeRhythmMaker(
            default=abjadext.rmakers.EvenDivisionRhythmMaker(
                denominators=[8],
                preferred_denominator='from_counts',
                ),
            first=abjadext.rmakers.NoteRhythmMaker(),
            last=abjadext.rmakers.IncisedRhythmMaker(
                incise_specifier=abjadext.rmakers.InciseSpecifier(
                    prefix_counts=[0],
                    suffix_talea=[1],
                    suffix_counts=[1],
                    talea_denominator=16,
                    ),
                ),
            only=abjadext.rmakers.EvenDivisionRhythmMaker(
                denominators=[32],
                preferred_denominator='from_counts',
                ),
            )

    ..  container:: example

        ::

            >>> divisions = [(1, 4), (1, 4), (1, 4), (1, 4)]
            >>> result = composite_rhythm_maker(divisions)
            >>> staff = abjad.Staff()
            >>> for x in result:
            ...     staff.extend(x)
            ...
            >>> print(format(staff))
            \new Staff {
                c'4
                {
                    c'8 [
                    c'8 ]
                }
                {
                    c'8 [
                    c'8 ]
                }
                c'8. [
                c'16 ]
            }

    ..  container:: example

        ::

            >>> divisions = [(1, 4), (1, 4)]
            >>> result = composite_rhythm_maker(divisions)
            >>> staff = abjad.Staff()
            >>> for x in result:
            ...     staff.extend(x)
            ...
            >>> print(format(staff))
            \new Staff {
                c'4
                c'8. [
                c'16 ]
            }

    ..  container:: example

        ::

            >>> divisions = [(1, 4)]
            >>> result = composite_rhythm_maker(divisions)
            >>> staff = abjad.Staff()
            >>> for x in result:
            ...     staff.extend(x)
            ...
            >>> print(format(staff))
            \new Staff {
                {
                    c'32 [
                    c'32
                    c'32
                    c'32
                    c'32
                    c'32
                    c'32
                    c'32 ]
                }
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default',
        '_first',
        '_last',
        '_only',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        default=None,
        first=None,
        last=None,
        only=None,
        ):
        if first is not None:
            assert isinstance(first, abjadext.rmakers.RhythmMaker)
        if last is not None:
            assert isinstance(last, abjadext.rmakers.RhythmMaker)
        if only is not None:
            assert isinstance(only, abjadext.rmakers.RhythmMaker)
        if default is None:
            default = abjadext.rmakers.NoteRhythmMaker()
        assert isinstance(default, abjadext.rmakers.RhythmMaker)
        self._first = first
        self._last = last
        self._only = only
        self._default = default

    ### SPECIAL METHODS ###

    def __call__(self, divisions, rotation=None):
        divisions = [mathtools.NonreducedFraction(x) for x in divisions]
        result = []
        if not divisions:
            pass
        elif len(divisions) == 1:
            if self.only:
                result.extend(self.only(divisions, rotation=rotation))
            elif self.last:
                result.extend(self.last(divisions, rotation=rotation))
            elif self.first:
                result.extend(self.first(divisions, rotation=rotation))
            else:
                result.extend(self.default(divisions, rotation=rotation))
        elif len(divisions) == 2:
            if self.first and self.last:
                first = self.first(divisions=[divisions[0]], rotation=rotation)
                last = self.last(divisions=[divisions[1]], rotation=rotation)
                result.extend(first)
                result.extend(last)
            elif self.first:
                first = self.first(divisions=[divisions[0]], rotation=rotation)
                default = self.default(divisions=[divisions[1]], rotation=rotation)
                result.extend(first)
                result.extend(default)
            elif self.last:
                default = self.default(divisions=[divisions[0]], rotation=rotation)
                last = self.last(divisions=[divisions[1]], rotation=rotation)
                result.extend(default)
                result.extend(last)
            else:
                default = self.default(divisions=divisions, rotation=rotation)
                result.extend(default)
        else:
            if self.first and self.last:
                first = self.first(divisions=[divisions[0]], rotation=rotation)
                default = self.default(divisions=divisions[1:-1], rotation=rotation)
                last = self.last(divisions=[divisions[-1]], rotation=rotation)
                result.extend(first)
                result.extend(default)
                result.extend(last)
            elif self.first:
                first = self.first(divisions=[divisions[0]], rotation=rotation)
                default = self.default(divisions=divisions[1:], rotation=rotation)
                result.extend(first)
                result.extend(default)
            elif self.last:
                default = self.default(divisions=divisions[:-1], rotation=rotation)
                last = self.last(divisions=[divisions[-1]], rotation=rotation)
                result.extend(default)
                result.extend(last)
            else:
                default = self.default(divisions=divisions, rotation=rotation)
                result.extend(default)
        return result

    def __illustrate__(self, divisions=None):
        r'''Illustrates composite rhythm-maker.

        Returns LilyPond file.
        '''
        divisions = divisions or [
            (3, 8),
            (4, 8),
            (3, 16),
            (4, 16),
            (5, 8),
            (2, 4),
            (5, 16),
            (2, 8),
            (7, 8),
            ]
        selections = self(divisions)
        lilypond_file = abjad.LilyPondFile.rhythm(
            selections,
            divisions,
            )
        return lilypond_file

    ### PUBLIC METHODS ###

    def new(
        self,
        first=None,
        last=None,
        only=None,
        default=None,
        **kwargs
        ):
        first = first or self.first
        last = last or self.last
        only = only or self.only
        default = default or self.default
        if first is not None:
            first = abjad.new(first, **kwargs)
        if last is not None:
            last = abjad.new(last, **kwargs)
        if only is not None:
            only = abjad.new(only, **kwargs)
        if default is not None:
            default = abjad.new(default, **kwargs)
        result = abjad.new(
            self,
            first=first,
            last=last,
            only=only,
            default=default,
            )
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def first(self):
        return self._first

    @property
    def last(self):
        return self._last

    @property
    def only(self):
        return self._only

    @property
    def default(self):
        return self._default
