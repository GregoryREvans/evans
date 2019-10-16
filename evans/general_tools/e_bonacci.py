def e_bonacci_cycle(n, iters, first, second, modulus, wrap_to_zero=False):
    final = [0] * iters
    final[n - 1] = first
    final[n] = second
    for i, slot in enumerate(final[n + 1:]):
        i = i + n + 1
        dist = n + 1
        bound = i - dist
        sum = 0
        for x in final[i - 1: bound: -1]:
            sum = sum + x
        final[i] = sum
    for _ in range(n - 1):
        final.remove(0)
    sequence = [(_ % modulus) for _ in final]
    if wrap_to_zero is False:
        for index, item in enumerate(sequence):
            if item == 0:
                sequence[index] = item + modulus
    return sequence

# ###DEMO###
# print(e_bonacci_cycle(n=3, iters=15, first=1, second=1, modulus=7))
