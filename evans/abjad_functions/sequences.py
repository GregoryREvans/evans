def harmonic_series(fundamental=20, number_of_partials=10, invert=False):
    returned_list = []
    for _ in range(number_of_partials):
        multiplier = _ + 1
        if invert is False:
            returned_list.append(fundamental * multiplier)
        else:
            returned_list.append(fundamental / multiplier)
    return returned_list


# print(harmonic_series(20, 10))
# print(harmonic_series(900, 43, True))


def multiple_sequence(fundamental=20, number_of_partials=10, multiple=1.5):
    returned_list = [float(fundamental)]
    for _ in range(number_of_partials):
        returned_list.append(returned_list[-1] * multiple)
    return returned_list


# print(multiple_sequence(20, 10, 1.25))


# ##TESTER##
# import abjad
#
#
# def isprime(num=11):
#     if num > 1:
#         for i in range(2, num//2):
#             if (num % i) == 0:
#                 return False
#         else:
#             return True
#     else:
#         return False
#
# prime_partials = []
#
# for i, partial in enumerate(harmonic_series(900, 43, True)):
#     if isprime(i):
#         prime_partials.append(partial)
#
# seq = abjad.PitchClassSet([abjad.NumberedPitch.from_hertz(_).number for _ in prime_partials])
# seg = abjad.PitchClassSegment(seq)
# abjad.show(seg)
