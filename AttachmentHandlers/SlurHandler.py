import abjad

class SlurHandler:

    def __init__(
        self,
        attach_to=None,
        tie_repeated_notes=False,
        slurs=False,
        phrasing_slurs=False,
        ):
        self.attach_to = attach_to
        self.tie_repeated_notes = tie_repeated_notes
        self.slurs = slurs
        self.phrasing_slurs = phrasing_slurs

    def __call__(self, selections):
        return self.add_slurs(selections)

    def add_slurs(self, selections):
        if self.attach_to == 'selections':
            if self.tie_repeated_notes != False:
                    abjad.tie(selections[:])
            if self.slurs != False:
                    abjad.slur(selections[:])
            if self.phrasing_slurs != False:
                    abjad.phrasing_slur(selections[:])
        elif self.attach_to == 'runs':
            if self.tie_repeated_notes != False:
                for run in abjad.select(selections).runs():
                    abjad.tie(run[:])
            if self.slurs != False:
                for run in abjad.select(selections).runs():
                    abjad.slur(run[:])
            if self.phrasing_slurs != False:
                for run in abjad.select(selections).runs():
                    abjad.phrasing_slur(run[:])
        else:
            pass
        return selections
