import numpy as np


def mandelbrot(c,maxiter):
    z = c
    for n in range(maxiter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return 0

def mandelbrot_set(xmin,xmax,ymin,ymax,width,height,maxiter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width,height))
    for i in range(width):
        for j in range(height):
            n3[i,j] = mandelbrot(r1[i] + 1j*r2[j],maxiter)
    # print(f"r1={r1}")
    # print(f"r2={r2}")
    # print(f"n3={n3}")
    return (r1,r2,n3)

# mandelbrot_set(
#     xmin=7,
#     xmax=100,
#     ymin=7,
#     ymax=100,
#     width=100,
#     height=100,
#     maxiter=100,
#     )
