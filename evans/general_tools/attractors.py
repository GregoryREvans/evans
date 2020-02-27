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

def henon(
    first_state=[(-0.75), 0.32],
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

def roessler(
    a=0.13,
    b=0.2,
    c=6.5,
    t_ini=0,
    t_fin=(32 * (np.pi)),
    h=0.0001,
    ):
    def calc_coordinates(x_n,y_n,z_n,h,a_,b_,c_):
        x_n1 = x_n + h * (-y_n - z_n)
        y_n1 = y_n + h * (x_n + a_ * y_n)
        z_n1 = z_n + h * (b_ + z_n * (x_n - c_))
        return x_n1, y_n1, z_n1
    numsteps = int((t_fin - t_ini) / h)
    t = sp.linspace(t_ini, t_fin, numsteps)
    x = np.zeros(numsteps)
    y = np.zeros(numsteps)
    z = np.zeros(numsteps)
    x[0]=0
    y[0]=0
    z[0]=0
    for _ in range(x.size-1):
        [x[_+1], y[_+1], z[_+1]] = calc_coordinates(x[_], y[_], z[_], t[_+1]-t[_], a, b, c)
    return x, y, z

###DEMOS###
##LORENZ DEMO###
# from matplotlib import *
# from pylab import figure, show, setp
# map = lorenz(
#         rho=28.0,
#         sigma=10.0,
#         beta=(8.0 / 3.0),
#         first_state=[1.0, 1.0, 1.0],
#         time_values=[0.0, 40.0, 0.01],
#         iters=50000,
#     )
#
# import matplotlib.pyplot as plt
# plt.scatter(map[0], map[1], s=0.5)
# plt.scatter(map[1], map[2], s=0.5)
# plt.scatter(map[0], map[2], s=0.5)
#3D
# fig = figure()
# ax1 = fig.add_axes([0.1, 0.7, 0.4, 0.2])
# ax2 = fig.add_axes([0.1, 0.4, 0.4, 0.2])
# ax3 = fig.add_axes([0.1, 0.1, 0.4, 0.2])
# ax4 = fig.add_axes([0.55, 0.25, 0.35, 0.5], projection='3d')
# ax1.plot([_ for _ in range(len(map[0]))], map[0], color='red',lw=1,label='x(t)')
# ax1.set_xlabel('t')
# ax1.set_ylabel('x(t)')
# ax1.legend()
# ax1.axis((0, len(map[0]), min(map[0]), max(map[0])))
#
# ax2.plot([_ for _ in range(len(map[1]))], map[1], color='green',lw=1,label='y(t)')
# ax2.set_xlabel('t')
# ax2.set_ylabel('y(t)')
# ax2.legend()
# ax2.axis((0, len(map[1]), min(map[1]), max(map[1])))
#
# ax3.plot([_ for _ in range(len(map[1]))], map[2], color='blue',lw=1,label='z(t)')
# ax3.set_xlabel('t')
# ax3.set_ylabel('z(t)')
# ax3.legend()
# ax3.axis((0, len(map[2]), min(map[2]), max(map[2])))
#
# ax4.plot(map[0], map[1], map[2], color='black',lw=1,label='Evolution(t)')
# ax4.set_xlabel('x(t)')
# ax4.set_ylabel('y(t)')
# ax4.set_zlabel('z(t)')
# ax4.set_title('Evolution')
# fig.savefig('lorenz.png')

###HENON DEMO###
# import matplotlib.pyplot as plt
#
# map = henon(
#     first_state=[(-0.75), 0.32],
#     a=1.4,
#     b=0.3,
#     iters=400,
# )

# fig = plt.figure()
# ax=fig.add_axes([0,0,1,1])
# ax.scatter(map[0], map[1], s=0.5)
# fig.savefig('henon.png')
#
# import matplotlib.pyplot as plt
# from matplotlib import *
# from pylab import figure, show, setp
# fig = figure()
# ax1 = fig.add_axes([0.1, 0.7, 0.4, 0.2])
# ax2 = fig.add_axes([0.1, 0.4, 0.4, 0.2])
# ax3 = fig.add_axes([0.55, 0.25, 0.35, 0.5])
# ax1.plot([_ for _ in range(len(map[0]))], map[0], color='red',lw=1,label='x(t)')
# ax1.set_xlabel('t')
# ax1.set_ylabel('x(t)')
# ax1.legend()
#
# ax2.plot([_ for _ in range(len(map[1]))], map[1], color='green',lw=1,label='y(t)')
# ax2.set_xlabel('t')
# ax2.set_ylabel('y(t)')
# ax2.legend()
#
# ax3.scatter(map[0], map[1], color='black',lw=1,label='Evolution(t)', s=0.5)
# ax3.set_xlabel('x(t)')
# ax3.set_ylabel('y(t)')
# ax3.set_title('Evolution')
# fig.savefig('henon.png')

###ROESSLER DEMO###
# map = roessler(
#     a=0.13,
#     b=0.2,
#     c=6.5,
#     t_ini=0,
#     t_fin=(32 * (np.pi)),
#     h=0.0001,
# )
#
# from matplotlib import *
# from pylab import figure, show, setp
# from mpl_toolkits.mplot3d import Axes3D
# t = sp.linspace(0, (32 * (np.pi)), int(((32 * (np.pi) - 0) / 0.0001)))
# fig = figure()
# ax1 = fig.add_axes([0.1, 0.7, 0.4, 0.2])
# ax2 = fig.add_axes([0.1, 0.4, 0.4, 0.2])
# ax3 = fig.add_axes([0.1, 0.1, 0.4, 0.2])
# ax4 = fig.add_axes([0.55, 0.25, 0.35, 0.5],projection='3d')
#
# ax1.plot(t, map[0], color='red',lw=1,label='x(t)')
# ax1.set_xlabel('t')
# ax1.set_ylabel('x(t)')
# ax1.legend()
# ax1.axis((0,(32 * (np.pi)),min(map[0]),max(map[0])))
#
# ax2.plot(t, map[1], color='green',lw=1,label='y(t)')
# ax2.set_xlabel('t')
# ax2.set_ylabel('y(t)')
# ax2.legend()
# ax2.axis((0,(32 * (np.pi)),min(map[1]),max(map[1])))
#
# ax3.plot(t, map[2], color='blue',lw=1,label='z(t)')
# ax3.set_xlabel('t')
# ax3.set_ylabel('z(t)')
# ax3.legend()
# ax3.axis((0,(32 * (np.pi)),min(map[2]),max(map[2])))
#
# ax4.plot(map[0], map[1], map[2],color='black',lw=1,label='Evolution(t)')
# ax4.set_xlabel('x(t)')
# ax4.set_ylabel('y(t)')
# ax4.set_zlabel('z(t)')
# ax4.set_title('Evolution')
# from matplotlib import pyplot as plt
# fig.savefig('roessler.png')
