import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class NoteheadHandler:
    def __init__(
        self,
        notehead_list=None,
        transition=False,
        head_boolean_vector=[0],
        head_vector_continuous=True,
        transition_boolean_vector=[0],
        transition_vector_continuous=True,
        continuous=False,
        count=-1,
        name="Notehead Handler",
    ):
        self.notehead_list = notehead_list
        self.transition = transition
        self.head_vector_continuous = head_vector_continuous
        self._head_vector_count = -1
        self.head_boolean_vector = CyclicList(
            head_boolean_vector, self.head_vector_continuous, self._head_vector_count
        )
        self.transition_vector_continuous = transition_vector_continuous
        self._transition_vector_count = -1
        self.transition_boolean_vector = CyclicList(
            transition_boolean_vector,
            self.transition_vector_continuous,
            self._transition_vector_count,
        )
        self.continuous = continuous
        self._count = count
        self._cyc_noteheads = CyclicList(notehead_list, self.continuous, self._count)
        self.name = name

    def __call__(self, selections):
        self.add_noteheads(selections)

    def add_noteheads(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        heads = self._cyc_noteheads(r=len(ties))
        head_vector = self.head_boolean_vector(r=len(ties))
        trans_vector = self.transition_boolean_vector(r=len(ties))
        if self.notehead_list is not None:
            for tie, head, bool in zip(ties, heads, head_vector):
                string = str(r"""\tweak NoteHead.style #'""")
                full_string = string + head
                style = abjad.LilyPondLiteral(full_string, format_slot="before")
                if bool == 1:
                    for leaf in abjad.select(tie).leaves(pitched=True):
                        abjad.attach(style, leaf)
                else:
                    continue
        if self.transition is True:
            transition_arrow = abjad.LilyPondLiteral(
                r"""
                - \tweak arrow-length #2
                - \tweak arrow-width #0.5
                - \tweak bound-details.right.arrow ##t
                - \tweak thickness #2.5
                \glissando
            """,
                "absolute_after",
            )
            for tie, bool1, bool2 in zip(
                ties, head_vector, trans_vector
            ):  # verify that heads are different?
                if bool1 == 1:
                    if bool2 == 1:
                        abjad.attach(transition_arrow, tie[-1])
                    else:
                        continue
                else:
                    continue
            for run in abjad.select(selections).runs():
                last_tie = abjad.select(run).logical_ties(pitched=True)[-1]
                abjad.detach(transition_arrow, last_tie[-1])

    def name(self):
        return self.name

    def state(self):
        return f"""count\n{self._cyc_noteheads.state()}\nhead vector count\n{self.head_boolean_vector.state()}\ntransition vector count\n{self.transition_boolean_vector.state()}"""


# - \tweak arrow-length #2
# - \tweak arrow-width #0.5
# - \tweak bound-details.right.arrow ##t
# - \tweak thickness #3
# \glissando
