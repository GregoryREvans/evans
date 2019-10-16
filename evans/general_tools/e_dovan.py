def e_dovan_cycle(n, iters, first, second, modulus, wrap_to_zero=False):
    iters = iters + 1
    final = [0] * iters
    final[n] = first
    final[n + 1] = second
    for i, slot in enumerate(final[n + 2:]):
        i = i + n + 2
        dist = n + 2
        bound = i - dist
        sum = 0
        for x in final[i - 2: bound: -1]:
            sum = sum + x
        final[i] = sum
    for _ in range(n):
        final.remove(0)
    sequence = [(_ % modulus) for _ in final]
    if wrap_to_zero is False:
        for index, item in enumerate(sequence):
            if item == 0:
                sequence[index] = item + modulus
    return sequence

# ###DEMO###
# print(e_dovan_cycle(n=3, iters=15, first=1, second=1, modulus=7))
