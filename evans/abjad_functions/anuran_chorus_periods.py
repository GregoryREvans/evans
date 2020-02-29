import abjad


def altered_period(  # round to halves and use with talea timespanmaker
    phase_response_curve=0.5,
    time_elapsed_since_last_call_of_focal_male=20,
    distance_of_stimulus_in_meters=10,
    decay=100,
    effector_delay=60,
    period_in_miliseconds=500,
    stochastic_element=30,
    neighbor_stimulus_length=60,
    stimulus_length=50,
    return_in_seconds=True,
):
    sound_delay = distance_of_stimulus_in_meters / 344
    leader_delay = time_elapsed_since_last_call_of_focal_male + sound_delay
    social_delay = decay - effector_delay
    delays = leader_delay - social_delay
    variability = period_in_miliseconds + stochastic_element
    stimuli = neighbor_stimulus_length - stimulus_length
    first_half = phase_response_curve * delays
    last_half = variability + stimuli
    answer = first_half + last_half
    if return_in_seconds is True:
        answer = answer / 1000
    return answer


# print(
#     altered_period(
#         phase_response_curve=0.5,
#         time_elapsed_since_last_call_of_focal_male=35,
#         distance_of_stimulus_in_meters=10,
#         decay=100,
#         effector_delay=60,
#         period_in_miliseconds=500,
#         stochastic_element=30,
#         neighbor_stimulus_length=60,
#         stimulus_length=50,
#         return_in_seconds=True,
#         )
# )


def make_focal_voice(
    target_timespan=None, period_timespan=None, stimulus_length_timespan=None
):
    silence = period_timespan - stimulus_length_timespan
    silence = silence[0]
    ts_list = abjad.TimespanList()
    ts_list.append(stimulus_length_timespan)
    ts_list.append(silence)
    while ts_list[-1].stop_offset < target_timespan.stop_offset:
        adder = ts_list[-1].stop_offset
        new_stim = abjad.Timespan(
            stimulus_length_timespan.start_offset + adder,
            stimulus_length_timespan.stop_offset + adder,
        )
        new_silence = abjad.Timespan(
            silence.start_offset + adder, silence.stop_offset + adder
        )
        ts_list.append(new_stim)
        ts_list.append(new_silence)
    for sil in ts_list[1::2]:
        ts_list = ts_list - sil
    return ts_list


# basically do the same process as make_focal_voice but adjust the length of silence each time
def make_altered_period(
    focal_voice_timespan_list=None,
    target_timespan=None,
    period_timespan=None,
    stimulus_length_timespan=None,
    extra_offset=None,
):
    ts_list = abjad.TimespanList()
    return ts_list


###DEMO###

# target_tspan = abjad.Timespan(0, 5000)
# period_tspan = abjad.Timespan(0, 500)
# stimulus_length_tspan = abjad.Timespan(0, 50)
#
# ts_l = make_focal_voice(
#     target_timespan=target_tspan,
#     period_timespan=period_tspan,
#     stimulus_length_timespan=stimulus_length_tspan,
#     )
# abjad.show(ts_l, scale=0.5)
# ts_l.scale(0.02)
# ts_l.round_offsets((1, 8))
# abjad.show(ts_l, scale=0.5)
# #how to reduce silence?
