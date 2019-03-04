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
                self._apply_position_and_span_to_bounds(selections)
            elif self.attach_span_one_to == 'leaves':
                self._apply_position_and_span_to_leaves(selections)
        else:
            pass
        return selections

    def _apply_position_and_span_to_bounds(self, selections):
        for run in abjad.select(selections).runs():
            start_span = abjad.StartTextSpan(
                left_text=abjad.Markup(next(self._cyc_span_one_positions)).upright(),
                style=self.span_one_style + '-with-arrow',
                )
            stop_span = abjad.StartTextSpan(
                left_text=abjad.Markup(next(self._cyc_span_one_positions)).upright(),
                style=self.span_one_style + '-with-hook',
            )
            if len(run) < 2:
                abjad.attach(stop_span, run[0])
            else:
                abjad.attach(start_span, run[0])
                abjad.attach(abjad.StopTextSpan(), run[-1])
                abjad.attach(stop_span, run[-1])
            abjad.override(run[0]).text_spanner.staff_padding = 8
            abjad.override(run[-1]).text_spanner.staff_padding = 8
        return selections

    def _apply_position_and_span_to_leaves(self, selections):
        for run in abjad.select(selections).runs():
            tie_list = []
            for tie in abjad.select(run).logical_ties():
                tie_list.append(tie)
            if len(tie_list) < 2:
                continue
            else:
                for tie in abjad.select(run).logical_ties():
                    start_span = abjad.StartTextSpan(
                        left_text=abjad.Markup(next(self._cyc_span_one_positions)).upright(),
                        style=self.span_one_style + '-with-arrow',
                        )
                    abjad.text_spanner(tie[:], start_text_span=start_span)
                    for leaf in abjad.select(tie).leaves():
                        abjad.override(leaf).text_spanner.staff_padding = 8
                    if len(tie) > 1:
                        abjad.attach(abjad.StopTextSpan(), tie[0])
                abjad.detach(start_span, run[-1])
                stop_span = abjad.StartTextSpan(
                    left_text=abjad.Markup(next(self._cyc_span_one_positions)).upright(),
                    style=self.span_one_style + '-with-hook',
                    )
                abjad.attach(stop_span, run[-1])
        return selections
