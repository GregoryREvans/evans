import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class BendHandler:
    def __init__(self, bend_amounts=[1], bend_continuous=True, boolean_vector=[0], vector_continuous=True):
        self._bend_count = -1
        self._vector_count = -1
        self.bend_continuous = bend_continuous
        self.vector_continuous = vector_continuous
        self.bend_amounts = CyclicList(bend_amounts, self.bend_continuous, self._bend_count)
        self.boolean_vector = CyclicList(boolean_vector, self.vector_continuous, self._vector_count)

    def __call__(self, selections):
        self.add_bend(selections)

    def add_bend(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        vector = self.boolean_vector(r=len(ties))
        amounts = self.bend_amounts(r=len(ties))
        for tie, bool, amount in zip(ties, vector, amounts):
            if bool is 0:
                abjad.attach(abjad.BendAfter(amount), tie[-1])
            else:
                continue
