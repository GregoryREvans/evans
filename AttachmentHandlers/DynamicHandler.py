import abjad


class DynamicHandler:
    def __init__(
        self,
        dynamic_list=None,
        flare_boolean_vector=None,
        hold_last_boolean_vector=None,
        effort_boolean_vector=None,
        continuous=True,
    ):
        def cyc(
            lst, count, continuous
        ):  # something is wrong here...cyc can never really be false?
            if continuous is False:
                count = -1
            while True:
                count += 1
                yield lst[count % len(lst)]

        self.dynamic_list = dynamic_list
        self.flare_boolean_vector = flare_boolean_vector
        self.hold_last_boolean_vector = hold_last_boolean_vector
        self.effort_boolean_vector = effort_boolean_vector
        self.continuous = continuous
        self._count_1 = -1
        self._count_2 = -1
        self._count_3 = -1
        self._count_4 = -1
        self._cyc_dynamics = cyc(dynamic_list, self._count_1, self.continuous)
        self._cyc_flare_boolean_vector = cyc(
            flare_boolean_vector, self._count_2, self.continuous
        )
        self._cyc_hold_last_boolean_vector = cyc(
            hold_last_boolean_vector, self._count_3, self.continuous
        )
        self._cyc_effort_boolean_vector = cyc(
            effort_boolean_vector, self._count_4, self.continuous
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
            if len(run) > 1:
                if abjad.inspect(run[0]).has_indicator(abjad.Dynamic):
                    current_dynamic = abjad.inspect(run[0]).indicator(abjad.Dynamic)
                    start = abjad.Dynamic(current_dynamic, hide=True)
                    stop = next(self._cyc_dynamics)
                else:
                    start = next(self._cyc_dynamics)
                    stop = next(self._cyc_dynamics)
                hairpin = abjad.StartHairpin(
                    _calculate_hairpin(
                        start, stop, flared=next(self._cyc_flare_boolean_vector)
                    )
                )
                hold_last = next(self._cyc_hold_last_boolean_vector)
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
                        abjad.attach(abjad.StopHairpin(), abjad.inspect(run[-1]).leaf(1))
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
                hold_last = next(self._cyc_hold_last_boolean_vector)
                if hold_last is True:
                    dynamic = next(self._cyc_dynamics)
                    sustain = abjad.StartHairpin('--')
                    stopper = abjad.StopHairpin()
                    abjad.attach(dynamic, run[0])
                    abjad.attach(sustain, run[0])
                    abjad.attach(stopper, abjad.inspect(run[0]).leaf(1))
                else:
                    start = abjad.Dynamic(next(self._cyc_dynamics))
                    stop = abjad.Dynamic(next(self._cyc_dynamics), leak=True)
                    hairpin = abjad.StartHairpin(
                        _calculate_hairpin(
                            start, stop, flared=next(self._cyc_flare_boolean_vector)
                        )
                    )
                    abjad.hairpin([start, hairpin, stop], run)

# ###DEMO###
# staff = abjad.Staff("c'4 d'4 e'4 f'4 r4 g'4 r2")
#
# handler = DynamicHandler(
#     # dynamic_list=[3, -1, 2, 4],
#     dynamic_list=['f', 'niente', 'p', 'mf'],
#     flare_boolean_vector=[False, False, False, True],
#     hold_last_boolean_vector=[False, True],
#     continuous=False,  # Does Not Work
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
