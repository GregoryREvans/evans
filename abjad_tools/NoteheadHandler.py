import abjad

class NoteheadHandler:

    def __init__(
        self,
        notehead_list=None,
        ):
        def cyc(lst):
            count = 0
            while True:
                yield lst[count%len(lst)]
                count += 1
        self.notehead_list = notehead_list
        self._cyc_noteheads = cyc(notehead_list)

    def __call__(self, selections):
        return self.add_noteheads(selections)

    def add_noteheads(self, selections):
        if self.notehead_list != None:
            ties = abjad.select(selections).logical_ties(pitched=True)
            head = self._cyc_noteheads
            next_style = next(head)
            for tie in ties:
                if next_style == 'harmonic':
                    for leaf in tie:
                        string = str(r"""\once \override Staff.NoteHead.style = #'harmonic-mixed""")
                        style = abjad.LilyPondLiteral(string, format_slot='before',)
                        abjad.attach(style, leaf)
                elif next_style == 'half-harmonic':
                    for leaf in tie:
                        string = str(r"""\once \override Staff.NoteHead.style = #'diamond""")
                        style = abjad.LilyPondLiteral(string, format_slot='before',)
                        abjad.attach(style, leaf)
                elif next_style == 'cross':
                    for leaf in tie:
                        string = str(r"""\once \override Staff.NoteHead.style = #'cross""")
                        style = abjad.LilyPondLiteral(string, format_slot='before',)
                        abjad.attach(style, leaf)
                elif next_style == 'scratch':
                    for leaf in tie:
                        string = str(r"""\once \override Staff.NoteHead.style = #'triangle""")
                        style = abjad.LilyPondLiteral(string, format_slot='before',)
                        abjad.attach(style, leaf)
                elif next_style == 'subtone':
                    for leaf in tie:
                        string = str(r"""\once \override Staff.NoteHead.style = #'slash""")
                        style = abjad.LilyPondLiteral(string, format_slot='before',)
                        abjad.attach(style, leaf)
                else:
                    for leaf in tie:
                        string = str(r"""\once \override Staff.NoteHead.style = #'default""")
                        style = abjad.LilyPondLiteral(string, format_slot='before',)
                        abjad.attach(style, leaf)
        return selections
