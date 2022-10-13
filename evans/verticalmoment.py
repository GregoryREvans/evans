import abjad


class VerticalMoment:

    ### CLASS VARIABLES ###

    __slots__ = ("_components", "_governors", "_offset")

    ### INITIALIZER ###

    def __init__(self, components=None, offset=None):
        self._components = components
        self._offset = offset

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a vertical moment with the same
        components as this vertical moment.

        Returns true or false.
        """
        if isinstance(argument, VerticalMoment):
            if len(self) == len(argument):
                for c, d in zip(self.components, argument.components):
                    if c is not d:
                        return False
                else:
                    return True
        return False

    def __hash__(self):
        """
        Hases vertical moment.

        ..  container:: example

            Vertical moments can be hashed:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> vms = []
            >>> vms.extend(abjad.iterate_vertical_moments(staff))
            >>> vms.extend(abjad.iterate_vertical_moments(staff))

            >>> assert len(vms) == 8
            >>> assert len(set(vms)) == 4

        Redefined in tandem with __eq__.
        """
        if self.components:
            return hash(tuple([id(_) for _ in self.components]))
        return 0

    def __len__(self):
        r"""
        Length of vertical moment.

        ..  container:: example

            >>> score = abjad.Score(
            ... r'''
            ...    \new Staff {
            ...        \times 4/3 {
            ...            d''8
            ...            c''8
            ...            b'8
            ...        }
            ...    }
            ...    \new PianoStaff <<
            ...        \new Staff {
            ...            a'4
            ...            g'4
            ...        }
            ...        \new Staff {
            ...            \clef "bass"
            ...            f'8
            ...            e'8
            ...            d'8
            ...            c'8
            ...        }
            ...    >>
            ...    '''
            ...    )

            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3
                        {
                            d''8
                            c''8
                            b'8
                        }
                    }
                    \new PianoStaff
                    <<
                        \new Staff
                        {
                            a'4
                            g'4
                        }
                        \new Staff
                        {
                            \clef "bass"
                            f'8
                            e'8
                            d'8
                            c'8
                        }
                    >>
                >>

            >>> for moment in abjad.iterate_vertical_moments(score):
            ...     print(moment, len(moment))
            ...
            VerticalMoment(0, <<3>>) 9
            VerticalMoment(1/8, <<3>>) 9
            VerticalMoment(1/6, <<3>>) 9
            VerticalMoment(1/4, <<3>>) 9
            VerticalMoment(1/3, <<3>>) 9
            VerticalMoment(3/8, <<3>>) 9

        Defined equal to the number of components in vertical moment.

        Returns nonnegative integer.
        """
        return len(self.components)

    def __repr__(self):
        """
        Gets interpreter representation of vertical moment.

        Returns string.
        """
        if not self.components:
            return f"{type(self).__name__}()"
        length = len(self.components)
        result = f"{type(self).__name__}({str(self.offset)}, <<{length}>>)"
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def components(self):
        """
        Tuple of zero or more components happening at vertical moment.

        It is always the case that ``self.components =
        self.overlap_components + self.start_components``.
        """
        return self._components

    @property
    def governors(self):
        """
        Tuple of one or more containers in which vertical moment is evaluated.
        """
        return self._governors

    @property
    def ties(self) -> list[abjad.LogicalTie]:
        result = []
        for component in self.components:
            if isinstance(component, abjad.LogicalTie):
                result.append(component)
        return result

    @property
    def offset(self):
        """
        Rational-valued score offset at which vertical moment is evaluated.
        """
        return self._offset

    @property
    def overlap_ties(self):
        """
        Tuple of components in vertical moment starting before vertical
        moment, ordered by score index.
        """
        result = []
        for component in self.components:
            if abjad.get.timespan(component).start_offset < self.offset:
                result.append(component)
        result = tuple(result)
        return result

    @property
    def start_ties(self):
        """
        Tuple of components in vertical moment starting with at vertical
        moment, ordered by score index.
        """
        result = []
        for component in self.components:
            if abjad.get.timespan(component).start_offset == self.offset:
                result.append(component)
        result = tuple(result)
        return result




def iterate_vertical_moments_by_logical_tie(components, reverse=None):
    moments = []
    components = abjad.select.logical_ties(components)
    components.sort(key=lambda _: abjad.get.timespan(_).start_offset)
    offset_to_components = dict()
    for component in components:
        start_offset = abjad.get.timespan(component).start_offset
        if start_offset not in offset_to_components:
            offset_to_components[start_offset] = []
    # TODO: optimize with bisect
    for component in components:
        inserted = False
        timespan = abjad.get.timespan(component)
        for offset, list_ in offset_to_components.items():
            if (
                timespan.start_offset <= offset < timespan.stop_offset
                and component not in list_
            ):
                list_.append(component)
                inserted = True
            elif inserted is True:
                break
    moments = []
    for offset, list_ in offset_to_components.items():
        list_.sort(key=lambda _: abjad.parentage.Parentage(_[0]).score_index())
        moment = VerticalMoment(components=list_, offset=offset)
        moments.append(moment)
    if reverse is True:
        moments.reverse()
    return tuple(moments)
