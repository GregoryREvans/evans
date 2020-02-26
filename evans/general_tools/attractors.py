import numpy as np
from scipy.integrate import odeint
from decimal import Decimal


def lorenz(
    rho=28.0,
    sigma=10.0,
    beta=(8.0 / 3.0),
    first_state=[1.0, 1.0, 1.0],
    time_values=[0.0, 40.0, 0.01],
    iters=20,
    ):
    def vector_calc(state, t):
        x, y, z = state
        return Decimal(sigma) * (Decimal(y) - Decimal(x)), Decimal(x) * (Decimal(rho) - Decimal(z)) - Decimal(y), Decimal(x) * Decimal(y) - Decimal(beta) * Decimal(z)
    t = np.arange(time_values[0], time_values[1], time_values[2])
    states = odeint(vector_calc, first_state, t)
    return [[_ for _ in states[:iters, 0]], [_ for _ in states[:iters, 1]], [_ for _ in states[:iters, 2]]]

###DEMO###
# print(
#     lorenz(
#         rho=28.0,
#         sigma=10.0,
#         beta=(8.0 / 3.0),
#         first_state=[1.0, 1.0, 1.0],
#         time_values=[0.0, 40.0, 0.01],
#         iters=5,
#         )
#     )

# import matplotlib.pyplot as plt
#
# map = lorenz(
#         rho=28.0,
#         sigma=10.0,
#         beta=(8.0 / 3.0),
#         first_state=[1.0, 1.0, 1.0],
#         time_values=[0.0, 40.0, 0.01],
#         iters=50000,
#     )
# plt.scatter(map[0], map[1], s=0.5)
# plt.scatter(map[1], map[2], s=0.5)
# plt.scatter(map[0], map[2], s=0.5)


def henon(
    initial_x=(-0.75),
    initial_y=0.32,
    a=1.2,
    b=0.3,
    iters=10000,
    ):
    x_coordinates = [initial_x]
    y_coordinates = [initial_y]
    for _ in range(iters):
        prev_x = x_coordinates[-1]
        prev_y = y_coordinates[-1]
        x_coordinates.append((Decimal(prev_y) + 1) - (Decimal(a) * (Decimal(prev_x) ** 2)))
        y_coordinates.append(Decimal(b) * Decimal(prev_x))
    return x_coordinates, y_coordinates

###DEMO###
# print(
#     henon(
#         initial_x=(-0.75),
#         initial_y=0.32,
#         a=1.2,
#         b=0.3,
#         iters=10000,
#         )
# )
# import matplotlib.pyplot as plt
#
# map = henon(
#     initial_x=1,
#     initial_y=1,
#     a=1.4,
#     b=0.3,
#     iters=10000,
# )
# plt.scatter(map[0], map[1], s=0.5)
