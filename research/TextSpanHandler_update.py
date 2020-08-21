import abjad
import quicktions
from evans import CyclicList


# incorporate spanner anchors
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
        forget=True,
        count_1=-1,
        count_2=-1,
        count_3=-1,
        name="TextSpan Handler",
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
        self.forget = forget
        self._count_1 = count_1
        self._count_2 = count_2
        self._count_3 = count_3
        self._cyc_span_one_positions = CyclicList(
            span_one_positions, self.forget, self._count_1
        )
        self._cyc_span_two_positions = CyclicList(
            span_two_positions, self.forget, self._count_2
        )
        self._cyc_span_three_positions = CyclicList(
            span_three_positions, self.forget, self._count_3
        )
        self.name = name

    def __call__(self, selections):
        self._add_spanners(selections)

    def _add_spanners(self, selections):
        if self.attach_span_one_to == "bounds":
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
        if self.attach_span_two_to == "bounds":
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
        if self.attach_span_three_to == "bounds":
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
        first_leaf = abjad.select(selections).leaves()[0]
        abjad.attach(
            abjad.StopTextSpan(command=r"\stopTextSpan" + span_command), first_leaf
        )

    def _apply_position_and_span_to_bounds(
        self, selections, positions, style, span_command, span_padding
    ):
        for run in abjad.select(selections).runs():
            if len(run) < 2:
                start_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(positions(r=1)[0]).upright(),
                    style=style + "-with-hook",
                    command=r"\startTextSpan" + span_command,
                )
                abjad.attach(
                    abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                    abjad.get.leaf(run[-1], 1),
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
                    abjad.get.leaf(run[-1], 1),
                )
                abjad.tweak(start_span).staff_padding = span_padding
                abjad.tweak(stop_span).staff_padding = span_padding

    def _apply_position_and_span_to_leaves(
        self, selections, positions, style, span_command, span_padding
    ):
        for run in abjad.select(selections).runs():
            ties = abjad.select(run).logical_ties(pitched=True)
            leaf_after_run = abjad.get.leaf(ties[-1][-1], 1)
            following_leaf = abjad.Note("c'16")
            distance = len(ties) + 1
            start_strings = [positions(r=1)[0] for _ in range(distance)]
            for i, start_string in enumerate(start_strings[:-1]):
                if all(start_string[_].isdigit() for _ in (0, -1)):
                    if quicktions.Fraction(
                        int(start_strings[i][0]), int(start_strings[i][-1])
                    ) > quicktions.Fraction(
                        int(start_strings[i + 1][0]), int(start_strings[i + 1][-1])
                    ):
                        start_strings[
                            i
                        ] = fr"""\center-column {{ \center-align \vcenter \musicglyph \evans-upbow \vspace #0.2 \upright \fraction {start_string[0]} {start_string[-1]} }}"""
                    elif quicktions.Fraction(
                        int(start_strings[i][0]), int(start_strings[i][-1])
                    ) < quicktions.Fraction(
                        int(start_strings[i + 1][0]), int(start_strings[i + 1][-1])
                    ):
                        start_strings[
                            i
                        ] = fr"""\center-column {{ \center-align \vcenter \musicglyph \evans-downbow \vspace #0.2 \upright \fraction {start_string[0]} {start_string[-1]} }}"""
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
                abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                following_leaf,
            )
            abjad.attach(final_indicator, following_leaf)
            abjad.attach(
                abjad.StopTextSpan(command=r"\stopTextSpan" + span_command),
                leaf_after_run,
            )
            # add_spanner_anchor(leaf=ties[-1][-1], anchor_leaf=following_leaf) # new

    def _apply_position_and_span_to_left(
        self, selections, positions, style, span_command, span_padding
    ):
        runs = abjad.select(selections).runs()
        start_strings = [positions(r=1)[0] for _ in runs]
        start_indicators = [
            abjad.StartTextSpan(
                left_text=abjad.Markup(start_string).upright(),
                style=fr"{style}-with-hook",
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
                abjad.get.leaf(run[-1], 1),
            )

    def name(self):
        return self.name

    def state(self):
        return abjad.OrderedDict(
            [
                ("count_1", self._cyc_span_one_positions.state()),
                ("count_2", self._cyc_span_two_positions.state()),
                ("count_3", self._cyc_span_three_positions.state()),
            ]
        )
