from fractions import Fraction

import abjad

# from evans.AttachmentHandlers.CyclicList import CyclicList


def _apply_position_and_span_to_leaves(
    selections, positions, style, span_command, span_padding
):
    for run in abjad.select(selections).runs():
        ties = abjad.select(run).logical_ties(pitched=True)
        following_leaf = abjad.inspect(ties[-1][-1]).leaf(1)
        distance = len(ties) + 1
        start_strings = [positions(r=1)[0] for _ in range(distance)]
        for i, start_string in enumerate(start_strings[:-1]):
            if all(start_string[_].isdigit() for _ in (0, -1)):
                if Fraction(
                    int(start_strings[i][0]), int(start_strings[i][-1])
                ) > Fraction(
                    int(start_strings[i + 1][0]), int(start_strings[i + 1][-1])
                ):
                    start_strings[
                        i
                    ] = fr"""\center-column {{ \center-align \vcenter \musicglyph \evans-upbow \upright \fraction {start_string[0]} {start_string[-1]} }}"""
                elif Fraction(
                    int(start_strings[i][0]), int(start_strings[i][-1])
                ) < Fraction(
                    int(start_strings[i + 1][0]), int(start_strings[i + 1][-1])
                ):
                    start_strings[
                        i
                    ] = fr"""\center-column {{ \center-align \vcenter \musicglyph \evans-downbow \upright \fraction {start_string[0]} {start_string[-1]} }}"""
                else:
                    start_strings[
                        i
                    ] = fr"""\center-column {{ \center-align \vcenter \upright \fraction {start_string[0]} {start_string[-1]} }}"""
            else:
                start_strings[
                    i
                ] = fr"""\center-column {{ \upright \center-align \vcenter {start_string} }}"""
        start_indicators = [
            abjad.StartTextSpan(
                left_text=abjad.Markup(start_string, literal=True),
                style=fr"{style}-with-arrow",
                command=r"\startTextSpan" + span_command,
                right_padding=1.4,
            )
            for start_string in start_strings
        ]
        final_indicator = abjad.StartTextSpan()
        if all(start_string[-1].isdigit() for _ in (0, -1)):
            final_indicator = abjad.StartTextSpan(
                left_text=abjad.Markup(
                    fr"""\center-column {{ \center-align \vcenter \upright \fraction {start_strings[-1][0]} {start_strings[-1][-1]} }}""",
                    literal=True,
                ),
                style=r"invisible-line",
                command=r"\startTextSpan" + span_command,
                right_padding=3,
            )
        else:
            final_indicator = abjad.StartTextSpan(
                left_text=abjad.Markup(
                    fr"""\center-column {{ \center-align \upright \vcenter {start_strings[-1]} }}""",
                    literal=True,
                ),
                style=r"invisible-line",
                command=r"\startTextSpan" + span_command,
                right_padding=3,
            )
        for indicator in start_indicators:
            abjad.tweak(indicator).staff_padding = span_padding
        abjad.tweak(final_indicator).staff_padding = span_padding
        abjad.attach(start_indicators[0], ties[0][0])
        for pair in zip(ties[1:], start_indicators[1:]):
            tie, start_indicator = pair
            abjad.attach(
                abjad.StopTextSpan(command=r"\stopTextSpan" + span_command), tie[0]
            )
            abjad.attach(start_indicator, tie[0])
        abjad.attach(
            abjad.StopTextSpan(command=r"\stopTextSpan" + span_command), following_leaf
        )
        abjad.attach(final_indicator, following_leaf)
        abjad.attach(
            abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
            abjad.inspect(following_leaf).leaf(1),
        )


# ###test###
# staff = abjad.Staff("c'8 c'8 c'8 c'8 c'8 c'8 r8 r8 c'8 c'8 c'8 c'8 c'8 c'8 r8 r8")
# applicator = _apply_position_and_span_to_leaves(selections=staff[:], positions=CyclicList(lst=["1/2", "1/1", "1/4"], continuous=True), style="solid-line", span_command="One", span_padding=1.5)
# abjad.show(staff)
