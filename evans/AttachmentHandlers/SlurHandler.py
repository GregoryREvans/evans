import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class SlurHandler:
    def __init__(self, apply_slur_to="runs", boolean_vector=[0], continuous=True):
        self.apply_slur_to = apply_slur_to
        self._count = -1
        self.continuous = continuous
        self.boolean_vector = CyclicList(boolean_vector, self.continuous, self._count)

    def __call__(self, selections):
        self.add_slurs(selections)

    def add_slurs(self, selections):
        if self.slurs == "selections":
            if self.boolean_vector(r=1)[0] is 0:
                abjad.slur(selections[:])
            else:
                continue
        elif self.slurs == "runs":
            for run in abjad.select(selections).runs():
                if self.boolean_vector(r=1)[0] is 0:
                    abjad.slur(run[:])
                else:
                    continue
        else:
            pass
