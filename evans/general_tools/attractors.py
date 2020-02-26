import numpy as np
import scipy as sp
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
    first_state=[(-0.75), 0.32]
    a=1.2,
    b=0.3,
    iters=10000,
    ):
    x_coordinates = [first_state[0]]
    y_coordinates = [first_state[1]]
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

#We define a function which is going to be the recursive function.
def roessler(
    a=0.13,
    b=0.2,
    c=6.5,
    t_ini=0,
    t_fin=32*pi,
    h=0.0001,
    first_state=[0, 0, 0],
    ):
    def num_rossler(x_n,y_n,z_n,h,a_,b_,c_):
        x_n1=x_n+h*(-y_n-z_n)
        y_n1=y_n+h*(x_n+a_*y_n)
        z_n1=z_n+h*(b_+z_n*(x_n-c_))
        return x_n1,y_n1,z_n1
    numsteps=int((t_fin-t_ini)/h)
    t=linspace(t_ini,t_fin,numsteps)
    x=zeros(numsteps)
    y=zeros(numsteps)
    z=zeros(numsteps)
    x[0]=first_state[0]
    y[0]=first_state[1]
    z[0]=first_state[2]
    for k in range(x.size-1):
        [x[k+1],y[k+1],z[k+1]]=num_rossler(x[k],y[k],z[k],t[k+1]-t[k],a,b,c)
