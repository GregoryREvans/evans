import abjad

class TextSpanHandler:
    def __init__(
        self,
        positions,
        continuous=False,
        ):
        def cyc(lst):
            if self.continuous == False:
                self._count = 0
            while True:
                yield lst[self._count % len(lst)]
                self._count += 1
        self.positions = positions
        self.continuous = continuous
        self._cyc_positions = cyc(positions)
        self._count = 0

    def __call__(self, selections):
        return self._apply_position_and_span(selections)

    def _apply_position_and_span(self, selections):
        for run in abjad.select(selections).runs():
            print(run)
            span = abjad.StartTextSpan(
                left_text=abjad.Markup(next(self._cyc_positions)).upright(),
                right_text=abjad.Markup(next(self._cyc_positions)).upright(),
                style='dashed-line-with-arrow',
                )
            abjad.text_spanner(run[:], start_text_span=span)
            abjad.override(run[0]).text_spanner.staff_padding = 4
        return selections
