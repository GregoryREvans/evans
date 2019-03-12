###THIS WORKFLOW FUNCTIONS###
# import abjad
# from abjadext import rmakers
# import evans.abjad_functions.talea_timespan.timespan_functions
#
#
# def rhythm_cell(duration, rtm):
#     rtm_parser = abjad.rhythmtrees.RhythmTreeParser()
#     selection = abjad.select(rtm_parser(rtm)[0](duration))
#     for tuplet in abjad.select(selection).components(abjad.Tuplet):
#         tuplet.normalize_multiplier()
#     return selection
#
# def conversion(rtm_type, duration_type):
#     rtm = rtm_type
#     rmodel_one = lambda duration: rhythm_cell(duration, rtm)
#     duration_one = duration_type
#     list = [(rmodel_one, duration_one)]
#     for rmodel, duration in list:
#         container = abjad.Container([])
#         durations = [duration]
#         selections = rmodel(durations)
#         container.extend(selections)
#         specifier = rmakers.BeamSpecifier(beam_each_division=True, beam_rests=True)
#         specifier(abjad.select(container))
#         voice = abjad.Voice()
#         voice.append(container)
#         abjad.show(voice)
#
# rtm = '(1 (1 (4 (1 -1 1 -1 1))))'
# duration_one = abjad.Duration(4, 4)
# conversion(rtm_type=rtm, duration_type=duration_one)

###THIS WORKFLOW IS IN PROGRESS###
import abjad
from abjadext import rmakers
import evans.abjad_functions.talea_timespan.timespan_functions

class RTMMaker:

    def __init__(
        self,
        rtm='(1 1 1 1)',
        previous_state=[],
        duration=abjad.Duration(1, 4),
        state=[],
        continuous=False,
        ):
        def cyc(lst):
            if self.continuous == False:
                self._count = 0
            while True:
                yield lst[self._count % len(lst)]
                self._count += 1
        self.rtm = rtm
        self.previous_state = state
        self.duration = duration
        self.state = state
        self.continuous = continuous
        self._count = 0

    def __call__(self, rtm_type, duration_type):
            return self._rtm_maker(duration, self.rtm, self.previous_state)

    def _rhythm_cell(self, duration, rtm):
        rtm_parser = abjad.rhythmtrees.RhythmTreeParser()
        selection = abjad.select(rtm_parser(rtm)[0](duration))
        for tuplet in abjad.select(selection).components(abjad.Tuplet):
            tuplet.normalize_multiplier()
        return selection

    def _rtm_maker(self, rtm_type, duration_type):
        rtm = rtm_type
        rmodel_one = lambda duration: self._rhythm_cell(duration, rtm)
        duration_one = duration_type
        list_ = [(rmodel_one, duration_one)]
        for rmodel, duration in list_:
            container = abjad.Container([])
            durations = [duration]
            selections = rmodel(durations)
            container.extend(selections)
            specifier = rmakers.BeamSpecifier(beam_each_division=True, beam_rests=True)
            specifier(abjad.select(container))
            # voice = abjad.Voice()
            # voice.append(container)
            # abjad.show(voice)
            selections = abjad.select(container)
        return selections


# rtm = '(1 (1 (4 (1 -1 1 -1 1))))'
# rtm = '(1 ((1 (1 1)) 1 (1 (1 1 1)) (1 (1 1))1 ))'
duration_one = abjad.Duration(4, 4)
staff = abjad.Staff()
maker = RTMMaker()
staff.extend(maker(rtm=rtm, duration=duration_one))
abjad.show(staff)
