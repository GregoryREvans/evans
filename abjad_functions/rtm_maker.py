import abjad

class RTMMaker:

    def __init__(
        self,
        rtm='(1 1 1 1)',
        previous_state=[],
        duration=abjad.Duration(1, 4),
        state=[],
        ):
        self.rtm = rtm
        self.previous_state = state
        self.duration = duration
        self.state = state

    def __call__(self, durations):
            return self.rtm_maker(durations, self.rtm, self.state)

    def rhythm_cell(rtm, duration):
        rtm_parser = abjad.rhythmtrees.RhythmTreeParser()
        selection = abjad.select(rtm_parser(rtm)[0](duration))
        for tuplet in abjad.select(selection).components(abjad.Tuplet):
            tuplet.normalize_multiplier()
        return selection

    def rtm_maker(duration, cell_string, state):
        state = []
        cell = lambda duration: self.rhythm_cell(rtm=cell_string, duration=duration)
        return cell
