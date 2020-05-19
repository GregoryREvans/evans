def orbits(initial_state=0.4, iterations=10):
    list_ = []
    for _ in range(iterations):
        front = 4 * initial_state
        back = 1 - initial_state
        next_state = front * back
        list_.append(next_state)
        initial_state = next_state
    return list_


# print(orbits(initial_state=0.4, iterations=20))


def feigenbaum_bifurcations(fertility=3.59785, initial_state=0.5, iterations=10):
    list_ = [initial_state]
    for _ in range(iterations):
        front = fertility * initial_state
        back = 1 - initial_state
        next_state = front * back
        list_.append(next_state)
        initial_state = next_state
    return list_


# print(feigenbaum_bifurcations(fertility= 2.3, initial_state=0.5, iterations=10))


# import matplotlib.pyplot as plt
# plt.plot(bifurcations(initial_state=0.37, iterations=200))
# plt.ylabel('bifurcation orbits')
# plt.xlabel('fedback iterations')
# plt.show()
