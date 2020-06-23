import numpy

class MarkovChain(object):
    # """
    # >>> import numpy
    # >>> numpy.random.seed(7)
    # >>> prob = {
    # ...     'one': {'one': 0.8, 'two': 0.19, 'three': 0.01},
    # ...     'two': {'one': 0.2, 'two': 0.7, 'three': 0.1},
    # ...     'three': {'one': 0.1, 'two': 0.2, 'three': 0.7}
    # ... }
    # >>> chain = evans.MarkovChain(transition_prob=prob)
    # >>> key_list = [
    # ...     x for x in chain.generate_states(
    # ...         current_state='one', no=14
    # ...         )
    # ...     ]
    # >>> key_list
    # ['one', 'one', 'one', 'one', 'two', 'two', 'two', 'one', 'one', 'one', 'one', 'two', 'two', 'one']
    #
    # """
    def __init__(self, transition_prob):
        self.transition_prob = transition_prob
        self.states = list(transition_prob.keys())

    def next_state(self, current_state):
        return numpy.random.choice(
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
