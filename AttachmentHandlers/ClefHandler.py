import abjad
from statistics import mean


class ClefHandler:
    def __init__(
        self,
        clef=None,
        clef_shelf=None,
        add_extended_clefs=False,
        ottava_shelf=None,
        add_ottavas=False,
        extend_in_direction="up",
    ):
        self.clef = clef
        self.clef_shelf = clef_shelf
        self.add_extended_clefs = add_extended_clefs
        self.ottava_shelf = ottava_shelf
        self.add_ottavas = add_ottavas
        self.extend_in_direction = extend_in_direction

    def __call__(self, voice):
        self._add_clefs(voice)

    def _extended_range_clefs(self, clef):
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
        if self.extend_in_direction == "down":
            return clef_groups_down[clef]
        else:
            return clef_groups_up[clef]

    def _extended_range_ottavas(self, clef):
        default_clef_shelves_up = {"bass": 3, "tenor": 10, "tenorvarC": 10, "alto": 13, "varC": 13, "treble": 24} #in some cases treble might be 36?
        default_clef_shelves_down = {"bass": -28, "tenor": -21, "tenorvarC": -21, "alto": -12, "varC": -12, "treble": -5}
        if self.extend_in_direction == "down":
            return default_clef_shelves_down[clef]
        else:
            return default_clef_shelves_up[clef]

    def _add_clefs(self, voice):
        clef = self.clef
        if clef is not None:
            clef_list = [abjad.Clef(self._extended_range_clefs(clef)[0])]
            abjad.attach(clef_list[0], voice[0])
            if self.add_extended_clefs is True:
                clefs = self._extended_range_clefs(clef)
                for run in abjad.select(voice).runs():
                    ties = abjad.select(run).logical_ties(pitched=True)
                    pitches = []
                    for tie in ties:
                        for pitch in abjad.inspect(tie[0]).pitches():
                            pitches.append(pitch.number)
                    average = mean(pitches)
                    if average > self._extended_range_ottavas(clefs[0]):
                        if average > self._extended_range_ottavas(clefs[1]):
                            clef = abjad.Clef(clefs[2])
                            if clef != clef_list[-1]:
                                abjad.attach(clef, run[0])
                                clef_list.append(clef)
                            else:
                                pass
                        else:
                            clef = abjad.Clef(clefs[1])
                            if clef != clef_list[-1]:
                                abjad.attach(clef, run[0])
                                clef_list.append(clef)
                            else:
                                pass
                    else:
                        clef = abjad.Clef(clefs[0])
                        if clef != clef_list[-1]:
                            abjad.attach(clef, run[0])
                            clef_list.append(clef)
                        else:
                            pass
                    self._add_ottavas(run, clef.name)
                clef_list.append(clef)
            else:
                converted_clef = self._extended_range_clefs(clef)[0]
                clef = abjad.Clef(converted_clef)
                first_leaf = abjad.select(voice).leaves()[0]
                abjad.attach(clef, first_leaf)
                self._add_ottavas(voice, clef.name)
        else:
            clef = abjad.Clef("treble")
            first_leaf = abjad.select(voice).leaves()[0]
            abjad.attach(clef, first_leaf)
            self._add_ottavas(voice, clef.name)

    def _add_ottavas(self, voice, active_clef):
        if self.add_ottavas is True:
            current_clef = active_clef
            if self.ottava_shelf is not None:
                shelf = self.ottava_shelf
                if self.extend_in_direction == "down":
                    for run in abjad.select(voice).runs():
                        for tie in abjad.select(run).logical_ties(pitched=True):
                            for pitch in abjad.inspect(tie[0]).pitches():
                                if pitch < shelf:
                                    abjad.ottava(
                                        tie, start_ottava=abjad.Ottava(n=-1)
                                    )
                else:
                    for run in abjad.select(voice).runs():
                        for tie in abjad.select(run).logical_ties(pitched=True):
                            for pitch in abjad.inspect(tie[0]).pitches():
                                if pitch > shelf:
                                    abjad.ottava(
                                        tie, start_ottava=abjad.Ottava(n=1)
                                    )
            else:
                shelf = self._extended_range_ottavas(current_clef)
                if self.extend_in_direction == "down":
                    for run in abjad.select(voice).runs():
                        for tie in abjad.select(run).logical_ties(pitched=True):
                            for pitch in abjad.inspect(tie[0]).pitches():
                                if pitch < shelf:
                                    abjad.ottava(
                                        tie, start_ottava=abjad.Ottava(n=-1)
                                    )
                else:
                    for run in abjad.select(voice).runs():
                        for tie in abjad.select(run).logical_ties(pitched=True):
                            for pitch in abjad.inspect(tie[0]).pitches():
                                if pitch > shelf:
                                    abjad.ottava(
                                        tie, start_ottava=abjad.Ottava(n=1)
                                    )
        else:
            pass
