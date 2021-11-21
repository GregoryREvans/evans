"""
Metric modulation.
"""
import abjad
import quicktions


def mixed_number(fraction_pair=(288, 5)):
    fraction_pair = quicktions.Fraction(fraction_pair)
    q = fraction_pair.numerator // fraction_pair.denominator
    r = quicktions.Fraction(
        (fraction_pair.numerator % fraction_pair.denominator)
        / fraction_pair.denominator
    ).limit_denominator()
    return (q, (r.numerator, r.denominator))


def compare_speed(l_note=None, r_note=None):
    left_dur = abjad.get.duration(l_note)
    right_dur = abjad.get.duration(r_note)
    multiplier = left_dur / right_dur
    return multiplier


def calculate_metric_modulation(l_tempo=60, l_note=None, r_note=None):
    left_dur = abjad.get.duration(l_note)
    right_dur = abjad.get.duration(r_note)
    multiplier = right_dur / left_dur
    new_tempo = l_tempo * multiplier
    return new_tempo


def metric_modulation(
    metronome_mark=((1, 4), 60),
    left_note=(abjad.Note("c'8")),
    right_note=(abjad.Note("c'8.")),
    modulated_beat=(abjad.Note("c'4")),
    rounded=None,
    font_size=None,
    leaf_scale=(0.6, 0.6),
    raise_value=None,
):
    r"""
    Makes metric modulation markup.

    .. container:: example

        >>> m = evans.metric_modulation(
        ...     metronome_mark=((1, 4), 96),
        ...     left_note=(abjad.Tuplet(multiplier=(5, 3), components=[abjad.Note()])),
        ...     right_note=(abjad.Note("c'4")),
        ...     modulated_beat=(abjad.Note("c'4")),
        ... )
        ...
        >>> staff = abjad.Staff("c'1")
        >>> abjad.attach(m, staff[0])
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[score],
        ...     includes=[
        ...         "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily"
        ...     ],
        ...     global_staff_size=16,
        ... )
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'1
                ^ \markup {
                  \huge
                  \concat {
                      \abjad-metronome-mark-mixed-number-markup #2 #0 #1 #"57" #"3" #"5"
                      \hspace #1
                      \upright [
                      \abjad-metric-modulation-tuplet-lhs #2 #0 #5 #3 #2 #0 #'(0.6 . 0.6)
                      \hspace #0.5
                      \upright ]
                  }
                }
            }

    .. container:: example

        >>> m = evans.metric_modulation(
        ...     metronome_mark=((1, 4), 96),
        ...     left_note=(abjad.Note("c'4.")),
        ...     right_note=(abjad.Note("c'4")),
        ...     modulated_beat=(abjad.Note("c'4")),
        ... )
        ...
        >>> staff = abjad.Staff("c'1")
        >>> abjad.attach(m, staff[0])
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[score],
        ...     includes=[
        ...         "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily"
        ...     ],
        ...     global_staff_size=16,
        ... )
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'1
                ^ \markup {
                  \huge
                  \concat {
                      \abjad-metronome-mark-markup #2 #0 #1 #"64"
                      \hspace #1
                      \upright [
                      \abjad-metric-modulation #2 #1 #2 #0 #'(0.6 . 0.6)
                      \hspace #0.5
                      \upright ]
                  }
                }
            }

    .. container:: example

        >>> m = evans.metric_modulation(
        ...     metronome_mark=((1, 4), 71),
        ...     left_note=(abjad.Tuplet(multiplier=(10, 9), components=[abjad.Note("c'16")])),
        ...     right_note=(abjad.Note("c'16")),
        ...     modulated_beat=(abjad.Note("c'4")),
        ... )
        ...
        >>> staff = abjad.Staff("c'1")
        >>> abjad.attach(m, staff[0])
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[score],
        ...     includes=[
        ...         "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily"
        ...     ],
        ...     global_staff_size=16,
        ... )
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'1
                ^ \markup {
                  \huge
                  \concat {
                      \abjad-metronome-mark-mixed-number-markup #2 #0 #1 #"63" #"9" #"10"
                      \hspace #1
                      \upright [
                      \abjad-metric-modulation-tuplet-lhs #4 #0 #10 #9 #4 #0 #'(0.6 . 0.6)
                      \hspace #0.5
                      \upright ]
                  }
                }
            }

    .. container:: example

        >>> m = evans.metric_modulation(
        ...     metronome_mark=((1, 4), 40),
        ...     left_note=(abjad.Tuplet(multiplier=(2, 3), components=[abjad.Note("c'2")])),
        ...     right_note=(abjad.Note("c'2")),
        ...     modulated_beat=(abjad.Note("c'4")),
        ... )
        ...
        >>> staff = abjad.Staff("c'1")
        >>> abjad.attach(m, staff[0])
        >>> score = abjad.Score([staff])
        >>> moment = "#(ly:make-moment 1 25)"
        >>> abjad.setting(score).proportional_notation_duration = moment
        >>> file = abjad.LilyPondFile(
        ...     items=[score],
        ...     includes=[
        ...         "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily"
        ...     ],
        ...     global_staff_size=16,
        ... )
        >>> abjad.show(file) # doctest: +SKIP

        .. docs::

            >>> print(abjad.lilypond(staff))
            \new Staff
            {
                c'1
                ^ \markup {
                  \huge
                  \concat {
                      \abjad-metronome-mark-markup #2 #0 #1 #"60"
                      \hspace #1
                      \upright [
                      \abjad-metric-modulation-tuplet-lhs #1 #0 #2 #3 #1 #0 #'(0.6 . 0.6)
                      \hspace #0.5
                      \upright ]
                  }
                }
            }

    """
    tempo_note = abjad.Note()
    tempo_note.written_duration = metronome_mark[0]
    left_speed_multiplier = compare_speed(l_note=tempo_note, r_note=left_note)
    left_speed = metronome_mark[1] * left_speed_multiplier
    modulation_speed = calculate_metric_modulation(
        l_tempo=left_speed, l_note=left_note, r_note=right_note
    )
    returned_speed = float(modulation_speed * compare_speed(left_note, modulated_beat))
    if font_size is not None:
        size = fr"  \override #'(font-size . {font_size})"
    else:
        size = r"  \huge"
    if returned_speed % 1 == 0.0:
        met = abjad.MetronomeMark.make_tempo_equation_markup(
            abjad.get.duration(modulated_beat), int(returned_speed)
        )
        mod = abjad.MetricModulation(
            left_rhythm=left_note, right_rhythm=right_note, scale=leaf_scale
        )
        if raise_value is None:
            mark = abjad.LilyPondLiteral(
                [
                    r"^ \markup {",
                    size,
                    r"  \concat {",
                    f"      {str(met)[8:]}",
                    r"      \hspace #1",
                    r"      \upright [",
                    f"      {str(mod)[8:]}",
                    r"      \hspace #0.5",
                    r"      \upright ]",
                    r"  }",
                    r"}",
                ],
                format_slot="after",
            )
        else:
            mark = abjad.LilyPondLiteral(
                [
                    r"^ \markup {",
                    size,
                    fr"  \raise #{raise_value} \with-dimensions-from \null",
                    r"  \concat {",
                    f"      {str(met)[8:]}",
                    r"      \hspace #1",
                    r"      \upright [",
                    f"      {str(mod)[8:]}",
                    r"      \hspace #0.5",
                    r"      \upright ]",
                    r"  }",
                    r"}",
                ],
                format_slot="after",
            )
        return mark
    else:
        if rounded is True:
            met = abjad.MetronomeMark.make_tempo_equation_markup(
                abjad.get.duration(modulated_beat),
                quicktions.Fraction(round(returned_speed)).limit_denominator(),
            )
            mod = abjad.MetricModulation(
                left_rhythm=left_note, right_rhythm=right_note, scale=leaf_scale
            )
            if raise_value is None:
                mark = abjad.LilyPondLiteral(
                    [
                        r"^ \markup {",
                        size,
                        r"  \concat {",
                        "       c.",
                        r"      \hspace #1",
                        f"      {str(met)[8:]}",
                        r"      \hspace #1",
                        r"      \upright [",
                        f"      {str(mod)[8:]}",
                        r"      \hspace #0.5",
                        r"      \upright ]",
                        r"  }",
                        r"}",
                    ],
                    format_slot="after",
                )
            else:
                mark = abjad.LilyPondLiteral(
                    [
                        r"^ \markup {",
                        size,
                        fr"  \raise #{raise_value} \with-dimensions-from \null",
                        r"  \concat {",
                        "       c.",
                        r"      \hspace #1",
                        f"      {str(met)[8:]}",
                        r"      \hspace #1",
                        r"      \upright [",
                        f"      {str(mod)[8:]}",
                        r"      \hspace #0.5",
                        r"      \upright ]",
                        r"  }",
                        r"}",
                    ],
                    format_slot="after",
                )
        else:
            met = abjad.MetronomeMark.make_tempo_equation_markup(
                abjad.get.duration(modulated_beat),
                quicktions.Fraction(returned_speed).limit_denominator(),
            )
            mod = abjad.MetricModulation(
                left_rhythm=left_note, right_rhythm=right_note, scale=leaf_scale
            )
            if raise_value is None:
                mark = abjad.LilyPondLiteral(
                    [
                        r"^ \markup {",
                        size,
                        r"  \concat {",
                        f"      {str(met)[8:]}",
                        r"      \hspace #1",
                        r"      \upright [",
                        f"      {str(mod)[8:]}",
                        r"      \hspace #0.5",
                        r"      \upright ]",
                        r"  }",
                        r"}",
                    ],
                    format_slot="after",
                )
            else:
                mark = abjad.LilyPondLiteral(
                    [
                        r"^ \markup {",
                        size,
                        fr"  \raise #{raise_value} \with-dimensions-from \null",
                        r"  \concat {",
                        f"      {str(met)[8:]}",
                        r"      \hspace #1",
                        r"      \upright [",
                        f"      {str(mod)[8:]}",
                        r"      \hspace #0.5",
                        r"      \upright ]",
                        r"  }",
                        r"}",
                    ],
                    format_slot="after",
                )
        return mark


def calculate_tempo_modulated_duration(
    original_tempo=((1, 4), 60),
    new_tempo=((1, 4), 120),
    duration=abjad.Duration((1, 1)),
):
    """

    .. container:: example

        >>> evans.calculate_tempo_modulated_duration(
        ...     original_tempo=((1, 4), 60),
        ...     new_tempo=((1, 4), 120),
        ...     duration=abjad.Duration((1, 1)),
        ... )
        ...
        Duration(2, 1)

    .. container:: example

        >>> evans.calculate_tempo_modulated_duration(
        ...     original_tempo=((1, 4), 72),
        ...     new_tempo=((1, 4), 83),
        ...     duration=abjad.Duration((23, 8)),
        ... )
        ...
        Duration(1909, 576)

    """

    def convert_to_quarter(tempo):
        notehead_string = f"{tempo[0][0]}/{tempo[0][1]}"
        beat_change = quicktions.Fraction("1/4") / quicktions.Fraction(notehead_string)
        new_speed = tempo[1] * beat_change
        return ((1, 4), new_speed)

    original_tempo = convert_to_quarter(original_tempo)
    new_tempo = convert_to_quarter(new_tempo)
    multiplier = original_tempo[1] / new_tempo[1]
    timed_duration = duration / multiplier
    return timed_duration
