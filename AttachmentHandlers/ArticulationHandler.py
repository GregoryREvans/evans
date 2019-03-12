import abjad

class ArticulationHandler:

    def __init__(
        self,
        articulation_list=None,
        continuous=False,
        ):
        def cyc(lst):
            if self.continuous == False:
                self._count = 0
            while True:
                yield lst[self._count % len(lst)]
                self._count += 1
        self.articulation_list = articulation_list
        self.continuous = continuous
        self._cyc_articulations = cyc(articulation_list)
        self._count = 0

    def __call__(self, selections):
        return self.add_articulations(selections)

    def add_articulations(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        for tie in ties:
            if self.articulation_list != None:
                articulation = self._cyc_articulations
                articulation = next(articulation)
                if articulation == 'tremolo':
                    for leaf in tie:
                        if abjad.inspect(leaf).duration() <= abjad.Duration(1, 32):
                            continue
                        else:
                            abjad.attach(abjad.StemTremolo(32), leaf)
                else:
                    abjad.attach(abjad.Articulation(articulation), tie[0])
        return selections
