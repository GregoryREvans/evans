import abjad

clef_groups_up = {
    "bass": ("bass", "tenorvarC", "treble"),
    "tenor": ("tenorvarC", "treble", "treble^8"),
    "alto": ("varC", "treble", "treble^8"),
    "treble": ("treble", "treble^8", "treble^15"),
}

clef_groups_down = {
    "bass": ("bass", "bass_8", "bass_15"),
    "tenor": ("tenorvarC", "bass", "bass_8"),
    "alto": ("varC", "bass", "bass_8"),
    "treble": ("treble", "treble_8", "bass"),
}

default_clef_shelves_up = {"bass": 3, "tenor": 10, "alto": 13, "treble": 36}

default_clef_shelves_down = {"bass": -28, "tenor": -21, "alto": -12, "treble": -5}


class ClefHandler:
    def __init__(
        self,
        clef=None,
        clef_shelf=None,
        add_extended_clefs=False,
        ottava_shelf=None,
        ottava_number=1,
        add_ottavas=False,
        extend_in_direction="up",
    ):
        self.clef = clef
        self.clef_shelf = clef_shelf
        self.add_extended_clefs = add_extended_clefs
        self.ottava_shelf = ottava_shelf
        self.ottava_number = ottava_number
        self.add_ottavas = add_ottavas
        self.extend_in_direction = extend_in_direction

    def __call__(self, voice):
        self._add_clefs(voice)
        if self.add_ottavas is not False:
            self._add_ottavas(voice)

    def _extended_range_clefs(self, clef):
        if self.extend_in_direction == "down":
            return clef_groups_down[clef]
        else:
            return clef_groups_up[clef]

    def _extended_range_ottavas(self, clef):
        if self.extend_in_direction == "down":
            return default_clef_shelves_down[clef]
        else:
            return default_clef_shelves_up[clef]

    def _add_clefs(self, voice):
        clef = self.clef
        if clef is not None:
            if self.add_extended_clefs is True:
                # clefs = _extended_range_clefs(clef)
                for run in abjad.select(voice).runs():  # for now
                    clef = abjad.Clef().from_selection(run)
                    abjad.attach(clef, run[0])
            else:
                clef = abjad.Clef(self.clef)
                first_leaf = abjad.select(voice).leaves()[0]
                abjad.attach(clef, first_leaf)
            self._add_ottavas(voice)
        else:
            print("CLEF INPUT REQUIRED: got NONE type")
            pass

    def _add_ottavas(self, voice):  # needs to consider what clef is active
        if self.ottava_shelf is not None:
            shelf = self.ottava_shelf
            for run in abjad.select(voice).runs():
                for tie in abjad.select(run).logical_ties(pitched=True):
                    for pitch in abjad.select(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(
                                tie, start_ottava=abjad.Ottava(n=self.ottava_number)
                            )
        else:
            shelf = self._extended_range_ottavas(self.clef)
            for run in abjad.select(voice).runs():
                for tie in abjad.select(run).logical_ties(pitched=True):
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(
                                tie, start_ottava=abjad.Ottava(n=self.ottava_number)
                            )
