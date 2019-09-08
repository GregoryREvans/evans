import numpy as np


class MarkovChain(object):
    def __init__(self, transition_prob):
        self.transition_prob = transition_prob
        self.states = list(transition_prob.keys())

    def next_state(self, current_state):
        return np.random.choice(
            self.states,
            p=[
                self.transition_prob[current_state][next_state]
                for next_state in self.states
            ],
        )

    def generate_states(self, current_state, no=10):
        future_states = []
        for i in range(no):
            next_state = self.next_state(current_state)
            future_states.append(next_state)
            current_state = next_state
        return future_states


transition_prob = {
    "microtones_up": {
        "microtones_down": 0.8,
        "combinations": 0.19,
        "microtones_up": 0.01,
    },
    "microtones_down": {
        "microtones_up": 0.2,
        "combinations": 0.7,
        "microtones_down": 0.1,
    },
    "combinations": {"microtones_down": 0.1, "combinations": 0.2, "microtones_up": 0.7},
}

weather_chain = MarkovChain(transition_prob=transition_prob)

print(weather_chain.generate_states(current_state="combinations", no=20))
