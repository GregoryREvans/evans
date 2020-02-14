def altered_period(
    phase_response_curve=0.5,
    time_elapsed_since_last_call_of_focal_male=20,
    distance_of_stimulus_in_meters=10,
    decay=100,
    effector_delay=60,
    period=500,
    stochastic_element=30,
    neighbor_stimulus_length=60,
    stimulus_length=50,
    return_in_seconds=True,
):
    sound_delay = distance_of_stimulus_in_meters / 344
    leader_delay = time_elapsed_since_last_call_of_focal_male + sound_delay
    social_delay = decay - effector_delay
    delays = leader_delay - social_delay
    variability = period + stochastic_element
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
#         time_elapsed_since_last_call_of_focal_male=20,
#         distance_of_stimulus_in_meters=10,
#         decay=100,
#         effector_delay=60,
#         period=500,
#         stochastic_element=30,
#         neighbor_stimulus_length=60,
#         stimulus_length=50,
#         return_in_seconds=True,
#         )
# )
