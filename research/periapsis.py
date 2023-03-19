import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from PyAstronomy import pyasl

orbit = pyasl.KeplerEllipse(a=1.0, per=1.0, e=0.5, Omega=0.0, i=30.0, w=0.0)
t = np.linspace(0, 4, 200)

pos = orbit.xyzPos(t)

plt.plot(0, 0, "bo", markersize=9, label="Earth")
plt.plot(pos[::, 1], pos[::, 0], "k-", label="Satellite Trajectory")
plt.plot(pos[0, 1], pos[0, 0], "r*", label="Periapsis")

plt.legend(loc="upper right")
plt.title("Orbital Simulation")
plt.show()


# import math
#
#
# class BinaryOrbit:
#     def __init__(
#         alpha,
#         mu,
#         eccentricity,
#     ):
#         self.alpha = alpha
#         self.mu = mu
#         self.eccentricity = eccentricity
#
#     @property
#     def apocenter(self):
#         min_speed = math.sqrt(((1 - self.eccentricity) * self.mu) / ((1 + self.eccentricity) * self.alpha))
#         max_distance = ((1 + self.eccentricity) * self.alpha)
#         return (min_speed, max_distance)
#
#     @property
#     def pericenter(self):
#         max_speed = math.sqrt(((1 + self.eccentricity) * self.mu) / ((1 - self.eccentricity) * self.alpha))
#         min_distance = ((1 - self.eccentricity) * self.alpha)
#         return (max_speed, min_distance)
#
#     @property
#     def specific_relative_angular_momentum(self):
#         return math.sqrt(((1 - (self.eccentricity ** 2)) * self.mu * self.alpha))
#
#     @property
#     def specific_orbital_energy(self):
#         return - (self.mu / (2 * self.alpha))
