def fibonacci_cycle(first_number, second_number, length, modulus, wrap_to_zero=False):
    sequence = [first_number, second_number]
    for _ in range(length):
        sequence.append(sequence[-2] + sequence[-1])
    sequence = [(_ % modulus) for _ in sequence]
    if wrap_to_zero is False:
        for index, item in enumerate(sequence):
            if item == 0:
                sequence[index] = item + modulus
    return sequence


# ###DEMO###
# for _ in fibonacci_cycle(first_number=1, second_number=2, length=30, modulus=7):
#     print(_)
