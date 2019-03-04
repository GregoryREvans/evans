import abjad

class TextSpanHandler:
    def __init__(
        self,
        span_one_positions=None,
        span_one_style=None,
        attach_span_one_to=None,
        continuous=False,
        ):
        def cyc(lst):
            if self.continuous == False:
                self._count = 0
            while True:
                yield lst[self._count % len(lst)]
                self._count += 1
        self.span_one_positions = span_one_positions
        self.span_one_style = span_one_style
        self.attach_span_one_to = attach_span_one_to
        self.continuous = continuous
        self._cyc_span_one_positions = cyc(span_one_positions)
        self._count = 0

    def __call__(self, selections):
        return self._add_spanners(selections)

    def _add_spanners(self, selections):
        if self.attach_span_one_to != None:
            if self.attach_span_one_to == 'bounds':
                self._apply_position_and_span_to_bounds(selections, spanner_number=r'One')
            elif self.attach_span_one_to == 'leaves':
                self._apply_position_and_span_to_leaves(selections, spanner_number=r'One')
        else:
            pass
        return selections

    def _apply_position_and_span_to_bounds(self, selections, spanner_number):
        for run in abjad.select(selections).runs():
            start_span = abjad.StartTextSpan(
                command=r'\startTextSpan' + spanner_number,
                left_text=abjad.Markup(next(self._cyc_span_one_positions)).upright(),
                style=self.span_one_style + '-with-arrow',
                )
            stop_span = abjad.StartTextSpan(
                command=r'\startTextSpan' + spanner_number,
                left_text=abjad.Markup(next(self._cyc_span_one_positions)).upright(),
                style=self.span_one_style + '-with-hook',
            )
            if len(run) < 2:
                abjad.attach(stop_span, run[0])
            else:
                abjad.attach(start_span, run[0])
                abjad.attach(abjad.StopTextSpan(command=r'\startTextSpan' + spanner_number), run[-1])
                abjad.attach(stop_span, run[-1])
            abjad.override(run[0]).text_spanner.staff_padding = 8
            abjad.override(run[-1]).text_spanner.staff_padding = 8
        return selections

    def _apply_position_and_span_to_leaves(self, selections, spanner_number):
        for run in abjad.select(selections).runs():
            start_span = abjad.StartTextSpan(
                command=r'\startTextSpan' + spanner_number,
                left_text=abjad.Markup(next(self._cyc_span_one_positions)).upright(),
                style=self.span_one_style + '-with-arrow',
                )
            stop_span = abjad.StartTextSpan(
                command=r'\startTextSpan' + spanner_number,
                left_text=abjad.Markup(next(self._cyc_span_one_positions)).upright(),
                style=self.span_one_style + '-with-hook',
            )
            if len(run) < 2:
                continue
            else:
                for tie in abjad.select(run).logical_ties():
                    abjad.attach(start_span, tie[0])
                    abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpan' + spanner_number), tie[-1])
                    for leaf in abjad.select(tie).leaves():
                        abjad.override(leaf).text_spanner.staff_padding = 8
                abjad.detach(start_span, run[-1])
                abjad.attach(stop_span, run[-1])
        return selections
