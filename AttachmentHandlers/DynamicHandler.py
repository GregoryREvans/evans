import abjad
from CyclicList import CyclicList

# add "effort BV" and "sfz BV"
class DynamicHandler:
    def __init__(
        self,
        dynamic_list=None,
        flare_boolean_vector=None,
        hold_first_boolean_vector=None,
        hold_last_boolean_vector=None,
        effort_boolean_vector=None,
        sfx_boolean_vector=None,
        continuous=True,
    ):
        self.dynamic_list = dynamic_list
        self.flare_boolean_vector = flare_boolean_vector
        self.hold_first_boolean_vector = hold_first_boolean_vector
        self.hold_last_boolean_vector = hold_last_boolean_vector
        self.effort_boolean_vector = effort_boolean_vector
        self.continuous = continuous
        self._count_1 = -1
        self._count_2 = -1
        self._count_3 = -1
        self._count_4 = -1
        self._count_5 = -1
        self._cyc_dynamics = CyclicList(dynamic_list, self.continuous, self._count_1)
        self._cyc_flare_boolean_vector = CyclicList(
            flare_boolean_vector, self.continuous, self._count_2
        )
        self._cyc_hold_first_boolean_vector = CyclicList(
            hold_first_boolean_vector, self.continuous, self._count_3
        )
        self._cyc_hold_last_boolean_vector = CyclicList(
            hold_last_boolean_vector, self.continuous, self._count_4
        )
        self._cyc_effort_boolean_vector = CyclicList(
            effort_boolean_vector, self.continuous, self._count_5
        )

    def __call__(self, selections):
        return self._apply_dynamics(selections)

    def _calculate_hairpin(self, start, stop, flared=False):
        if isinstance(start, str):
            start = abjad.Dynamic(start)
        elif isinstance(start, int):
            start = abjad.Dynamic(abjad.Dynamic.dynamic_ordinal_to_dynamic_name(start))
        else:
            pass
        if isinstance(stop, str):
            stop = abjad.Dynamic(stop)
        elif isinstance(stop, int):
            stop = abjad.Dynamic(abjad.Dynamic.dynamic_ordinal_to_dynamic_name(stop))
        else:
            pass
        if flared is True:
            if start.ordinal < stop.ordinal:
                if start.name == "niente":
                    hairpin = "o<|"
                else:
                    hairpin = "<|"
            else:
                if stop.name == "niente":
                    stop = abjad.Dynamic("niente", hide=True)
                    hairpin = "|>o"
                else:
                    hairpin = "|>"
        else:
            if start.ordinal < stop.ordinal:
                if start.name == "niente":
                    hairpin = "o<"
                else:
                    hairpin = "<"
            else:
                if stop.name == "niente":
                    hairpin = ">o"
                else:
                    hairpin = ">"
        return hairpin

    def _apply_dynamics(self, selections):
        for run in abjad.select(selections).runs():
            hold_first = self._cyc_hold_first_boolean_vector(r=1)[0]
            if hold_first is False:
                if len(run) > 1:
                    if abjad.inspect(run[0]).has_indicator(abjad.Dynamic):
                        current_dynamic = abjad.inspect(run[0]).indicator(abjad.Dynamic)
                        start = abjad.Dynamic(current_dynamic, hide=True)
                        stop = self._cyc_dynamics(r=1)[0]
                    else:
                        items = self._cyc_dynamics(r=2)
                        start = items[0]
                        stop = items[1]
                    hairpin = abjad.StartHairpin(
                        self._calculate_hairpin(
                            start, stop, flared=self._cyc_flare_boolean_vector
                        )
                    )
                    hold_last = self._cyc_hold_last_boolean_vector(r=1)
                    if isinstance(start, str):
                        start = abjad.Dynamic(start)
                    elif isinstance(start, int):
                        start = abjad.Dynamic(
                            abjad.Dynamic.dynamic_ordinal_to_dynamic_name(start)
                        )
                    else:
                        pass
                    if isinstance(stop, str):
                        stop = abjad.Dynamic(stop)
                    elif isinstance(stop, int):
                        stop = abjad.Dynamic(
                            abjad.Dynamic.dynamic_ordinal_to_dynamic_name(stop)
                        )
                    else:
                        pass
                    if start.name == "niente":
                        start = abjad.Dynamic("niente", hide=True)
                    else:
                        pass
                    if stop.name == "niente":
                        stop = abjad.Dynamic("niente", hide=True)
                    if hold_last is True:
                        if stop.name != "niente":
                            abjad.attach(abjad.StartHairpin("--"), run[-1])
                            abjad.attach(
                                abjad.StopHairpin(), abjad.inspect(run[-1]).leaf(1)
                            )
                        else:
                            if isinstance(abjad.inspect(run[-1]).leaf(1), abjad.Rest):
                                stop = abjad.Dynamic(stop, command="\!", leak=True)
                            else:
                                pass
                    else:
                        if isinstance(abjad.inspect(run[-1]).leaf(1), abjad.Rest):
                            stop = abjad.Dynamic(stop, leak=True)
                        else:
                            pass
                    if abjad.inspect(run[0]).has_indicator(abjad.Dynamic):
                        abjad.attach(abjad.StopHairpin(), run[0])
                        abjad.attach(hairpin, run[0])
                        abjad.attach(stop, run[-1])
                    else:
                        abjad.hairpin([start, hairpin, stop], run)
                else:
                    hold_last = self._cyc_hold_last_boolean_vector(r=1)[0]
                    if hold_last is True:
                        start = abjad.Dynamic(self._cyc_dynamics(r=1)[0])
                        sustain = abjad.StartHairpin("--")
                        next_leaf = abjad.inspect(run[-1]).leaf(1)
                        abjad.attach(start, run[0])
                        abjad.attach(sustain, run[0])
                        if isinstance(next_leaf, (abjad.Rest, abjad.MultimeasureRest)):
                            abjad.attach(abjad.StopHairpin(), next_leaf)
                    else:
                        items = self._cyc_dynamics(r=2)
                        start = abjad.Dynamic(items[0])
                        stop = abjad.Dynamic(items[1], leak=True)
                        hairpin = abjad.StartHairpin(
                            self._calculate_hairpin(
                                start,
                                stop,
                                flared=self._cyc_flare_boolean_vector(r=1)[0],
                            )
                        )
                        abjad.hairpin([start, hairpin, stop], run)
            else:
                start = abjad.Dynamic(self._cyc_dynamics(r=1)[0])
                if start == abjad.Dynamic("niente"):
                    start = abjad.Dynamic(self._cyc_dynamics(r=1)[0])
                hairpin = abjad.StartHairpin("--")
                stopper = abjad.StopHairpin()
                next_leaf = abjad.inspect(run[-1]).leaf(1)
                abjad.attach(start, run[0])
                abjad.attach(hairpin, run[0])
                if isinstance(next_leaf, (abjad.Rest, abjad.MultimeasureRest)):
                    abjad.attach(stopper, next_leaf)
                else:
                    pass


# ###DEMO###
# staff = abjad.Staff("c'4 d'4 e'4 f'4 r4 g'4 r2")
#
# handler = DynamicHandler(
#     # dynamic_list=[3, -1, 2, 4],
#     dynamic_list=['f', 'niente', 'p', 'mf'],
#     flare_boolean_vector=[False, False, False, True],
#     hold_first_boolean_vector=[True, False, False,],
#     hold_last_boolean_vector=[False, True],
#     continuous=True,
# )
#
# # for run in abjad.select(staff).runs():
# #     handler(run)
#
# # handler(staff) # should be different but is not
#
# first_group = staff[0:3]
# second_group = staff[2:]
#
# handler(first_group)
# handler(second_group)
#
# abjad.f(staff)
