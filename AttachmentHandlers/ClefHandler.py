import abjad
from statistics import mean

# add shelf for ottava to ensure that no notes in the bracket are illegible
class ClefHandler:
    def __init__(
        self,
        clef=None,
        clef_shelf=None,
        allowable_clefs=None,
        add_extended_clefs=False,
        ottava_shelf=None,
        add_ottavas=False,
        extend_in_direction="up",
    ):
        self.clef = clef
        self.clef_shelf = clef_shelf
        self.allowable_clefs = allowable_clefs
        self.add_extended_clefs = add_extended_clefs
        self.ottava_shelf = ottava_shelf
        self.add_ottavas = add_ottavas
        self.extend_in_direction = extend_in_direction

    def __call__(self, voice):
        self._add_clefs(voice)

    def _extended_range_clefs(self, clef):
        clef_groups_up = {
            "bass": ("bass", "tenorvarC", "treble", "treble^8", "treble^15"),
            "tenor": ("tenorvarC", "treble", "treble^8", "treble^15"),
            "alto": ("varC", "treble", "treble^8", "treble^15"),
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
        default_clef_shelves = {"bass": (-28, 3), "tenor": (-21, 10), "tenorvarC": (-21, 10), "alto": (-12, 13), "varC": (-12, 13), "treble": (-5, 24), "treble^8": (7, 36), "treble^15": (19, 48)}
        return default_clef_shelves[clef]

    def _add_clefs(self, voice): #make sure if clef is a string or not
        clef = self.clef
        if clef is not None:
            first_clef_name = self._extended_range_clefs(clef)[0]
            clef_list = [abjad.Clef(first_clef_name)]
            abjad.attach(clef_list[0], abjad.select(voice).leaves()[0])
            if self.add_extended_clefs is True:
                if self.allowable_clefs is not None:
                    allowable_clefs = self.allowable_clefs
                else:
                    allowable_clefs = self._extended_range_clefs(clef)
                for tie in abjad.select(voice).logical_ties(pitched=True):
                    if abjad.inspect(tie[0]).indicator(abjad.Clef) is not None:
                        abjad.detach(abjad.inspect(tie[0]).indicator(abjad.Clef), tie[0])
                    pitches = []
                    for pitch in abjad.inspect(tie[0]).pitches():
                        pitches.append(pitch.number)
                    pitch = mean(pitches)
                    value = None
                    for count , clef in enumerate(allowable_clefs):
                        if clef_list[-1] == abjad.Clef(clef):
                            value = count
                    active_clef_in_list = clef_list[-1]
                    active_clef_in_list_shelf = self._extended_range_ottavas(clef_list[-1].name)
                    if pitch > active_clef_in_list_shelf[1]:
                        if value + 1 <= len(allowable_clefs):
                            temp_clef = allowable_clefs[value + 1]
                            clef = abjad.Clef(temp_clef)
                            if pitch > self._extended_range_ottavas(temp_clef)[1]:
                                if value + 2 <= len(allowable_clefs):
                                    temp_clef = allowable_clefs[value + 2]
                                    clef = abjad.Clef(temp_clef)
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue
                    elif pitch < active_clef_in_list_shelf[0]:
                        if value - 1 >= len(allowable_clefs):
                            temp_clef = allowable_clefs[value - 1]
                            clef = abjad.Clef(temp_clef)
                            if pitch < self._extended_range_ottavas(temp_clef)[0]:
                                if value - 2 >= len(allowable_clefs):
                                    temp_clef = allowable_clefs[value - 2]
                                    clef = abjad.Clef(temp_clef)
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                    if clef == clef_list[-1]:
                        continue
                    else:
                        print(clef)
                        abjad.attach(clef, tie[0])
                        clef_list.append(clef)
                        if clef == allowable_clefs[-1]:
                            self._add_ottavas(tie, clef)
            else:
                converted_clef = self._extended_range_clefs(clef)[0]
                clef = abjad.Clef(converted_clef)
                first_leaf = abjad.select(voice).leaves()[0]
                if abjad.inspect(first_leaf).indicator(abjad.Clef) is not None:
                    abjad.detach(abjad.inspect(first_leaf).indicator(abjad.Clef), first_leaf)
                    abjad.attach(clef, first_leaf)
                else:
                    abjad.attach(clef, first_leaf)
                self._add_ottavas(voice, clef.name)
        else:
            clef = abjad.Clef("treble")
            first_leaf = abjad.select(voice).leaves()[0]
            abjad.attach(clef, first_leaf)
            self._add_ottavas(voice, clef.name)

    def _add_ottavas(self, tie, active_clef):
        if self.add_ottavas is True:
            current_clef = active_clef
            if self.ottava_shelf is not None:
                shelf = self.ottava_shelf
                if self.extend_in_direction == "down":
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch < shelf:
                            abjad.ottava(
                                tie, start_ottava=abjad.Ottava(n=-1)
                            )
                else:
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(
                                tie, start_ottava=abjad.Ottava(n=1)
                            )
            else:
                shelf = self._extended_range_ottavas(current_clef)
                if self.extend_in_direction == "down":
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch < shelf:
                            abjad.ottava(
                                tie, start_ottava=abjad.Ottava(n=-1)
                            )
                else:
                    for pitch in abjad.inspect(tie[0]).pitches():
                        if pitch > shelf:
                            abjad.ottava(
                                tie, start_ottava=abjad.Ottava(n=1)
                            )
        else:
            pass
