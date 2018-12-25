import abjad

class ClefHandler:

    def __init__(
        self,
        clef=None,
        ):
        self.clef = clef

    def __call__(self, selections):
        return self.add_clef(selections)

    def add_clef(self, selections):
        runs = abjad.select(selections).runs()
        ties = abjad.select(runs).logical_ties(pitched=True)
        if self.clef != None:
            abjad.attach(abjad.Clef(self.clef), ties[0][0]) #doesn't seem to always work
