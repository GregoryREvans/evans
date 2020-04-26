def harmonic_series(fundamental=20, number_of_partials=10):
    returned_list = []
    for _ in range(number_of_partials):
        multiplier = _ + 1
        returned_list.append(fundamental * multiplier)
    return returned_list

# print(harmonic_series(20, 10))

def multiple_sequence(fundamental=20, number_of_partials=10, multiple=1.5):
    returned_list = [float(fundamental)]
    for _ in range(number_of_partials):
        returned_list.append(returned_list[-1] * multiple)
    return returned_list

# print(multiple_sequence(20, 10, 1.25))
