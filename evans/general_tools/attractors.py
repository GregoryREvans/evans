import numpy as np
from scipy.integrate import odeint


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
        return sigma * (y - x), x * (rho - z) - y, x * y - beta * z
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
