import abjad

class SlurHandler:

    def __init__(
        self,
        tie_repeated_notes=False,
        slurs=False,
        phrasing_slurs=False,
        ):
        self.tie_repeated_notes = tie_repeated_notes
        self.slurs = slurs
        self.phrasing_slurs = phrasing_slurs

    def __call__(self, selections):
        return self.add_slurs(selections)

    def add_slurs(self, selections):
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
