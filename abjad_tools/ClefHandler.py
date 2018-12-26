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
        for run in abjad.select(selections).runs():
            leaves = abjad.select(run).leaves(pitched=True)
            if self.clef != None:
                abjad.attach(abjad.Clef(self.clef), leaves[0]) #doesn't seem to always work
        return selections
