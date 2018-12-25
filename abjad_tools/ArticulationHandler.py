import abjad

class ArticulationHandler:

    def __init__(
        self,
        articulation_list=None,
        text_list=None,
        ):
        def cyc(lst):
            count = 0
            while True:
                yield lst[count%len(lst)]
                count += 1
        self.articulation_list = articulation_list
        self._cyc_articulations = cyc(articulation_list)

    def __call__(self, selections):
        return self.add_articulations(selections)

    def add_articulations(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        for tie in ties:
            if len(tie) == 1:
                if self.articulation_list != None:
                    articulation = self._cyc_articulations
                    abjad.attach(abjad.Articulation(next(articulation)), tie[0])
        return selections
