Sequence Recipes
================

First Example
-------------


::

    >>> import abjad
    >>> import evans
    >>> from abjadext import microtones
    >>> ratio = evans.Ratio("13:11:10:9:5")
    >>> ratio
    Ratio((13, 11, 10, 9, 5))

::

    >>> ratios = ratio.extract_sub_ratios(as_fractions=True)
    >>> ratios
    Sequence([Fraction(1, 1), Fraction(9, 5), Fraction(2, 1), Fraction(11, 5), Fraction(13, 5)])

::

    >>> combination_multiples = evans.Sequence(ratios).combination_multiplication(2)
    >>> ratios = microtones.RatioClassSet(combination_multiples).sorted()
    >>> ratios
    RatioClassSet([Fraction(1, 1), Fraction(11, 10), Fraction(117, 100), Fraction(13, 10), Fraction(143, 100), Fraction(9, 5), Fraction(99, 50)])

::

    >>> ratios = evans.Sequence(ratios)
    >>> final_seq = ratios.random_walk(length=25, step_list=[1, 2, 1], random_seed=1)
    >>> final_seq
    Sequence([Fraction(1, 1), Fraction(99, 50), Fraction(1, 1), Fraction(117, 100), Fraction(11, 10), Fraction(1, 1), Fraction(9, 5), Fraction(99, 50), Fraction(1, 1), Fraction(9, 5), Fraction(143, 100), Fraction(9, 5), Fraction(13, 10), Fraction(143, 100), Fraction(13, 10), Fraction(11, 10), Fraction(117, 100), Fraction(11, 10), Fraction(13, 10), Fraction(143, 100), Fraction(13, 10), Fraction(11, 10), Fraction(117, 100), Fraction(13, 10), Fraction(11, 10), Fraction(1, 1)])

::

    >>> handler = evans.PitchHandler(final_seq, as_ratios=True, forget=False)
    >>> staff = abjad.Staff([abjad.Note("a4") for _ in final_seq])
    >>> handler(staff)

::

    >>> score = abjad.Score([staff])
    >>> abjad.override(score).BarLine.stencil = False
    >>> abjad.override(score).Beam.stencil = False
    >>> abjad.override(score).Flag.stencil = False
    >>> abjad.override(score).Rest.stencil = False
    >>> abjad.override(score).SpacingSpanner.strict_note_spacing = True
    >>> abjad.override(score).SpanBar.stencil = False
    >>> abjad.override(score).Stem.stencil = False
    >>> abjad.override(score).TimeSignature.stencil = False
    >>> abjad.setting(score).proportional_notation_duration = abjad.SchemeMoment(
    ...     (1, 20)
    ... )
    ...

::

    >>> file = abjad.LilyPondFile(
    ...     items=[score, abjad.Block(name="paper"), abjad.Block(name="layout")],
    ...     includes=[
    ...         "abjad.ily",
    ...         "ekmelos-ji-accidental-markups.ily",
    ...     ],
    ...     global_staff_size=16,
    ... )
    ...
    >>> file.paper_block.items.append("indent = 0")
    >>> file.layout_block.items.append(r'\accidentalStyle "dodecaphonic"')
    >>> abjad.show(file)


Second Example
--------------


::

    >>> import abjad
    >>> import evans
    >>> from abjadext import microtones

::

    >>> source = microtones.PitchClassSet([0, 1, 2, 4, 7, 8])
    >>> inverted_source = source.invert().transpose(6)
    >>> inverted_source
    PitchClassSet([Fraction(6, 1), Fraction(5, 1), Fraction(4, 1), Fraction(2, 1), Fraction(11, 1), Fraction(10, 1)])

::

    >>> derived_sequence = evans.Sequence(source).derive_added_sequences(inverted_source, flat=True)
    >>> derived_sequence
    Sequence([Fraction(6, 1), Fraction(7, 1), Fraction(8, 1), Fraction(10, 1), Fraction(13, 1), Fraction(14, 1), Fraction(5, 1), Fraction(6, 1), Fraction(7, 1), Fraction(9, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)])

::

    >>> jos = derived_sequence.josephus(2)
    >>> jos
    Sequence([[Fraction(6, 1), Fraction(7, 1), Fraction(8, 1), Fraction(10, 1), Fraction(13, 1), Fraction(14, 1), Fraction(5, 1), Fraction(6, 1), Fraction(7, 1), Fraction(9, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(10, 1), Fraction(13, 1), Fraction(14, 1), Fraction(5, 1), Fraction(6, 1), Fraction(7, 1), Fraction(9, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(14, 1), Fraction(5, 1), Fraction(6, 1), Fraction(7, 1), Fraction(9, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(6, 1), Fraction(7, 1), Fraction(9, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(9, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1), Fraction(18, 1)], [Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1)], [Fraction(6, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1)], [Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1)], [Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1)], [Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1)], [Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1)], [Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1)], [Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1)], [Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(18, 1), Fraction(12, 1), Fraction(17, 1)], [Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(18, 1), Fraction(12, 1)], [Fraction(6, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(18, 1), Fraction(12, 1)], [Fraction(6, 1), Fraction(7, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(18, 1), Fraction(12, 1)], [Fraction(6, 1), Fraction(7, 1), Fraction(11, 1), Fraction(11, 1), Fraction(18, 1), Fraction(12, 1)], [Fraction(6, 1), Fraction(7, 1), Fraction(11, 1), Fraction(11, 1), Fraction(12, 1)], [Fraction(7, 1), Fraction(11, 1), Fraction(11, 1), Fraction(12, 1)], [Fraction(7, 1), Fraction(11, 1), Fraction(12, 1)], [Fraction(7, 1), Fraction(11, 1)], [Fraction(7, 1)]])

::

    >>> jos = jos.flatten()
    >>> jos
    Sequence([Fraction(6, 1), Fraction(7, 1), Fraction(8, 1), Fraction(10, 1), Fraction(13, 1), Fraction(14, 1), Fraction(5, 1), Fraction(6, 1), Fraction(7, 1), Fraction(9, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(10, 1), Fraction(13, 1), Fraction(14, 1), Fraction(5, 1), Fraction(6, 1), Fraction(7, 1), Fraction(9, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(14, 1), Fraction(5, 1), Fraction(6, 1), Fraction(7, 1), Fraction(9, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(6, 1), Fraction(7, 1), Fraction(9, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(9, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(13, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(8, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(12, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(6, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(12, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(15, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(19, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(11, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(14, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1), Fraction(18, 1), Fraction(6, 1), Fraction(8, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1), Fraction(6, 1), Fraction(13, 1), Fraction(5, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1), Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(12, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1), Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(6, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1), Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(2, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1), Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(9, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1), Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(13, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1), Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(18, 1), Fraction(10, 1), Fraction(12, 1), Fraction(17, 1), Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(18, 1), Fraction(12, 1), Fraction(17, 1), Fraction(6, 1), Fraction(13, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(18, 1), Fraction(12, 1), Fraction(6, 1), Fraction(7, 1), Fraction(4, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(18, 1), Fraction(12, 1), Fraction(6, 1), Fraction(7, 1), Fraction(11, 1), Fraction(4, 1), Fraction(11, 1), Fraction(18, 1), Fraction(12, 1), Fraction(6, 1), Fraction(7, 1), Fraction(11, 1), Fraction(11, 1), Fraction(18, 1), Fraction(12, 1), Fraction(6, 1), Fraction(7, 1), Fraction(11, 1), Fraction(11, 1), Fraction(12, 1), Fraction(7, 1), Fraction(11, 1), Fraction(11, 1), Fraction(12, 1), Fraction(7, 1), Fraction(11, 1), Fraction(12, 1), Fraction(7, 1), Fraction(11, 1), Fraction(7, 1)])

::

    >>> lorenz = evans.Sequence.lorenz(
    ...     rho=28.0,
    ...     sigma=10.0,
    ...     beta=(8.0 / 3.0),
    ...     first_state=[1.0, 1.0, 1.0],
    ...     time_values=[0.0, 40.0, 0.01],
    ...     iters=10,
    ... ).flatten()
    ...
    >>> lorenz
    Sequence([1.0, 1.0125657408032651, 1.0488214579592021, 1.107206299034454, 1.1868654842333801, 1.2875548011090359, 1.4095688012763303, 1.5536887870511105, 1.721145788631946, 1.9135963877769706, 1.0, 1.2599200056984277, 1.5240008388892068, 1.798314577764884, 2.0885455352781572, 2.400160398825767, 2.738552104480127, 3.109160997057688, 3.51757713188136, 3.969623487737072, 1.0, 0.9848910446848755, 0.973114341630953, 0.9651591023109144, 0.9617373815250438, 0.9638062240116604, 0.9726082787069016, 0.9897311952182216, 1.0171865646618774, 1.057511871629279])

::

    >>> lorenz = lorenz.multiply(13)
    >>> lorenz = lorenz.normalize_to_indices()
    >>> lorenz
    Sequence([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

::

    >>> seq_len = len(jos)
    >>> map = lorenz.mod(seq_len, indices=True)
    >>> map
    Sequence([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])


::

    >>> final_seq = evans.Sequence(jos).map_indices(map)
    >>> final_seq
    Sequence([Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(8, 1), Fraction(8, 1), Fraction(8, 1), Fraction(10, 1), Fraction(10, 1), Fraction(13, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1), Fraction(7, 1)])

::

    >>> handler = evans.PitchHandler(final_seq, forget=False)
    >>> staff = abjad.Staff([abjad.Note() for _ in final_seq])
    >>> handler(staff)

::

    >>> score = abjad.Score([staff])
    >>> abjad.override(score).BarLine.stencil = False
    >>> abjad.override(score).Beam.stencil = False
    >>> abjad.override(score).Flag.stencil = False
    >>> abjad.override(score).Rest.stencil = False
    >>> abjad.override(score).SpacingSpanner.strict_note_spacing = True
    >>> abjad.override(score).SpanBar.stencil = False
    >>> abjad.override(score).Stem.stencil = False
    >>> abjad.override(score).TimeSignature.stencil = False
    >>> abjad.setting(score).proportional_notation_duration = abjad.SchemeMoment(
    ...     (1, 20)
    ... )
    ...

::

    >>> file = abjad.LilyPondFile(
    ...     items=[score, abjad.Block(name="paper"), abjad.Block(name="layout")],
    ...     includes=[
    ...         "abjad.ily",
    ...         "ekmelos-ji-accidental-markups.ily",
    ...     ],
    ...     global_staff_size=16,
    ... )
    ...
    >>> file.paper_block.items.append("indent = 0")
    >>> file.layout_block.items.append(r'\accidentalStyle "dodecaphonic"')
    >>> abjad.show(file)


Third Example
-------------

::

    >>> rule_dict = {"A": "AB", "B": "BC", "C": "BDC", "D": "EF", "E": "FB", "F": "A"}
    >>> lind_list = evans.Sequence.lindenmayer(seed="AB", rules=rule_dict, iters=7)
    >>> lind_list
    Sequence(['A', 'B', 'B', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'C', 'A', 'B', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'C', 'A', 'B', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'B', 'C', 'B', 'D', 'C', 'A', 'B', 'B', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'C', 'A', 'B', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'C', 'A', 'B', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'B', 'C', 'B', 'D', 'C', 'A', 'B', 'B', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'C', 'A', 'B', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'C', 'A', 'B', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'B', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'B', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'B', 'C', 'B', 'D', 'C', 'A', 'B', 'B', 'C', 'B', 'C', 'B', 'D', 'C', 'B', 'C', 'E', 'F', 'B', 'D', 'C', 'A', 'B', 'C', 'A', 'B', 'B', 'C', 'B', 'D', 'C', 'F', 'B', 'A', 'B', 'C', 'E', 'F', 'B', 'D', 'C'])

::

    >>> mapping_dict = {
    ...     "A": 0,
    ...     "B": 1,
    ...     "C": 2,
    ...     "D": 3,
    ...     "E": 4,
    ...     "F": 5,
    ... }
    ...
    >>> map = lind_list.map_dict(mapping_dict)
    >>> map = evans.Sequence([0, 1, 2, 4, 7, 8]).map_indices(map)
    >>> map
    Sequence([0, 1, 1, 2, 1, 2, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 0, 1, 2, 0, 1, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 0, 1, 2, 0, 1, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 0, 1, 1, 2, 1, 4, 2, 0, 1, 1, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 0, 1, 2, 0, 1, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 0, 1, 2, 0, 1, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 0, 1, 1, 2, 1, 4, 2, 0, 1, 1, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 0, 1, 2, 0, 1, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 0, 1, 2, 0, 1, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 0, 1, 1, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 0, 1, 1, 2, 1, 2, 1, 4, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2, 0, 1, 1, 2, 1, 4, 2, 0, 1, 1, 2, 1, 2, 1, 4, 2, 1, 2, 7, 8, 1, 4, 2, 0, 1, 2, 0, 1, 1, 2, 1, 4, 2, 8, 1, 0, 1, 2, 7, 8, 1, 4, 2])

::

    >>> handler = evans.PitchHandler(map, forget=False)
    >>> staff = abjad.Staff([abjad.Note() for _ in map])
    >>> handler(staff)

::

    >>> score = abjad.Score([staff])
    >>> abjad.override(score).BarLine.stencil = False
    >>> abjad.override(score).Beam.stencil = False
    >>> abjad.override(score).Flag.stencil = False
    >>> abjad.override(score).Rest.stencil = False
    >>> abjad.override(score).SpacingSpanner.strict_note_spacing = True
    >>> abjad.override(score).SpanBar.stencil = False
    >>> abjad.override(score).Stem.stencil = False
    >>> abjad.override(score).TimeSignature.stencil = False
    >>> abjad.setting(score).proportional_notation_duration = abjad.SchemeMoment(
    ...     (1, 20)
    ... )
    ...

::

    >>> file = abjad.LilyPondFile(
    ...     items=[score, abjad.Block(name="paper"), abjad.Block(name="layout")],
    ...     includes=[
    ...         "abjad.ily",
    ...         "ekmelos-ji-accidental-markups.ily",
    ...     ],
    ...     global_staff_size=16,
    ... )
    ...
    >>> file.paper_block.items.append("indent = 0")
    >>> file.layout_block.items.append(r'\accidentalStyle "dodecaphonic"')
    >>> abjad.show(file)
