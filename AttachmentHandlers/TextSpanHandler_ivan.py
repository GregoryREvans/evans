import abjad

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
        def cyc(lst, key):
            if self.continuous is False:
                self._counters[key] = -1
            while True:
                self._counters[key] += 1
                yield lst[self._counters[key] % len(lst)]
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

        self._attachment_functions = {
            'bounds' : self._apply_position_and_span_to_bounds,
            'leaves' : self._apply_position_and_span_to_leaves,
            'left' : self._apply_position_and_span_to_left,
        }
        self._counters = {
            'span one' : -1, 
            'span two' : -1, 
            'span three' : -1,
        }
        self._spans = {
            r"One" : (cyc(span_one_positions, 'span one'), self.span_one_style, self.span_one_padding, self.attach_span_one_to),
            r"Two" : (cyc(span_two_positions, 'span two'), self.span_two_style, self.span_two_padding, self.attach_span_two_to),
            r"Three" : (cyc(span_three_positions, 'span three'), self.span_three_style, self.span_three_padding, self.attach_span_three_to),
        }


    def __call__(self, selections):
        return self._add_spanners(selections)


    def _add_spanners(self, selections):
        for literal in (r"One", r"Two", r"Three"):
            positions, style, padding, attach_to = self._spans[literal]
            attachment_function = self._attachment_functions[attach_to]
            if attachment_function is not None:
                attachment_function(selections, positions, style, literal, padding)
                continue 
            self._apply_empty_spanner(selections, literal)
        
        return selections 


    def _apply_empty_spanner(self, selections, span_command):
        container = abjad.Container()
        container.extend(selections)
        first_leaf = abjad.select(container).leaves()[0]
        abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpan'+span_command), first_leaf)
        return selections


    def _apply_position_and_span_to_bounds(self, selections, positions, style, span_command, span_padding):
        container = abjad.Container()
        container.extend(selections)
        for run in abjad.select(container).runs():
            if len(run) < 2:
                start_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(next(positions)).upright(),
                    style=style + '-with-hook',
                    command=r'\startTextSpan'+span_command,)
                abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpan'+span_command), run[0])
                abjad.attach(start_span, run[0])
                abjad.tweak(start_span).staff_padding = span_padding
            else:
                start_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(next(positions)).upright(),
                    style=style + '-with-arrow',
                    command=r'\startTextSpan'+span_command,
                    )
                stop_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(next(positions)).upright(),
                    style=style + '-with-hook',
                    command=r'\startTextSpan'+span_command
                    )
                abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpan'+span_command), run[0])
                abjad.attach(start_span, run[0])
                abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpan'+span_command), run[-1])
                abjad.attach(stop_span, run[-1])
                abjad.tweak(start_span).staff_padding = span_padding
                abjad.tweak(stop_span).staff_padding = span_padding
        return selections


    def _apply_position_and_span_to_leaves(self, selections, positions, style, span_command, span_padding):
        container = abjad.Container()
        container.extend(selections)
        for run in abjad.select(container).runs():
            if len(abjad.select(run).logical_ties()) > 1:
                ties = abjad.select(run).logical_ties()
                start_strings = [next(positions) for _ in ties]
                for i, start_string in enumerate(start_strings):
                    if all(
                        start_string[_].isdigit() for _ in (0, -1)
                    ):
                        start_strings[i] = \
                            f'\\upright \\center-align \\vcenter \\fraction {start_string[0]} {start_string[-1]}'
                start_indicators = [
                    abjad.StartTextSpan(
                        left_text=abjad.Markup(start_string),
                        style=f'{style}-with-arrow',
                        command=r'\startTextSpan'+span_command,
                    )
                    for start_string in start_strings[:-1]
                ]
                start_indicators.append(
                    abjad.StartTextSpan(
                        left_text=abjad.Markup(start_strings[-1]),
                        style=f'{style}-with-hook',
                        command=r'\startTextSpan'+span_command
                    )
                )
                for indicator in start_indicators:
                    abjad.tweak(indicator).staff_padding = span_padding
                for i, pair in enumerate(zip(ties, start_indicators)):
                    tie, start_indicator = pair
                    abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpan'+span_command), tie[0])
                    abjad.attach(start_indicator, tie[0])
        return selections


    def _apply_position_and_span_to_left(self, selections, positions, style, span_command, span_padding):
        container = abjad.Container()
        container.extend(selections)
        runs = abjad.select(container).runs()
        start_strings = [next(positions) for _ in runs]
        start_indicators = [
            abjad.StartTextSpan(
                left_text=abjad.Markup(start_string),
                style=f'{style}-with-hook',
                command=r'\startTextSpan'+span_command,
            )
            for start_string in start_strings
        ]
        for indicator in start_indicators:
            abjad.tweak(indicator).staff_padding = span_padding
        for i, pair in enumerate(zip(runs, start_indicators)):
            run, start_indicator = pair
            abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpan'+span_command), run[0])
            abjad.attach(start_indicator, run[0])
        return selections
