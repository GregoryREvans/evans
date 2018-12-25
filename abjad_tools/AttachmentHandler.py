import abjad

class AttachmentHandler:

    def __init__(
        self,
        text_list=None,
        line_style=None,
        clef=None,
        continuous=False,
        ):
        def cyc(lst):
            if self.continuous == False:
                self._count = 0
            while True:
                yield lst[self._count % len(lst)]
                self._count += 1
        self.text_list = text_list
        self.line_style = line_style
        self.clef = clef
        self.continuous = continuous
        self._cyc_text = cyc(text_list)
        self._count = 0

    def __call__(self, selections):
        return self.add_attachments(selections)

    def _apply_text_and_span_lr(self, selections):
        text = self._cyc_text
        for run in abjad.select(selections).runs():
            leaves = abjad.select(run).leaves()
            start_span = abjad.StartTextSpan(
                command=r'\startTextSpanOne',
                left_text=abjad.Markup(next(text)).upright(),
                style=self.line_style,
                )
            stop_span = abjad.StartTextSpan(
                command=r'\startTextSpanOne',
                right_padding=2.5,
                left_text=abjad.Markup(next(text)).upright(),
                style='solid-line-with-hook',
                )
            abjad.text_spanner(leaves[0], start_text_span=start_span)
            abjad.attach(abjad.StopTextSpan(command=r'\stopTextSpanOne',), leaves[-1])
            abjad.text_spanner(leaves[-1], start_text_span=stop_span)

    def _apply_text_and_span_l_only(self, selections):
        text = self._cyc_text
        for run in abjad.select(selections).runs():
            leaves = abjad.select(run).leaves()
            span = abjad.StartTextSpan(
                command=r'\startTextSpanOne',
                right_padding=2.5,
                left_text=abjad.Markup(next(text)).upright(),
                style='solid-line-with-hook',
                )
            abjad.text_spanner(leaves[0], start_text_span=span)

    def add_attachments(self, selections):
        runs = abjad.select(selections).runs()
        ties = abjad.select(selections).logical_ties(pitched=True)
        for run in runs:
            if self.clef != None:
                abjad.attach(abjad.Clef(self.clef), run[0]) #doesn't seem to always work, redo entire attachment handler?
            if len(run) > 1:
                leaves = abjad.select(run).leaves()
                if self.text_list != None:
                    if len(self.text_list) > 1:
                        self._apply_text_and_span_lr(run)
                    else:
                        self._apply_text_and_span_l_only(run)
            else:
                leaves = abjad.select(run).leaves()
                if self.text_list != None:
                    self._apply_text_and_span_l_only(run)
        return selections
