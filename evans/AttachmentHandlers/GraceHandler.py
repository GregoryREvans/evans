import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class GraceHandler:
    def __init__(
        self,
        boolean_vector=None,
        gesture_lengths=None,
        continuous=False,
        vector_count=-1,
        gesture_count=-1,
        name="Grace Handler",
    ):
        self.continuous = continuous
        self._vector_count = vector_count
        self._gesture_count = gesture_count
        self.boolean_vector = boolean_vector
        self.gesture_lengths = gesture_lengths
        self._cyc_boolean_vector = CyclicList(boolean_vector, self.continuous, self._vector_count)
        self._cyc_gesture_lengths = CyclicList(gesture_lengths, self.continuous, self._gesture_count)
        self.name = name

    def __call__(self, selections):
        self._add_grace_notes(selections)

    def _add_grace_notes(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        vectors = self._cyc_boolean_vector(r=len(ties))
        if self.boolean_vector != None:
            for value, tie in zip(vectors, ties):
                if value == 1:
                    grace_list = ""
                    if self.gesture_lengths != None:
                        grace_length = self._cyc_gesture_lengths(r=1)[0]
                        for x in range(grace_length):
                            s = "c'16"
                            grace_list = grace_list + s
                            grace_list = grace_list + " "
                            grace_list = grace_list + "s8.."
                            grace_list = grace_list + " "
                        grace_list = grace_list + "s2"
                        grace = abjad.BeforeGraceContainer(grace_list, command=r"\acciaccatura")
                        if len(abjad.select(grace).leaves(pitched=True)) > 1:
                            abjad.beam(grace, beam_rests=True, beam_lone_notes=True, stemlet_length=0)
                            literal_slash = abjad.LilyPondLiteral(r"\slash", format_slot="before")
                            abjad.attach(literal_slash, abjad.select(grace).leaves(pitched=True)[0])
                            direction_override = abjad.LilyPondLiteral(
                                r"\override Stem.direction = #UP",
                                format_slot="before",
                                )
                            direction_revert = abjad.LilyPondLiteral(
                                r"\revert Stem.direction",
                                format_slot="after"
                                )
                            abjad.attach(direction_override, abjad.select(grace).leaves(pitched=True)[0])
                            abjad.attach(direction_revert, abjad.select(grace).leaves(pitched=True)[-1])
                        open_literal = abjad.LilyPondLiteral("\scaleDurations #'(1 . 1) {", format_slot="before")
                        close_literal = abjad.LilyPondLiteral("}", format_slot="after")
                        abjad.attach(open_literal, grace)
                        abjad.attach(close_literal, grace)
                        abjad.attach(grace, tie[0])
                    else:
                        grace = abjad.BeforeGraceContainer("c'16", command=r"\appoggiatura")
                        open_literal = abjad.LilyPondLiteral("\scaleDurations #'(1 . 1) {", format_slot="before")
                        close_literal = abjad.LilyPondLiteral("}", format_slot="after")
                        abjad.attach(open_literal, grace)
                        abjad.attach(close_literal, grace)
                        abjad.attach(grace, tie[0])
                else:
                    continue
        else:
            pass

    def name(self):
        return self.name

    def state(self):
        return f"""vector count\n{self._cyc_boolean_vector.state()}\ngesture count\n{self._cyc_gesture_lengths.state()}"""


###DEMO
# s = abjad.Staff("c'4 c'4 c'4 c'4")
# h = GraceHandler(
#     boolean_vector=[0, 1, 0, 1],
#     gesture_lengths=[1, 2],
#     continuous=True,
# )
# h(s[:])
# abjad.f(s)
