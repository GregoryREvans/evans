import abjad

class NoteheadHandler:

    def __init__(
        self,
        notehead_list=None,
        continuous=False,
        ):
        def cyc(lst):
            if self.continuous == False:
                self._count = 0
            while True:
                yield lst[self._count % len(lst)]
                self._count += 1
        self.notehead_list = notehead_list
        self.continuous = continuous
        self._cyc_noteheads = cyc(notehead_list)
        self._count = 0

    def __call__(self, selections):
        return self.add_noteheads(selections)

    def add_noteheads(self, selections):
        if self.notehead_list != None:
            head = self._cyc_noteheads
            for tie in abjad.select(selections).logical_ties(pitched=True):
                head_name = next(head)
                string = str(r"""\once \override Staff.NoteHead.style = #'""")
                full_string = string + head_name
                style = abjad.LilyPondLiteral(full_string, format_slot='before',)
                for leaf in abjad.select(tie).leaves(pitched=True):
                    abjad.attach(style, leaf)
        return selections
