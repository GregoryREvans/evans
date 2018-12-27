import abjad

class SlurHandler:

    def __init__(
        self,
        slurs=None,
        ):
        self.slurs = slurs

    def __call__(self, selections):
        return self.add_slurs(selections)

    def add_slurs(self, selections):
        if self.slurs == 'selections':
            abjad.slur(selections[:])
        elif self.slurs == 'runs':
            for run in abjad.select(selections).runs():
                abjad.slur(run[:])
        else:
            pass
        return selections
