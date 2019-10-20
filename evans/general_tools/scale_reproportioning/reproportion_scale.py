import abjad
from evans.general_tools.reciprocal import reciprocal


def reproportion_scale(base, limit):
    step = base / 10.0
    end = limit + 1
    scale = [_ for _ in range(2, end)]
    new_scale = [_ * step for _ in scale]
    return new_scale


def _return_amplitude_reciprocals(rescaled_scale):
    reciprocal_list = [1]
    for _ in rescaled_scale:
        reciprocal_list.append(reciprocal(_))
    return reciprocal_list


def reproportion_harmonics(fund, scale, return_amp_reciprocals=None):
    calculated_series = [_ * fund for _ in scale]
    final_series = [fund]
    final_series.extend(calculated_series)
    if return_amp_reciprocals == "as_tuples":
        return [
            (harmonic, amp)
            for harmonic, amp in zip(final_series, _return_amplitude_reciprocals(scale))
        ]
    elif return_amp_reciprocals == "as_lists":
        return final_series, _return_amplitude_reciprocals(scale)
    else:
        return final_series


def _to_nearest_eighth_tone(number):
    number = round(float(number) * 4) / 4
    div, mod = divmod(number, 1)
    if mod == 0.75:
        div += 0.75  # used to be 1
    elif mod == 0.5:
        div += 0.5
    elif mod == 0.25:  # new
        div += 0.25  # new
    return abjad.mathtools.integer_equivalent_number_to_integer(div)


def reproportion_chromatic_decimals(base, root_int, scale_range, round=False):
    base_converter = base / 10.0
    octave = root_int + 12
    converted_octave = octave * base_converter
    collection = [root_int]
    step = converted_octave / 12
    for _ in range(scale_range):
        collection.append(collection[-1] + step)
    if round is True:
        collection = [_to_nearest_eighth_tone(_) for _ in collection]
    return collection

def reproportion_chord(base, chord, round=False):
    base_converter = base / 10.0
    collection = []
    for _ in chord:
        collection.append(_ * base_converter)
    if round is True:
        collection = [_to_nearest_eighth_tone(_) for _ in collection]
    return collection


###DEMO###
# insert_scale = (reproportion_scale(base=15, limit=17))
# print(insert_scale)
# print(reproportion_harmonics(fund=20, scale=insert_scale, return_amp_reciprocals='as_tuples'))
# print(reproportion_harmonics(fund=20, scale=insert_scale, return_amp_reciprocals='as_lists'))
# print(reproportion_harmonics(fund=20, scale=insert_scale))
# print(reproportion_chromatic_decimals(base=10, root_int=0, scale_range=12, round=True))
# print(reproportion_chord(base=2, chord=[-24, -20, -15, -14, -4, 5, 11, 19, 26, 37, 39, 42], round=True))
