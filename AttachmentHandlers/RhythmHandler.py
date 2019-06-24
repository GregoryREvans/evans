import abjad

class RhythmHandler:
    def __init__(
        self,
        rmaker,
        continuous=False,
        state=None,
    ):
        self.rmaker = rmaker
        self.continuous = continuous
        self.state = self.rmaker.state

    def __call__(self, durations):
        return self._make_music(durations)

    def _make_basic_rhythm(self, durations):
        if self.continuous == True:
            selections = self.rmaker(durations, previous_state=self.rmaker.state)
            self.state = self.rmaker.state
        else:
            selections = self.rmaker(durations, )
        return selections

    def _make_music(self, durations):
        selections = self._make_basic_rhythm(durations)
        # if self.pitch_handler == None:
        #     start_command = abjad.LilyPondLiteral(
        #         r'\stopStaff \once \override Staff.StaffSymbol.line-count = #1 \startStaff',
        #         format_slot='before',
        #         )
        #     stop_command = abjad.LilyPondLiteral(
        #         r'\stopStaff \startStaff',
        #         format_slot='after',
        #         )
        #     literal = abjad.LilyPondLiteral(r'\once \override Staff.Clef.transparent = ##t', 'before')
        #     c_clef = abjad.LilyPondLiteral(r'\clef alto', 'before')
        #     abjad.attach(literal, selections[0][0])
        #     abjad.attach(c_clef, selections[0][0])
        #     abjad.attach(start_command, selections[0][0])
        #     abjad.attach(stop_command, selections[0][-1])
        # if self.grace_handler != None:
        #     selections = self.grace_handler(selections)
        return selections
