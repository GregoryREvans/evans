from math import log, log2

# MAX_ITER = 80

def julia(c, z0, max_iter):
    z = z0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1

    if n == max_iter:
        return max_iter

    return n + 1 - log(log2(abs(z)))
