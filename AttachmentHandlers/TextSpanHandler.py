import abjad

class TextSpanHandler:

    def __init__(
        self,
        position_list_one=None,
        position_list_two=None,
        position_list_three=None,
        start_style_one=None,
        start_style_two=None,
        start_style_three=None,
        stop_style_one=None,
        stop_style_two=None,
        stop_style_three=None,
        apply_list_one_to=None,
        apply_list_two_to=None,
        apply_list_three_to=None,
        continuous=False,
        ):
        def cyc(lst):
            if self.continuous == False:
                self._count = 0
            while True:
                yield lst[self._count % len(lst)]
                self._count += 1
        self.position_list_one = position_list_one
        self.position_list_two = position_list_two
        self.position_list_three = position_list_three
        self.start_style_one = start_style_one
        self.start_style_two = start_style_two
        self.start_style_three = start_style_three
        self.stop_style_one = stop_style_one
        self.stop_style_two = stop_style_two
        self.stop_style_three = stop_style_three
        self.apply_list_one_to = apply_list_one_to
        self.apply_list_two_to = apply_list_two_to
        self.apply_list_three_to = apply_list_three_to
        self.continuous = continuous
        self._cyc_position_list_one_text = cyc(position_list_one)
        self._cyc_position_list_two_text = cyc(position_list_two)
        self._cyc_position_list_three_text = cyc(position_list_three)
        self._count = 0

    def __call__(self, selections):
        return self.add_spans(selections)

    def add_spans(self, selections):
        if self.position_list_one != None:
            if self.apply_list_one_to == 'left_only':
                pos_list_1 = self._cyc_position_list_one_text
                for run in abjad.select(selections).components(abjad.Voice):
                    self._apply_position_and_span_left_only(staff=voice, poses=pos_list_1, style=self.start_style_one, padding=8.2, command=r'\startTextSpanOne', stop_command=r'\stopTextSpanOne', ending_hook=self.stop_style_one)
            if self.apply_list_one_to == 'edges':
                pos_list_1 = self._cyc_position_list_one_text
                for voice in abjad.select(selections).components(abjad.Voice):
                    self._apply_position_and_span_to_edges(staff=voice, poses=pos_list_1, style=self.start_style_one, padding=8.2, command=r'\startTextSpanOne', stop_command=r'\stopTextSpanOne', ending_hook=self.stop_style_one)
            elif self.apply_list_one_to == 'ties':
                pos_list_1 = self._cyc_position_list_one_text
                for voice in abjad.select(selections).components(abjad.Voice):
                    self._apply_position_and_span_to_ties(staff=voice, poses=pos_list_1, style=self.start_style_one, padding=8.2, command=r'\startTextSpanOne', stop_command=r'\stopTextSpanOne', ending_hook=self.stop_style_one)
            else:
                pass
        if self.position_list_two != None:
            if self.apply_list_two_to == 'left_only':
                pos_list_2 = self._cyc_position_list_two_text
                for voice in abjad.select(selections).components(abjad.Voice):
                    self._apply_position_and_span_left_only(staff=voice, poses=pos_list_2, style=self.start_style_two, padding=10.7, command=r'\startTextSpanTwo', stop_command=r'\stopTextSpanTwo', ending_hook=self.stop_style_two)
            if self.apply_list_two_to == 'edges':
                pos_list_2 = self._cyc_position_list_two_text
                for voice in abjad.select(selections).components(abjad.Voice):
                    self._apply_position_and_span_to_edges(staff=voice, poses=pos_list_2, style=self.start_style_two, padding=10.7, command=r'\startTextSpanTwo', stop_command=r'\stopTextSpanTwo',ending_hook=self.stop_style_two)
            elif self.apply_list_two_to == 'ties':
                pos_list_2 = self._cyc_position_list_two_text
                for voice in abjad.select(selections).components(abjad.Voice):
                    self._apply_position_and_span_to_ties(staff=voice, poses=pos_list_2, style=self.start_style_two, padding=10.7, command=r'\startTextSpanTwo', stop_command=r'\stopTextSpanTwo',ending_hook=self.stop_style_two)
            else:
                pass
        if self.position_list_three != None:
            if self.apply_list_three_to == 'left_only':
                pos_list_3 = self._cyc_position_list_three_text
                for voice in abjad.select(selections).components(abjad.Voice):
                    self._apply_position_and_span_left_only(staff=voice, poses=pos_list_3, style=self.start_style_three, padding=13.2, command=r'\startTextSpanThree', stop_command=r'\stopTextSpanThree', ending_hook=self.stop_style_three)
            if self.apply_list_three_to == 'edges':
                pos_list_3 = self._cyc_position_list_three_text
                for voice in abjad.select(selections).components(abjad.Voice):
                    self._apply_position_and_span_to_edges(staff=voice, poses=pos_list_3, style=self.start_style_three, padding=13.2, command=r'\startTextSpanThree', stop_command=r'\stopTextSpanThree', ending_hook=self.stop_style_three)
            elif self.apply_list_three_to == 'ties':
                pos_list_3 = self._cyc_position_list_three_text
                for voice in abjad.select(selections).components(abjad.Voice):
                    self._apply_position_and_span_to_edges(staff=voice, poses=pos_list_3, style=self.start_style_three, padding=13.2, command=r'\startTextSpanThree', stop_command=r'\stopTextSpanThree', ending_hook=self.stop_style_three)
            else:
                pass
        return selections

    def _apply_position_and_span_to_edges(staff, poses, style, padding, command, stop_command, ending_hook,):
        position = next(poses)
        for run in abjad.select(staff).runs():
            start_span = abjad.StartTextSpan(
                command=command,
                left_text=abjad.Markup(position).upright(),
                style=style,
                )
            stop_span = abjad.StartTextSpan(
                command=command,
                right_padding=2,
                left_text=abjad.Markup(position).upright(),
                style=ending_hook,
                )
            abjad.tweak(start_span).staff_padding = padding
            abjad.attach(start_span, run[0])
            abjad.attach(abjad.StopTextSpan(command=stop_command,), run[-1])
            abjad.tweak(stop_span).staff_padding = padding
            abjad.attach(stop_span, run[-1])
        return selections

    def _apply_position_and_span_to_ties(staff, poses, style, padding, command, stop_command, ending_hook):
        position = next(poses)
        for run in abjad.select(staff).runs():
            abjad.attach(abjad.StopTextSpan(command=stop_command,), run[-1])
            abjad.tweak(stop_span).staff_padding = padding
            abjad.attach(stop_span, run[-1])
            for tie in abjad.select(run).logical_ties():
                start_span = abjad.StartTextSpan(
                    command=command,
                    left_text=abjad.Markup(position).upright(),
                    style=style,
                    )
                stop_span = abjad.StartTextSpan(
                    command=command,
                    right_padding=2,
                    left_text=abjad.Markup(position).upright(),
                    style=ending_hook,
                    )
                abjad.tweak(start_span).staff_padding = padding
                abjad.attach(start_span, tie[0])
        return selections

    def _apply_text_and_span_l_only(staff, poses, style, padding, command, stop_command, ending_hook):
        text = next(poses)
        for run in abjad.select(staff).runs():
            leaves = abjad.select(run).leaves()
            span = abjad.StartTextSpan(
                command=stop_command,
                right_padding=2.5,
                left_text=abjad.Markup(text).upright(),
                style=ending_hook,
                )
            abjad.text_spanner(leaves[0], start_text_span=span)
        return selections
