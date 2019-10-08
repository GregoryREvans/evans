import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList
from fractions import Fraction


class TextSpanHandler:
    def __init__(
        self,
        span_one_positions=None,
        span_one_style=None,
        span_one_padding=None,
        attach_span_one_to=None,
        span_two_positions=None,
        span_two_style=None,
        span_two_padding=None,
        attach_span_two_to=None,
        span_three_positions=None,
        span_three_style=None,
        span_three_padding=None,
        attach_span_three_to=None,
        continuous=False,
    ):
        self.span_one_positions = span_one_positions
        self.span_one_style = span_one_style
        self.span_one_padding = span_one_padding
        self.attach_span_one_to = attach_span_one_to
        self.span_two_positions = span_two_positions
        self.span_two_style = span_two_style
        self.span_two_padding = span_two_padding
        self.attach_span_two_to = attach_span_two_to
        self.span_three_positions = span_three_positions
        self.span_three_style = span_three_style
        self.span_three_padding = span_three_padding
        self.attach_span_three_to = attach_span_three_to
        self.continuous = continuous
        self._count_1 = -1
        self._count_2 = -1
        self._count_3 = -1
        self._cyc_span_one_positions = CyclicList(
            span_one_positions, self.continuous, self._count_1
        )
        self._cyc_span_two_positions = CyclicList(
            span_two_positions, self.continuous, self._count_2
        )
        self._cyc_span_three_positions = CyclicList(
            span_three_positions, self.continuous, self._count_3
        )

    def __call__(self, selections):
        self._add_spanners(selections)

    def _add_spanners(self, selections):
        # print('Adding spanners ...')
        if self.attach_span_one_to == None:
            self._apply_empty_spanner(selections, r"One")
        elif self.attach_span_one_to == "bounds":
            self._apply_position_and_span_to_bounds(
                selections,
                self._cyc_span_one_positions,
                self.span_one_style,
                r"One",
                self.span_one_padding,
            )
        elif self.attach_span_one_to == "leaves":
            self._apply_position_and_span_to_leaves(
                selections,
                self._cyc_span_one_positions,
                self.span_one_style,
                r"One",
                self.span_one_padding,
            )
        elif self.attach_span_one_to == "left":
            self._apply_position_and_span_to_left(
                selections,
                self._cyc_span_one_positions,
                self.span_one_style,
                r"One",
                self.span_one_padding,
            )
        else:
            pass
        if self.attach_span_two_to == None:
            self._apply_empty_spanner(selections, r"Two")
        elif self.attach_span_two_to == "bounds":
            self._apply_position_and_span_to_bounds(
                selections,
                self._cyc_span_two_positions,
                self.span_two_style,
                r"Two",
                self.span_two_padding,
            )
        elif self.attach_span_two_to == "leaves":
            self._apply_position_and_span_to_leaves(
                selections,
                self._cyc_span_two_positions,
                self.span_two_style,
                r"Two",
                self.span_two_padding,
            )
        elif self.attach_span_two_to == "left":
            self._apply_position_and_span_to_left(
                selections,
                self._cyc_span_two_positions,
                self.span_two_style,
                r"Two",
                self.span_two_padding,
            )
        else:
            pass
        if self.attach_span_three_to == None:
            self._apply_empty_spanner(selections, r"Three")
        elif self.attach_span_three_to == "bounds":
            self._apply_position_and_span_to_bounds(
                selections,
                self._cyc_span_three_positions,
                self.span_three_style,
                r"Three",
                self.span_three_padding,
            )
        elif self.attach_span_three_to == "leaves":
            self._apply_position_and_span_to_leaves(
                selections,
                self._cyc_span_three_positions,
                self.span_three_style,
                r"Three",
                self.span_three_padding,
            )
        elif self.attach_span_three_to == "left":
            self._apply_position_and_span_to_left(
                selections,
                self._cyc_span_three_positions,
                self.span_three_style,
                r"Three",
                self.span_three_padding,
            )
        else:
            pass

    def _apply_empty_spanner(self, selections, span_command):
        # print('Adding empty spanner ...')
        first_leaf = abjad.select(selections).leaves()[0]
        abjad.attach(
            abjad.StopTextSpan(command=r"\stopTextSpan" + span_command), first_leaf
        )

    def _apply_position_and_span_to_bounds(
        self, selections, positions, style, span_command, span_padding
    ):
        # print('Adding bounded spanner ...')
        for run in abjad.select(selections).runs():
            if len(run) < 2:
                start_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(positions(r=1)[0]).upright(),
                    style=style + "-with-hook",
                    command=r"\startTextSpan" + span_command,
                )
                abjad.attach(
                    abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                    abjad.inspect(run[-1]).leaf(1),
                )
                abjad.attach(start_span, run[0])
                abjad.tweak(start_span).staff_padding = span_padding
            else:
                start_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(positions(r=1)[0]).upright(),
                    style=style + "-with-arrow",
                    command=r"\startTextSpan" + span_command,
                    right_padding=1.4,
                )
                stop_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(positions(r=1)[0]).upright(),
                    style=style + "-with-hook",
                    command=r"\startTextSpan" + span_command,
                    right_padding=3,
                )
                abjad.attach(start_span, run[0])
                abjad.attach(
                    abjad.StopTextSpan(command=r"\stopTextSpan" + span_command), run[-1]
                )
                abjad.attach(stop_span, run[-1])
                abjad.attach(
                    abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                    abjad.inspect(run[-1]).leaf(1),
                )
                abjad.tweak(start_span).staff_padding = span_padding
                abjad.tweak(stop_span).staff_padding = span_padding

    def _apply_position_and_span_to_leaves(
        self, selections, positions, style, span_command, span_padding
    ):
        # print('Adding leaf spanner ...')
        for run in abjad.select(selections).runs():
            if len(abjad.select(run).logical_ties()) > 1:
                ties = abjad.select(run).logical_ties()
                start_strings = [positions(r=1)[0] for _ in ties]
                bowings = []
                for i, start_string in enumerate(start_strings[:-1]):
                    if all(start_string[_].isdigit() for _ in (0, -1)):
                        if Fraction(
                            int(start_strings[i][0]), int(start_strings[i][-1])
                        ) > Fraction(
                            int(start_strings[i + 1][0]), int(start_strings[i + 1][-1])
                        ):
                            bowings.append(abjad.Markup.musicglyph("scripts.upbow"))
                        elif Fraction(
                            int(start_strings[i][0]), int(start_strings[i][-1])
                        ) < Fraction(
                            int(start_strings[i + 1][0]), int(start_strings[i + 1][-1])
                        ):
                            bowings.append(abjad.Markup.musicglyph("scripts.downbow"))
                        else:
                            bowings.append(abjad.Markup(""))
                # bowings.append("")
                for i, pair in enumerate(zip(start_strings, bowings)):
                    if all(start_string[_].isdigit() for _ in (0, -1)):
                        start_strings[
                            i
                        ] = f"""\\upright \\center-align \\vcenter \\fraction {pair[0][0]} {pair[0][-1]}"""
                start_indicators = [
                    abjad.StartTextSpan(
                        left_text=abjad.Markup.center_column([pair[-1], start_string]),
                        style=f"{style}-with-arrow",
                        command=r"\startTextSpan" + span_command,
                        right_padding=1.4,
                    )
                    for bowing, start_string in zip(bowings[:-1], start_strings[:-1])
                ]
                start_indicators.append(
                    abjad.StartTextSpan(
                        left_text=abjad.Markup(start_strings[-1]),
                        style=f"invisible-line",
                        command=r"\startTextSpan" + span_command,
                        right_padding=3,
                    )
                )
                for indicator in start_indicators:
                    abjad.tweak(indicator).staff_padding = span_padding
                for pair in zip(ties[0], start_indicators[0]):
                    tie, start_indicator = pair
                    abjad.attach(start_indicator, tie[0])
                for i, pair in enumerate(zip(ties[1:], start_indicators[1:])):
                    tie, start_indicator = pair
                    abjad.attach(
                        abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                        tie[0],
                    )
                    abjad.attach(start_indicator, tie[0])
                abjad.attach(
                    abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                    abjad.inspect(run[-1]).leaf(1),
                )
            else:
                continue

    def _apply_position_and_span_to_left(
        self, selections, positions, style, span_command, span_padding
    ):
        # print('Adding left spanner ...')
        runs = abjad.select(selections).runs()
        start_strings = [positions(r=1)[0] for _ in runs]
        start_indicators = [
            abjad.StartTextSpan(
                left_text=abjad.Markup(start_string).upright(),
                style=f"{style}-with-hook",
                command=r"\startTextSpan" + span_command,
                right_padding=3,
            )
            for start_string in start_strings
        ]
        for indicator in start_indicators:
            abjad.tweak(indicator).staff_padding = span_padding
        for i, pair in enumerate(zip(runs, start_indicators)):
            run, start_indicator = pair
            abjad.attach(start_indicator, run[0])
            abjad.attach(
                abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                abjad.inspect(run[-1]).leaf(1),
            )
