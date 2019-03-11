import abjad

class GraceHandler:

    def __init__(
        self,
        boolean_vector=None,
        gesture_lengths=None,
        continuous=False,
        ):
        def cyc(lst):
            if self.continuous == False:
                self._count = 0
            while True:
                yield lst[self._count % len(lst)]
                self._count += 1
        self.boolean_vector = boolean_vector
        self.gesture_lengths = gesture_lengths
        self.continuous = continuous
        self._cyc_boolean_vector = cyc(boolean_vector)
        self._cyc_gesture_lengths = cyc(gesture_lengths)
        self._count = 0

    def __call__(self, selections):
        return self._add_grace_notes(selections)

    def _add_grace_notes(self, selections):
        container = abjad.Container()
        container.extend(selections)
        if self.boolean_vector != None:
            for run in abjad.select(container).runs():
                ties = abjad.select(run).logical_ties()
                vector_values = [next(self._cyc_boolean_vector) for _ in ties]
                for value, tie in zip(vector_values, ties):
                    if value == 1:
                        grace_list = []
                        if self.gesture_lengths != None:
                            grace_length = next(self._cyc_gesture_lengths)
                            for x in range(0, grace_length):
                                note = abjad.Note("c'16")
                                grace_list.append(note)
                            grace = abjad.AfterGraceContainer(grace_list)
                            literal = abjad.LilyPondLiteral('#(define afterGraceFraction (cons 15 16))')
                            if len(tie) > 1:
                                abjad.attach(literal, tie[-2])
                                abjad.attach(grace, tie[-1])
                            else:
                                abjad.attach(literal, tie[0])
                                abjad.attach(grace, tie[0])
                        else:
                            grace = abjad.AfterGraceContainer(abjad.Note("c'16"))
                            literal = abjad.LilyPondLiteral('#(define afterGraceFraction (cons 15 16))')
                            if len(tie) > 1:
                                abjad.attach(literal, tie[-2])
                                abjad.attach(grace, tie[-1])
                            else:
                                abjad.attach(literal, tie[0])
                                abjad.attach(grace, tie[0])
                    else:
                        continue
        else:
            pass
        return [container[:]]
