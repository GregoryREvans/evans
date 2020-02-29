def normalize_to_indices(raw_list=[1, 0.24, -12, -0.5]):
    list_of_floats = [float(_) for _ in raw_list]
    abs_list_of_floats = [abs(_) for _ in list_of_floats]
    m = min(abs_list_of_floats)
    if m == 0:
        m = 0.000001
    norm_list_of_floats = [int(float(i)/m) for i in list_of_floats]
    return norm_list_of_floats

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
