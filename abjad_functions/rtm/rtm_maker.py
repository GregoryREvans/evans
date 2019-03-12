import abjad

class RTMMaker(object):

    def __init__(self, rtm, continuous=False):
        self.rtm = rtm
        self.continuous = continuous

    def __call__(self, divisions):
        return self._rtm_maker(divisions)

    @staticmethod
    def _rhythm_cell(duration, rtm):
        rtm_parser = abjad.rhythmtrees.RhythmTreeParser()
        selection = abjad.select(rtm_parser(rtm)[0](duration))
        for tuplet in abjad.select(selection).components(abjad.Tuplet):
            tuplet.normalize_multiplier()
        return selection

    def _rtm_maker(self, divisions):
        selections = []
        for division in divisions:
            selection = self._rhythm_cell(division, self.rtm)
            selections.append(selection)

        return selections


# rtm = '(1 (1 (4 (1 -1 1 -1 1))))'
# divisions = [abjad.Duration(n, 8) for n in (3, 4, 3, 4)]
# maker = RTMMaker(rtm=rtm)
# selections = maker(divisions)

# lilyfile = abjad.LilyPondFile.rhythm(
#     selections,
#     divisions
# )

# abjad.show(lilyfile)


class RTMMaker_2(object):

    def __init__(self, continuous=False):
        self.continuous = continuous

    def __call__(self, rtm_strings, divisions):
        return self._rtm_maker(rtm_strings, divisions)

    @staticmethod
    def _rhythm_cell(duration, rtm):
        rtm_parser = abjad.rhythmtrees.RhythmTreeParser()
        selection = abjad.select(rtm_parser(rtm)[0](duration))
        for tuplet in abjad.select(selection).components(abjad.Tuplet):
            tuplet.normalize_multiplier()
        return selection

    def _rtm_maker(self, rtm_strings, divisions):
        selections = []
        for rtm_string, division in zip(rtm_strings, divisions):
            selection = self._rhythm_cell(division, rtm_string)
            selections.append(selection)
        return selections



# maker = RTMMaker_2()
# rtms = [
#     '(1 (1 (4 (1 -1 1 -1 1))))',
#     '(1 (1 (1 (1 1 1))))',
#     '(1 (1 1 1 (2 (1 1 1)) 1 1))',
#     '(1 (1 1 1 1 1))',
# ]
# divisions = [abjad.Duration(n, 8).with_denominator(8) for n in (3, 4, 3, 4)]
# selections = maker(rtms, divisions)

# lilyfile = abjad.LilyPondFile.rhythm(
#     selections,
#     divisions
# )

# abjad.show(lilyfile)

class RTMMaker_3(object):

    def __init__(self, continuous=False):
        self.continuous = continuous

    def __call__(self, division_pairs):
        return self._rtm_maker(division_pairs)

    @staticmethod
    def _rhythm_cell(duration, rtm):
        rtm_parser = abjad.rhythmtrees.RhythmTreeParser()
        selection = abjad.select(rtm_parser(rtm)[0](duration))
        for tuplet in abjad.select(selection).components(abjad.Tuplet):
            tuplet.normalize_multiplier()
        return selection

    def _rtm_maker(self, division_pairs):
        selections = []
        for division, rtm_string in division_pairs:
            selection = self._rhythm_cell(division, rtm_string)
            selections.append(selection)
        return selections



# maker = RTMMaker_3()
# rtms = [
#     '(1 (1 (4 (1 -1 1 -1 1))))',
#     '(1 (1 (1 (1 1 1))))',
#     '(1 (1 1 1 (2 (1 1 1)) 1 1))',
#     '(1 (1 1 1 1 1))',
# ]
# divisions = [abjad.Duration(n, 8).with_denominator(8) for n in (3, 4, 3, 4)]
# pairs = zip(divisions, rtms)
# selections = maker(pairs)

# lilyfile = abjad.LilyPondFile.rhythm(
#     selections,
#     divisions
# )

# abjad.show(lilyfile)

class RTMMaker_4(object):

    def __init__(self, rtm, continuous=False):
        self.rtm = abjad.CyclicTuple(rtm)
        self.state = {
            'last index used' : 0
        }

    def __call__(self, divisions, previous_state=None):
        starting_index = -1

        if previous_state is not None:
            starting_index = previous_state['last index used'] + 1

        selections = self._rtm_maker(divisions, starting_index=starting_index)

        if previous_state is not None:
            self.state['last index used'] += len(selections)
            self.state['last index used'] %= len(self.rtm)

        return selections

    @staticmethod
    def _rhythm_cell(duration, rtm):
        rtm_parser = abjad.rhythmtrees.RhythmTreeParser()
        selection = abjad.select(rtm_parser(rtm)[0](duration))
        for tuplet in abjad.select(selection).components(abjad.Tuplet):
            tuplet.normalize_multiplier()
        return selection

    def _rtm_maker(self, divisions, starting_index=0):
        rtm = self.rtm[starting_index:starting_index + len(divisions)]

        selections = []
        for rtm_string, division in zip(rtm, divisions):
            selection = self._rhythm_cell(division, rtm_string)
            selections.append(selection)

        return selections



# # from Scores.onkos.Components.rtm_lists import final_rtm_list
# rtm = '(1 ((1 (1 1)) 1 (1 (1 1 1)) (1 (1 1)) 1))'
# maker = RTMMaker_4(rtm=rtm, continuous=True)
# # divisions = [abjad.Duration(n, 8).with_denominator(8) for n in (2, 4, 3, 4, 5, 3, 4, 2, 3, 5, 4, 3, 4, 2, 5)]
# divisions = [abjad.Duration(4, 4)]
# #divisions = [abjad.Duration(n, 8).with_denominator(8) for n in (4, 4, 4, 4, 4, 4, 4, 4, 4, 4)]
# # selections_1 = maker(divisions)
# # selections_2 = maker(divisions, previous_state=maker.state)
# # selections_2 = maker(divisions, previous_state=maker.state)
# selections = maker(divisions)
# lilyfile = abjad.LilyPondFile.rhythm(
#     selections,
#     divisions
# )
#
# abjad.show(lilyfile)
