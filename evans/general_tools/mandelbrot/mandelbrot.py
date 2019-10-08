# MAX_ITER = 80


def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return n


###demo###
# for a in range(-10, 10, 5):
#     for b in range(-10, 10, 5):
#         c = complex(a / 10, b / 10)
#         print(c, mandelbrot(c, MAX_ITER))
