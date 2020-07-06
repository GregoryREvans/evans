import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class SlurHandler:
    r"""
    >>> staff = abjad.Staff("c'4 c'4 c'4 c'4")
    >>> handler = evans.SlurHandler()
    >>> handler(staff)
    >>> abjad.f(staff)
    \new Staff
    {
        c'4
        (
        c'4
        c'4
        c'4
        )
    }

    """

    def __init__(
        self,
        apply_slur_to="runs",
        boolean_vector=[1],
        continuous=True,
        count=-1,
        name="Slur Handler",
    ):
        self.apply_slur_to = apply_slur_to
        self._count = count
        self.continuous = continuous
        self.boolean_vector = CyclicList(boolean_vector, self.continuous, self._count)
        self.name = name

    def __call__(self, selections):
        self.add_slurs(selections)

    def add_slurs(self, selections):
        if self.apply_slur_to == "selections":
            if self.boolean_vector(r=1)[0] == 1:
                abjad.slur(selections[:])
            else:
                pass
        elif self.apply_slur_to == "runs":
            for run in abjad.select(selections).runs():
                if self.boolean_vector(r=1)[0] == 1:
                    abjad.slur(run[:])
                else:
                    continue
        else:
            pass

    def name(self):
        return self.name

    def state(self):
        return abjad.OrderedDict([("count", self.boolean_vector.state())])
