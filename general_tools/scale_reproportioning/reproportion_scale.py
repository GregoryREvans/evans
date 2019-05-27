import abjad

def reproportion_scale(base, limit):
    step = base / 10.0
    end = limit + 1
    scale = [_ for _ in range(2, end)]
    new_scale = [_ * step for _ in scale]
    return new_scale

def reproportion_harmonics(fund, scale):
    calculated_series = [_ * fund for _ in scale]
    final_series = [fund,]
    final_series.extend(calculated_series)
    return final_series

def _to_nearest_eighth_tone(number):
    number = round(float(number) * 4) / 4
    div, mod = divmod(number, 1)
    if mod == 0.75:
        div += 0.75 # used to be 1
    elif mod == 0.5:
        div += 0.5
    elif mod == 0.25: # new
        div += 0.25 # new
    return abjad.mathtools.integer_equivalent_number_to_integer(div)

def reproportion_chromatic_decimals(base, root_int, scale_range, round=False):
    base_converter = base / 10.0
    octave = root_int + 12
    converted_octave = octave * base_converter
    collection = [root_int, ]
    step = converted_octave / 12
    for _ in range(scale_range):
            collection.append(collection[-1] + step)
    if round is True:
        collection = [_to_nearest_eighth_tone(_) for _ in collection]
    return collection

###DEMO###
# insert_scale = (reproportion_scale(base=10, limit=17))
# print(insert_scale)
# print(reproportion_harmonics(fund=20, scale=insert_scale))
# print(reproportion_chromatic_decimals(base=10, root_int=0, scale_range=12, round=True))
