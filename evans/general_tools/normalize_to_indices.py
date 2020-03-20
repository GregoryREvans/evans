import evans


def normalize_to_indices(raw_list=[1, 0.24, -12, [-4, 0.7], -0.5]):
    out = []
    flat_raw = [abs(float(_)) for _ in evans.flatten(raw_list)]
    minimum_value = min(flat_raw)
    if minimum_value == 0:
        minimum_value = 0.000001
    for _ in raw_list:
        if isinstance(_, list):
            out.append(normalize_to_indices(_))
        else:
            out.append(int(float(_) / minimum_value))
    return out


###DEMO###
# import evans
# h = evans.henon()[0][:10]
# print(h)
# norm_to_ind_h = normalize_to_indices(h)
# print(norm_to_ind_h)
# source = [0, 1, 2, 3, 4, 5]
# for _ in norm_to_ind_h:
#     index = _ % len(source)
#     print(source[index])
###DEMO2###
# print(normalize_to_indices(raw_list=[1, 0.24, -12, [-4, 0.7], -0.5]))
