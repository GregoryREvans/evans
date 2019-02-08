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
            ties = abjad.select(run).logical_ties(pitched=True)
            if self.clef != None:
                abjad.attach(abjad.Clef(self.clef), ties[0][0])
        if self.add_ottavas == True:
            self._add_ottavas(selections)
        return selections

    def _add_ottavas(self, selections):
        if self.clef == 'treble':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for tie in abjad.select(selections).logical_ties():
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
            else:
                shelf = 36
                for tie in abjad.select(selections).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
        if self.clef == 'alto':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for tie in abjad.select(selections).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
            else:
                shelf = 13
                for tie in abjad.select(selections).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
        if self.clef == 'varC':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for tie in abjad.select(selections).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
            else:
                shelf = 13
                for tie in abjad.select(selections).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
        if self.clef == 'tenor':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for tie in abjad.select(selections).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
            else:
                shelf = 10
                for tie in abjad.select(selections).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
        if self.clef == 'tenorvarC':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for tie in abjad.select(selections).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
            else:
                shelf = 10
                for tie in abjad.select(selections).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
        if self.clef == 'bass':
            if self.ottava_shelf != None:
                shelf = self.ottava_shelf
                for tie in abjad.select(selections).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
            else:
                shelf = 3
                for tie in abjad.select(selections).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(tie)
        return(selections)
