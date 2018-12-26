import abjad

class ClefHandler:

    def __init__(
        self,
        clef=None,
        ottava_shelf=None,
        add_ottavas=False,
        ):
        self.clef = clef
        self.ottava_shelf = ottava_shelf
        self.add_ottavas = add_ottavas

    def __call__(self, selections):
        return self.add_clef(selections)

    def add_clef(self, selections):
        for run in abjad.select(selections).runs():
            leaves = abjad.select(run).leaves(pitched=True)
            if self.clef != None:
                abjad.attach(abjad.Clef(self.clef), leaves[0])
        if self.add_ottavas == True:
            self._add_ottavas(selections)
        return selections

    def _add_ottavas(self, selections):
        if self.clef == 'treble':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
            else:
                shelf = 36
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
        if self.clef == 'alto':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
            else:
                shelf = 13
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
        if self.clef == 'varC':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
            else:
                shelf = 13
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
        if self.clef == 'tenor':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
            else:
                shelf = 10
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
        if self.clef == 'tenorvarC':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
            else:
                shelf = 10
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
        if self.clef == 'bass':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
            else:
                shelf = 3
                for note in abjad.select(selections).leaves():
                    for pitch in abjad.inspect(note).pitches():
                        if pitch > shelf:
                            abjad.ottava(note)
        return(selections)
