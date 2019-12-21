import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList

#incorporate spanner anchors
class DynamicHandler:
    def __init__(
        self,
        dynamic_list=None,
        flare_boolean_vector=[0],
        flare_continuous=True,
        hold_first_boolean_vector=[0],
        hold_first_continuous=True,
        hold_last_boolean_vector=[0],
        hold_last_continuous=True,
        effort_boolean_vector=[0],
        effort_continuous=True,
        continuous=True,
        count_1=-1,
        count_2=-1,
        count_3=-1,
        count_4=-1,
        count_5=-1,
        name="Dynamic Handler",
    ):
        self.dynamic_list = dynamic_list
        self.flare_boolean_vector = flare_boolean_vector
        self.flare_continuous = flare_continuous
        self.hold_first_boolean_vector = hold_first_boolean_vector
        self.hold_first_continuous = hold_first_continuous
        self.hold_last_boolean_vector = hold_last_boolean_vector
        self.hold_last_continuous = hold_last_continuous
        self.effort_boolean_vector = effort_boolean_vector
        self.effort_continuous = effort_continuous
        self.continuous = continuous
        self._count_1 = count_1
        self._count_2 = count_2
        self._count_3 = count_3
        self._count_4 = count_4
        self._count_5 = count_5
        self._cyc_dynamics = CyclicList(dynamic_list, self.continuous, self._count_1)
        self._cyc_flare_boolean_vector = CyclicList(
            flare_boolean_vector, self.flare_continuous, self._count_2
        )
        self._cyc_hold_first_boolean_vector = CyclicList(
            hold_first_boolean_vector, self.hold_first_continuous, self._count_3
        )
        self._cyc_hold_last_boolean_vector = CyclicList(
            hold_last_boolean_vector, self.hold_last_continuous, self._count_4
        )
        self._cyc_effort_boolean_vector = CyclicList(
            effort_boolean_vector, self.effort_continuous, self._count_5
        )
        self.name = name

    def __call__(self, selections):
        self._apply_dynamics(selections)

    def _calculate_hairpin(self, start, stop, flared=0):
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
        if flared == 1:
            if start.ordinal < stop.ordinal:
                if start.name == "niente":
                    start = abjad.Dynamic(
                        "niente", hide=True
                    )  # carry these through instead?
                    hairpin = "o<|"
                else:
                    hairpin = "<|"
            else:
                if stop.name == "niente":
                    stop = abjad.Dynamic("niente", command="\!")
                    hairpin = "|>o"
                else:
                    hairpin = "|>"
        else:
            if start.ordinal < stop.ordinal:
                if start.name == "niente":
                    start = abjad.Dynamic("niente", hide=True)
                    hairpin = "o<"
                else:
                    hairpin = "<"
            else:
                if stop.name == "niente":
                    stop = abjad.Dynamic("niente", command="\!")
                    hairpin = ">o"
                else:
                    hairpin = ">"
        return hairpin  # , start, stop?

    def _make_effort_dynamics(self, dyn):
        conversion = {
            "ppppp": '"ppppp"',
            "pppp": '"pppp"',
            "ppp": '"ppp"',
            "pp": '"pp"',
            "p": '"p"',
            "mp": '"mp"',
            "mf": '"mf"',
            "f": '"f"',
            "ff": '"ff"',
            "fff": '"fff"',
            "ffff": '"ffff"',
            "fffff": '"fffff"',
            "fp": '"fp"',
            "sf": '"sf"',
            "sff": '"sff"',
            "sp": '"sp"',
            "spp": '"spp"',
            "sfz": '"sfz"',
            "sffz": '"sffz"',
            "sfffz": '"sfffz"',
            "sffp": '"sffp"',
            "sffpp": '"sffpp"',
            "sfp": '"sfp"',
            "sfpp": '"sfpp"',
            "rfz": '"rfz"',
            "niente": "niente",
        }
        return conversion[dyn]

    def _apply_dynamics(self, selections):
        for run in abjad.select(selections).runs():
            hold_first = self._cyc_hold_first_boolean_vector(r=1)[0]
            if hold_first == 0:
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
                            start, stop, flared=self._cyc_flare_boolean_vector(r=1)[0]
                        )
                    )
                    hold_last = self._cyc_hold_last_boolean_vector(r=1)[0]
                    effort_bools = self._cyc_effort_boolean_vector(r=2)
                    if isinstance(start, str):
                        if effort_bools[0] == 0:
                            start = start
                        else:
                            start = self._make_effort_dynamics(start)
                        start = abjad.Dynamic(start)
                    elif isinstance(start, int):
                        start = abjad.Dynamic.dynamic_ordinal_to_dynamic_name(start)
                        if effort_bools[0] == 0:
                            start = start
                        else:
                            start = self._make_effort_dynamics(start)
                        start = abjad.Dynamic(start)
                    else:
                        pass
                    if isinstance(stop, str):
                        if effort_bools[1] == 0:
                            stop = stop
                        else:
                            stop = self._make_effort_dynamics(stop)
                        stop = abjad.Dynamic(stop)
                    elif isinstance(stop, int):
                        stop = abjad.Dynamic.dynamic_ordinal_to_dynamic_name(stop)
                        if effort_bools[1] == 0:
                            stop = stop
                        else:
                            stop = self._make_effort_dynamics(stop)
                        stop = abjad.Dynamic(stop)
                    else:
                        pass
                    if start.name == "niente":
                        start = abjad.Dynamic("niente", hide=True)
                    if stop.name == "niente":
                        stop = abjad.Dynamic("niente", command="\!")
                    if hold_last == 1:
                        if stop.name != "niente":
                            abjad.attach(abjad.StartHairpin("--"), run[-1])
                            abjad.attach(
                                abjad.StopHairpin(), abjad.inspect(run[-1]).leaf(1)
                            )
                        else:
                            if isinstance(abjad.inspect(run[-1]).leaf(1), abjad.Rest):
                                stop = abjad.Dynamic(stop, command="\!", leak=True) #attach to anchor
                            else:
                                pass
                    else:
                        if isinstance(abjad.inspect(run[-1]).leaf(1), abjad.Rest):
                            stop = abjad.Dynamic(stop, leak=True) #attach to anchor
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
                    if hold_last == 1:
                        start = self._cyc_dynamics(r=1)[0]
                        if start == "niente":
                            start = self._cyc_dynamics(r=1)[0]
                        else:
                            pass
                        if self._cyc_effort_boolean_vector(r=1)[0] == 0:
                            start = abjad.Dynamic(start)
                        else:
                            start_string = self._make_effort_dynamics(start)
                            start = abjad.Dynamic(start_string)
                        sustain = abjad.StartHairpin("--")
                        next_leaf = abjad.inspect(run[-1]).leaf(1)
                        abjad.attach(start, run[0])
                        abjad.attach(sustain, run[0])
                        if isinstance(next_leaf, (abjad.Rest, abjad.MultimeasureRest)):
                            abjad.attach(abjad.StopHairpin(), next_leaf)
                    else:
                        items = self._cyc_dynamics(r=2)
                        effort_bools = self._cyc_effort_boolean_vector(r=2)
                        start = items[0]
                        stop = items[1]
                        if effort_bools[0] == 0:
                            if start == "niente":
                                start = abjad.Dynamic(start, hide=True)
                            else:
                                start = abjad.Dynamic(start)
                        else:
                            start_string = self._make_effort_dynamics(start)
                            if start_string == "niente":
                                start = abjad.Dynamic(start_string, hide=True)
                            else:
                                start = abjad.Dynamic(start_string)
                        if effort_bools[1] == 0:
                            if stop == "niente":
                                stop = abjad.Dynamic(stop, command="\!", leak=True) #attach to anchor
                            else:
                                stop = abjad.Dynamic(stop, leak=True) #attach to anchor
                        else:
                            stop_string = self._make_effort_dynamics(stop)
                            if stop_string == "niente":
                                stop = abjad.Dynamic(
                                    stop_string, command="\!", leak=True #attach to anchor
                                )
                            else:
                                stop = abjad.Dynamic(stop_string, leak=True) #attach to anchor
                        hairpin = abjad.StartHairpin(
                            self._calculate_hairpin(
                                start,
                                stop,
                                flared=self._cyc_flare_boolean_vector(r=1)[0],
                            )
                        )
                        abjad.hairpin([start, hairpin, stop], run)
            else:
                start = self._cyc_dynamics(r=1)[0]
                if start == "niente":
                    start = self._cyc_dynamics(r=1)[0]
                effort_bool = self._cyc_effort_boolean_vector(r=1)[0]
                if effort_bool == 1:
                    start_string = self._make_effort_dynamics(start)
                    start = abjad.Dynamic(start_string)
                else:
                    start = abjad.Dynamic(start)
                hairpin = abjad.StartHairpin("--")
                stopper = abjad.StopHairpin()
                next_leaf = abjad.inspect(run[-1]).leaf(1)
                abjad.attach(start, run[0])
                abjad.attach(hairpin, run[0])
                if isinstance(next_leaf, (abjad.Rest, abjad.MultimeasureRest)):
                    abjad.attach(stopper, next_leaf)
                else:
                    pass
        self._remove_niente(selections)

    def _remove_niente(self, selections):
        for leaf in abjad.select(selections).leaves():
            for dynamic in abjad.inspect(leaf).indicators(abjad.Dynamic):
                if dynamic.name is "niente":
                    if dynamic.command == "\!":
                        abjad.detach(dynamic, leaf)
                        abjad.attach(
                            abjad.Dynamic(dynamic, command="\!", leak=True), leaf #attach to anchor
                        )  # maybe just continue instead of replacing?
                    elif dynamic.leak is True:
                        abjad.detach(dynamic, leaf)
                        abjad.attach(
                            abjad.Dynamic(dynamic, command="\!", leak=True), leaf #attach to anchor
                        )
                    else:
                        abjad.detach(dynamic, leaf)
                        abjad.attach(abjad.Dynamic(dynamic, hide=True), leaf)
                else:
                    continue

    def name(self):
        return self.name

    def state(self):
        return f"""count 1\n{self._cyc_dynamics.state()}\ncount 2\n{self._cyc_flare_boolean_vector.state()}\ncount 3\n{self._cyc_hold_first_boolean_vector.state()}\ncount 4\n{self._cyc_hold_last_boolean_vector.state()}\ncount 5\n{self._cyc_effort_boolean_vector.state()}"""


# ###DEMO###
# staff = abjad.Staff("c'4 d'4 e'4 f'4 r4 g'4 r2")
#
# handler = DynamicHandler(
#     # dynamic_list=[3, -1, 2, 4],
#     dynamic_list=['f', 'niente', 'p', 'mf'],
#     flare_boolean_vector=[0, 0, 0, 1],
#     flare_continuous=True,
#     hold_first_boolean_vector=[1, 0, 0,],
#     hold_first_continuous=True,
#     hold_last_boolean_vector=[0, 1],
#     hold_last_continuous=True,
#     effort_boolean_vector=[1, 0],
#     effort_continuous=True,
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
# abjad.show(staff)
