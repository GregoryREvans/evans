"""
Sequence classes and functions.
"""
import itertools
import random

import abjad
import numpy


class CyclicList:
    r"""
    Cyclic List

    .. container:: example

        >>> _cyc_count = -1
        >>> _non_cyc_count = -1
        >>> cyc_generator = evans.CyclicList(lst=[1, 2, 3], forget=False, count=_cyc_count)
        >>> non_cyc_generator = evans.CyclicList(lst=[1, 2, 3], forget=True, count=_non_cyc_count)

        >>> cyc_generator(r=2)
        [1, 2]

        >>> cyc_generator(r=7)
        [3, 1, 2, 3, 1, 2, 3]

        >>> non_cyc_generator(r=2)
        [1, 2]

        >>> non_cyc_generator(r=7)
        [1, 2, 3, 1, 2, 3, 1]

        >>> print((cyc_generator.state(), non_cyc_generator.state()))
        (8, 6)

    """

    def __init__(self, lst=None, forget=True, count=-1):  # add *,
        self.lst = lst
        self.forget = forget
        self.count = count

    def __str__(self):
        return abjad.storage(self)

    def __repr__(self):
        return abjad.StorageFormatManager(self).get_repr_format()

    def state_cyc(self, lst, r):
        returned_material = []
        for x in range(r):
            self.count += 1
            returned_material.append(lst[self.count % len(lst)])
        return returned_material

    def non_state_cyc(self, lst, r):
        returned_material = []
        self.count = -1
        for x in range(r):
            self.count += 1
            returned_material.append(lst[self.count % len(lst)])
        return returned_material

    def __call__(self, r):
        if self.forget is False:
            return self.state_cyc(self.lst, r)
        else:
            return self.non_state_cyc(self.lst, r)

    def state(self):
        return self.count


class MarkovChain:
    """
    Markov Chain

    .. container:: example

        >>> import numpy
        >>> numpy.random.seed(7)
        >>> prob = {
        ...     'one': {'one': 0.8, 'two': 0.19, 'three': 0.01},
        ...     'two': {'one': 0.2, 'two': 0.7, 'three': 0.1},
        ...     'three': {'one': 0.1, 'two': 0.2, 'three': 0.7}
        ... }
        >>> chain = evans.MarkovChain(transition_prob=prob)
        >>> key_list = [
        ...     x for x in chain.generate_states(
        ...         current_state='one', no=14
        ...         )
        ...     ]
        >>> key_list
        ['one', 'one', 'one', 'one', 'two', 'two', 'two', 'one', 'one', 'one', 'one', 'two', 'two', 'one']

    """

    def __init__(self, transition_prob):
        self.transition_prob = transition_prob
        self.states = list(transition_prob.keys())

    def __str__(self):
        return abjad.storage(self)

    def __repr__(self):
        return abjad.storage(self)

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


def add_sequences(x, y):
    """

    .. container:: example

        >>> seq_1 = [0, 1, 2, 3]
        >>> seq_2 = [4, 5, 6, 7, 8]
        >>> evans.add_sequences(seq_1, seq_2)
        [4, 6, 8, 10]

    .. container:: example

        >>> seq_1 = [0, 1, 2, 3, 4]
        >>> seq_2 = [5, 6, 7, 8]
        >>> evans.add_sequences(seq_1, seq_2)
        [5, 7, 9, 11, 9]

    """
    returned_sequence = []
    cyc_y = CyclicList(y, forget=False)
    for _ in x:
        y_val = cyc_y(r=1)[0]
        returned_sequence.append(_ + y_val)
    return returned_sequence


def cyc(lst):
    """

    .. container:: example

        >>> cyc_list = evans.cyc([0, 1, 2])
        >>> for _ in range(5):
        ...     print(next(cyc_list))
        ...
        0
        1
        2
        0
        1

    """
    count = -1
    while True:
        count += 1
        yield lst[count % len(lst)]


def derive_added_sequences(x, y, flat=False):
    """

    .. container:: example

        >>> seq_1 = [0, 1, 2, 3]
        >>> seq_2 = [4, 5, 6, 7, 8]
        >>> for _ in evans.derive_added_sequences(seq_1, seq_2):
        ...     _
        ...
        [4, 5, 6, 7]
        [5, 6, 7, 8]
        [6, 7, 8, 9]
        [7, 8, 9, 10]
        [8, 9, 10, 11]

    .. container:: example

        >>> seq_1 = [0, 1, 2, 3, 4]
        >>> seq_2 = [5, 6, 7, 8]
        >>> for _ in evans.derive_added_sequences(seq_1, seq_2):
        ...     _
        ...
        [5, 6, 7, 8, 9]
        [6, 7, 8, 9, 10]
        [7, 8, 9, 10, 11]
        [8, 9, 10, 11, 12]

    .. container:: example

        >>> seq_1 = [0, 1, 2, 3, 4]
        >>> seq_2 = [5, 6, 7, 8]
        >>> evans.derive_added_sequences(seq_1, seq_2, flat=True)
        [5, 6, 7, 8, 9, 6, 7, 8, 9, 10, 7, 8, 9, 10, 11, 8, 9, 10, 11, 12]

    """
    returned_sequence = []
    for val in y:
        transposition = []
        for val_ in x:
            transposition.append(val + val_)
        returned_sequence.append(transposition)
    if flat is True:
        returned_sequence = flatten(returned_sequence)
    return returned_sequence


def derive_multiplied_sequences(x, y, flat=False):
    """

    .. container:: example

        >>> seq_1 = [0, 1, 2, 3]
        >>> seq_2 = [4, 5, 6, 7, 8]
        >>> for _ in evans.derive_multiplied_sequences(seq_1, seq_2):
        ...     _
        ...
        [0, 4, 8, 12]
        [0, 5, 10, 15]
        [0, 6, 12, 18]
        [0, 7, 14, 21]
        [0, 8, 16, 24]

    .. container:: example

        >>> seq_1 = [0, 1, 2, 3, 4]
        >>> seq_2 = [5, 6, 7, 8]
        >>> for _ in evans.derive_multiplied_sequences(seq_1, seq_2):
        ...     _
        ...
        [0, 5, 10, 15, 20]
        [0, 6, 12, 18, 24]
        [0, 7, 14, 21, 28]
        [0, 8, 16, 24, 32]

    .. container:: example

        >>> seq_1 = [0, 1, 2, 3, 4]
        >>> seq_2 = [5, 6, 7, 8]
        >>> evans.derive_multiplied_sequences(seq_1, seq_2, flat=True)
        [0, 5, 10, 15, 20, 0, 6, 12, 18, 24, 0, 7, 14, 21, 28, 0, 8, 16, 24, 32]

    """
    returned_sequence = []
    for val in y:
        transposition = []
        for val_ in x:
            transposition.append(val * val_)
        returned_sequence.append(transposition)
    if flat is True:
        returned_sequence = flatten(returned_sequence)
    return returned_sequence


def e_bonacci_cycle(n, iters, first, second, modulus, wrap_to_zero=False):
    """

    .. container:: example

        >>> print(evans.e_bonacci_cycle(n=3, iters=15, first=1, second=1, modulus=7))
        [1, 1, 2, 4, 7, 6, 3, 2, 4, 2, 1, 7, 3]

    """
    final = [0] * iters
    final[n - 1] = first
    final[n] = second
    for i, slot in enumerate(final[n + 1 :]):
        i = i + n + 1
        dist = n + 1
        bound = i - dist
        sum = 0
        for x in final[i - 1 : bound : -1]:
            sum = sum + x
        final[i] = sum
    for _ in range(n - 1):
        final.remove(0)
    sequence = [(_ % modulus) for _ in final]
    if wrap_to_zero is False:
        for index, item in enumerate(sequence):
            if item == 0:
                sequence[index] = item + modulus
    return sequence


def e_dovan_cycle(n, iters, first, second, modulus, wrap_to_zero=False):
    """

    .. container:: example

        >>> print(evans.e_dovan_cycle(n=3, iters=15, first=1, second=1, modulus=7))
        [1, 1, 1, 2, 3, 4, 6, 2, 6, 5, 7, 6, 4]

    """
    iters = iters + 1
    final = [0] * iters
    final[n] = first
    final[n + 1] = second
    for i, slot in enumerate(final[n + 2 :]):
        i = i + n + 2
        dist = n + 2
        bound = i - dist
        sum = 0
        for x in final[i - 2 : bound : -1]:
            sum = sum + x
        final[i] = sum
    for _ in range(n):
        final.remove(0)
    sequence = [(_ % modulus) for _ in final]
    if wrap_to_zero is False:
        for index, item in enumerate(sequence):
            if item == 0:
                sequence[index] = item + modulus
    return sequence


def feigenbaum_bifurcations(fertility=3.59785, initial_state=0.5, iterations=10):
    """

    .. container:: example

        >>> print(evans.feigenbaum_bifurcations(fertility= 2.3, initial_state=0.5, iterations=4))
        [0.5, 0.575, 0.5620625, 0.5661409660156249, 0.5649383570133959]

    """
    list_ = [initial_state]
    for _ in range(iterations):
        front = fertility * initial_state
        back = 1 - initial_state
        next_state = front * back
        list_.append(next_state)
        initial_state = next_state
    return list_


def flatten(lst):
    """

    .. container:: example

        >>> nested_list = [1, 1, [1, [1, 1]], 1]
        >>> flat = evans.flatten(nested_list)
        >>> print(flat)
        [1, 1, 1, 1, 1, 1]

    """
    out = []
    for i in lst:
        if isinstance(i, list):
            out.extend(flatten(i))
        else:
            out.append(i)
    return out


def grouper(lst1, lst2):
    """

    .. container:: example

        >>> print(evans.grouper([0, 1, 2, 3, 4, 5, 6, 7], [1, 1, 2, 1, 3]))
        [0, 1, [2, 3], 4, [5, 6, 7]]

    """

    def cyc(lst):
        c = 0
        while True:
            yield lst[c % len(lst)]
            c += 1

    lst1 = cyc(lst1)
    return [next(lst1) if i == 1 else [next(lst1) for _ in range(i)] for i in lst2]


def guerrero_morales(terms=None, set_size=None):
    """

    .. container:: example

        >>> g_m = evans.guerrero_morales(
        ...     [
        ...         "A",
        ...         "B",
        ...         "C",
        ...         "D",
        ...         "E",
        ...         "F",
        ...         "G",
        ...     ],
        ...     3,
        ... )
        >>> for _ in g_m:
        ...     _
        ...
        ['A', 'B', 'C']
        ['B', 'D', 'E']
        ['C', 'D', 'F']
        ['A', 'D', 'G']
        ['A', 'E', 'F']
        ['B', 'F', 'G']
        ['C', 'E', 'G']

    .. container:: example

        >>> for _ in evans.guerrero_morales("ABCDEFGHI", 5):
        ...     _
        ...
        ['A', 'B', 'C', 'D', 'E']
        ['B', 'F', 'G', 'H', 'I']

    .. container:: example

        >>> for _ in evans.guerrero_morales("ABCDEFGHIJKLMNO", 4):
        ...     _
        ...
        ['A', 'B', 'C', 'D']
        ['B', 'E', 'F', 'G']
        ['C', 'E', 'H', 'I']
        ['D', 'E', 'J', 'K']
        ['A', 'E', 'L', 'M']
        ['A', 'F', 'H', 'J']
        ['A', 'G', 'I', 'K']
        ['B', 'H', 'K', 'L']
        ['B', 'I', 'J', 'M']
        ['C', 'G', 'J', 'L']
        ['C', 'F', 'K', 'M']
        ['D', 'F', 'I', 'L']
        ['D', 'G', 'H', 'M']

    .. container:: example

        >>> for _ in evans.guerrero_morales("ABCDEFGHI", 3):
        ...     _
        ...
        ['A', 'B', 'C']
        ['B', 'D', 'E']
        ['C', 'D', 'F']
        ['A', 'D', 'G']
        ['A', 'E', 'F']
        ['B', 'F', 'G']
        ['C', 'E', 'G']
        ['A', 'H', 'I']

    """
    returned_list = []
    combinations = [_ for _ in itertools.combinations(terms, set_size)]
    pairs_list = []
    for term in terms:
        temp_pairs_list = []
        temp_returned_list = []
        term_relevant_sets = [s for s in combinations if term in s]
        for term_relevant_set in term_relevant_sets:
            pairs = [x + y for x, y in itertools.combinations(term_relevant_set, 2)]
            val = [_ in pairs_list for _ in pairs]
            if not any(val):
                temp_pairs_list.append(pairs)
                temp_returned_list.append(term_relevant_set)
        if 0 < len(temp_pairs_list):
            pairs_list.extend(temp_pairs_list[0])
            returned_list.append(list(temp_returned_list[0]))
    return returned_list


def harmonic_series(fundamental=20, number_of_partials=10, invert=False):
    """

    .. container:: example

        >>> print(evans.harmonic_series(20, 5))
        [20, 40, 60, 80, 100]

    .. container:: example

        >>> print(evans.harmonic_series(900, 5, True))
        [900.0, 450.0, 300.0, 225.0, 180.0]

    """
    returned_list = []
    for _ in range(number_of_partials):
        multiplier = _ + 1
        if invert is False:
            returned_list.append(fundamental * multiplier)
        else:
            returned_list.append(fundamental / multiplier)
    return returned_list


def hexagonal_sequence(n_list=[1]):
    """

    .. container:: example

        >>> seq = evans.hexagonal_sequence(n_list=[_ for _ in range(8)])
        >>> print(seq)
        [0, 1, 6, 15, 28, 45, 66, 91]

    """
    seq = []
    for n in n_list:
        x = n * (2 * n - 1)
        seq.append(x)
    return seq


def josephus(n, k):
    """

    .. container:: example

        >>> tone_row = [0, 1, 2, 3, 4]
        >>> for i in range(16):
        ...     print(
        ...         evans.josephus(len(tone_row), i + 2)
        ...     )
        ...
        [[0, 1, 2, 3, 4], [0, 2, 3, 4], [0, 2, 4], [2, 4], [2]]
        [[0, 1, 2, 3, 4], [0, 1, 3, 4], [1, 3, 4], [1, 3], [3]]
        [[0, 1, 2, 3, 4], [0, 1, 2, 4], [0, 1, 4], [0, 1], [0]]
        [[0, 1, 2, 3, 4], [0, 1, 2, 3], [1, 2, 3], [1, 3], [1]]
        [[0, 1, 2, 3, 4], [1, 2, 3, 4], [1, 3, 4], [3, 4], [3]]
        [[0, 1, 2, 3, 4], [0, 2, 3, 4], [0, 2, 3], [2, 3], [3]]
        [[0, 1, 2, 3, 4], [0, 1, 3, 4], [0, 3, 4], [0, 3], [0]]
        [[0, 1, 2, 3, 4], [0, 1, 2, 4], [0, 1, 2], [0, 1], [1]]
        [[0, 1, 2, 3, 4], [0, 1, 2, 3], [0, 2, 3], [0, 3], [3]]
        [[0, 1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 4], [2, 4], [4]]
        [[0, 1, 2, 3, 4], [0, 2, 3, 4], [2, 3, 4], [2, 3], [2]]
        [[0, 1, 2, 3, 4], [0, 1, 3, 4], [0, 1, 4], [0, 1], [1]]
        [[0, 1, 2, 3, 4], [0, 1, 2, 4], [1, 2, 4], [1, 4], [4]]
        [[0, 1, 2, 3, 4], [0, 1, 2, 3], [0, 1, 3], [0, 3], [0]]
        [[0, 1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3], [2, 3], [2]]
        [[0, 1, 2, 3, 4], [0, 2, 3, 4], [0, 3, 4], [0, 3], [3]]

    """
    p, i, seq = list(range(n)), 0, []
    while p:
        i = (i + k - 1) % len(p)
        seq.append(p.pop(i))
    sequences = [list(range(n))]
    for _ in seq:
        next = [x for x in sequences[-1]]
        next.remove(_)
        sequences.append(next)
    return sequences[:-1]


def lindenmayer(seed, rules, iters):
    """

    .. container:: example

        >>> rule_dict = { "A": "ABA" , "B": "BC", "C": "BAC"}
        >>> lind_list = [_ for _ in evans.lindenmayer(seed='AB', rules=rule_dict, iters=2)]
        >>> print(lind_list)
        ['A', 'B', 'A', 'B', 'C', 'A', 'B', 'A', 'B', 'C', 'B', 'A', 'C']

    """
    for _ in range(iters):
        result = ""
        for axiom in seed:
            if axiom in rules:
                result += rules[axiom]
            else:
                result += axiom
        seed = result
    return seed


def mirror(lst, sequential_duplicates):
    """

    .. container:: example

        >>> print(
        ...     evans.mirror(
        ...         [0, 1, 2, 3],
        ...         sequential_duplicates=True,
        ...     )
        ... )
        [0, 1, 2, 3, 3, 2, 1, 0]

    .. container:: example

        >>> print(
        ...     evans.mirror(
        ...         [0, 1, 2, 3],
        ...         sequential_duplicates=False,
        ...     )
        ... )
        [0, 1, 2, 3, 2, 1]

    """
    if sequential_duplicates is False:
        return lst + lst[-2:0:-1]
    else:
        return lst + lst[::-1]


def mod(sequence, modulus, indices=False):
    """

    .. container:: example

        >>> mod_seq = evans.mod(sequence=[7, 8, 9, 10], modulus=7)
        >>> print(mod_seq)
        [7, 1, 2, 3]

    """
    new_seq = [(_ % modulus) for _ in sequence]
    for i, _ in enumerate(new_seq):
        if indices is False:
            if _ == 0:
                new_seq[i] = _ + modulus
            else:
                continue
        else:
            continue
    return new_seq


def multiple_sequence(fundamental=20, number_of_partials=10, multiple=1.5):
    """

    .. container:: example

        >>> print(evans.multiple_sequence(20, 10, 1.25))
        [20.0, 25.0, 31.25, 39.0625, 48.828125, 61.03515625, 76.2939453125, 95.367431640625, 119.20928955078125, 149.01161193847656, 186.2645149230957]

    """
    returned_list = [float(fundamental)]
    for _ in range(number_of_partials):
        returned_list.append(returned_list[-1] * multiple)
    return returned_list


def multiply_all(list_of_numbers):
    x = 1
    for _ in list_of_numbers:
        x *= _
    return x


def multiply_sequences(x, y):
    """

    .. container:: example

        >>> seq_1 = [0, 1, 2, 3]
        >>> seq_2 = [4, 5, 6, 7, 8]
        >>> evans.multiply_sequences(seq_1, seq_2)
        [0, 5, 12, 21]

    .. container:: example

        >>> seq_1 = [0, 1, 2, 3, 4]
        >>> seq_2 = [5, 6, 7, 8]
        >>> evans.multiply_sequences(seq_1, seq_2)
        [0, 6, 14, 24, 20]

    """
    returned_sequence = []
    cyc_y = CyclicList(y, forget=False)
    for _ in x:
        y_val = cyc_y(r=1)[0]
        returned_sequence.append(_ * y_val)
    return returned_sequence


def n_bonacci_cycle(
    n, first_number, second_number, length, modulus, wrap_to_zero=False
):
    """

    .. container:: example

        >>> print(evans.n_bonacci_cycle(n=3, first_number=1, second_number=3, length=8, modulus=7))
        [1, 3, 3, 5, 4, 3, 6, 7, 6, 4]

    """
    sequence = [first_number, second_number]
    for _ in range(length):
        sequence.append(sequence[-2] + (sequence[-1] * n))
    sequence = [(_ % modulus) for _ in sequence]
    if wrap_to_zero is False:
        for index, item in enumerate(sequence):
            if item == 0:
                sequence[index] = item + modulus
    return sequence


def normalize_sum(integer_list, desired_sum=1):
    """

    .. container:: example

        >>> weights = [15, 6, 14, 4, 16, 6, 14, 4, 16, 5]
        >>> print(evans.normalize_sum(integer_list=weights, desired_sum=1))
        [0.15, 0.06, 0.14, 0.04, 0.16, 0.06, 0.14, 0.04, 0.16, 0.05]

    """
    sum = 0
    for _ in integer_list:
        sum = sum + _ / desired_sum
    normalized_list = []
    for _ in integer_list:
        normalized_list.append(_ / sum)
    return normalized_list


def normalize_to_indices(raw_list=[1, 0.24, -12, [-4, 0.7], -0.5]):
    """

    .. container:: example

        >>> print(evans.normalize_to_indices(raw_list=[1, 0.24, -12, [-4, 0.7], -0.5]))
        [4, 1, -50, [-5, 1], -2]

    """
    out = []
    flat_raw = [abs(float(_)) for _ in flatten(raw_list)]
    minimum_value = min(flat_raw)
    if minimum_value == 0:
        minimum_value = 0.000001
    for _ in raw_list:
        if isinstance(_, list):
            out.append(normalize_to_indices(_))
        else:
            out.append(int(float(_) / minimum_value))
    return out


def orbits(initial_state=0.4, iterations=10):
    """

    .. container:: example

        >>> print(evans.orbits(initial_state=0.4, iterations=5))
        [0.96, 0.15360000000000013, 0.5200281600000003, 0.9983954912280576, 0.006407737294172653]

    """
    list_ = []
    for _ in range(iterations):
        front = 4 * initial_state
        back = 1 - initial_state
        next_state = front * back
        list_.append(next_state)
        initial_state = next_state
    return list_


def perm(lst):
    """

    .. container:: example

        >>> print(evans.perm([0, 1, 2]))
        [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]

    """
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return [lst]
    else:
        list_ = []
        for i in range(len(lst)):
            x = lst[i]
            ba = lst[:i] + lst[i + 1 :]
            for p in perm(ba):
                list_.append([x] + p)
        return list_


def pitch_warp(
    warp_values=[0.5, -0.5], pitch_list=[0, 1, 2, 3, 4], boolean_vector=[0, 1, 1]
):
    warp_count = -1
    bool_count = -1
    w = CyclicList(warp_values, count=warp_count, forget=False)
    b = CyclicList(boolean_vector, count=bool_count, forget=False)
    bool_values = b(r=len(pitch_list))
    pairs = zip(bool_values, pitch_list)
    for i, pair in enumerate(pairs):
        if pair[0] == 1:
            if isinstance(pair[1], list):
                for p, _ in enumerate(pitch_list[i]):
                    warp_value = w(r=1)[0]
                    pitch_list[i][p] = pitch_list[i][p] + warp_value
            else:
                warp_value = w(r=1)[0]
                pitch_list[i] = pitch_list[i] + warp_value
    return pitch_list


def prime_sequence(start, end):
    """

    .. container:: example

        >>> primes = evans.prime_sequence(start=11, end=25)
        >>> print(primes)
        [11, 13, 15, 17, 19, 21, 23, 25]

    """
    seq = []
    for val in range(start, end + 1):
        if val > 1:
            for n in range(2, val):
                if (val % n) == 0:
                    break
                else:
                    if val not in seq:
                        seq.append(val)
                    else:
                        continue
    return seq


def prism_sequence(n_list=[1]):
    """

    .. container:: example

        >>> seq = evans.prism_sequence(n_list=[_ for _ in range(8)])
        >>> print(seq)
        [1, 14, 57, 148, 305, 546, 889, 1352]

    """
    seq = []
    for n in n_list:
        x = (n + 1) * (3 * n ** 2 + 3 * n + 1)
        seq.append(x)
    return seq


def random_walk(random_seed, length, step_list, mapped_list):
    """

    .. container:: example

        >>> walk = evans.random_walk(
        ...     random_seed=1,
        ...     length=5,
        ...     step_list=[1, 2, 1],
        ...     mapped_list=[_ for _ in range(10)],
        ... )
        >>> print(walk)
        [0, 9, 0, 2, 1, 0]

    """
    random.seed(random_seed)
    if step_list is not None:
        step = cyc(step_list)
    walk = []
    walk.append(-1 if random.random() < 0.5 else 1)
    for i in range(1, length):
        if step_list is not None:
            next_step = next(step)
            movement = -next_step if random.random() < 0.5 else next_step
        else:
            movement = -1 if random.random() < 0.5 else 1
        value = walk[i - 1] + movement
        walk.append(value)
    input_list = mapped_list
    list_ = len(input_list)
    final_list = [input_list[0]]
    final_list.extend([input_list[x] for x in reduce_mod(list_, walk)])
    return final_list


def recaman_sequence(number):
    """

    .. container:: example

        >>> rec_seq = [evans.recaman_sequence(number=_ + 1) for _ in range(10)]
        >>> print(rec_seq)
        [1, 3, 6, 2, 7, 1, 8, 16, 7, 17]

    """
    temp_list = []
    if number == 1:
        temp_list.append(number)
        return number
    else:
        a = recaman_sequence(number - 1)
        am = a - number
        ap = a + number
        if am > 0 and am not in temp_list:
            temp_list.append(am)
            return am
        else:
            temp_list.append(ap)
            return ap


def reciprocal(value):
    """

    .. container:: example

        >>> print(evans.reciprocal(0.5))
        2.0

    """
    return 1 / value


def reduce_mod(x, rw):
    """

    .. container:: example

        >>> mod_list = evans.reduce_mod(5, [0, 1, 2, 3, 4, 5, 6, 7, 8])
        >>> print(mod_list)
        [0, 1, 2, 3, 4, 0, 1, 2, 3]

    """
    return [(y % x) for y in rw]


def reproportion_chord(base, chord, round=None):
    """

    .. container:: example

        >>> rounder = evans.to_nearest_eighth_tone
        >>> print(
        ...     evans.reproportion_chord(
        ...         base=2,
        ...         chord=[-24, -20, -15, -14, -4, 5, 11, 19, 26, 37, 39, 42],
        ...         round=rounder,
        ...     )
        ... )
        [-4.75, -4, -3, -2.75, -0.75, 1, 2.25, 3.75, 5.25, 7.5, 7.75, 8.5]

    """
    base_converter = base / 10.0
    collection = []
    for _ in chord:
        collection.append(_ * base_converter)
    if round is not None:
        collection = [round(_) for _ in collection]
    return collection


def reproportion_chromatic_decimals(base, root_int, scale_range, round=None):
    """

    .. container:: example

        >>> rounder = evans.to_nearest_eighth_tone
        >>> print(
        ...     evans.reproportion_chromatic_decimals(
        ...         base=10, root_int=0, scale_range=12, round=rounder,
        ...     )
        ... )
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    """
    base_converter = base / 10.0
    octave = root_int + 12
    converted_octave = octave * base_converter
    collection = [root_int]
    step = converted_octave / 12
    for _ in range(scale_range):
        collection.append(collection[-1] + step)
    if round is not None:
        collection = [round(_) for _ in collection]
    return collection


def reproportion_harmonics(fund, scale, return_amp_reciprocals=None):
    """

    .. container:: example

        >>> print(
        ...     evans.reproportion_harmonics(
        ...         fund=20, scale=[(_ + 1) for _ in range(5)], return_amp_reciprocals='as_tuples'
        ...     )
        ... )
        [(20, 1), (20, 1.0), (40, 0.5), (60, 0.3333333333333333), (80, 0.25), (100, 0.2)]

    .. container:: example

        >>> print(
        ...     evans.reproportion_harmonics(
        ...         fund=20, scale=[(_ + 1) for _ in range(5)], return_amp_reciprocals='as_lists'
        ...     )
        ... )
        ([20, 20, 40, 60, 80, 100], [1, 1.0, 0.5, 0.3333333333333333, 0.25, 0.2])

    .. container:: example

        >>> print(
        ...     evans.reproportion_harmonics(
        ...         fund=20, scale=[(_ + 1) for _ in range(5)],
        ...     )
        ... )
        [20, 20, 40, 60, 80, 100]

    """
    calculated_series = [_ * fund for _ in scale]
    final_series = [fund]
    final_series.extend(calculated_series)
    if return_amp_reciprocals == "as_tuples":
        return [
            (harmonic, amp)
            for harmonic, amp in zip(final_series, _return_amplitude_reciprocals(scale))
        ]
    elif return_amp_reciprocals == "as_lists":
        return final_series, _return_amplitude_reciprocals(scale)
    else:
        return final_series


def reproportion_scale(base, limit):
    """

    .. container:: example

        >>> insert_scale = (evans.reproportion_scale(base=15, limit=17))
        >>> print(insert_scale)
        [3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5, 15.0, 16.5, 18.0, 19.5, 21.0, 22.5, 24.0, 25.5]

    """
    step = base / 10.0
    end = limit + 1
    scale = [_ for _ in range(2, end)]
    new_scale = [_ * step for _ in scale]
    return new_scale


def _return_amplitude_reciprocals(rescaled_scale):
    reciprocal_list = [1]
    for _ in rescaled_scale:
        reciprocal_list.append(reciprocal(_))
    return reciprocal_list


def rotate(lst, n):
    """

    .. container:: example

        >>> print(evans.rotate([0, 1, 2, 3], 2))
        [2, 3, 0, 1]

    """
    return lst[n:] + lst[:n]


def warp(min, max, random_seed, warped_list, by_integers=False):
    """

    .. container:: example

        >>> print(evans.warp(-0.5, 0.5, 3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
        [-0.26203537290810863, 1.0442292252959517, 1.8699551665480794, 3.1039200385961943, 4.125720304108054, 4.565528859239813, 5.513167991554874, 7.33746908209646, 7.759354014328007, 8.734330961046696]

    .. container:: example

        >>> print(evans.warp(-1, 1, 3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], by_integers=True))
        [-1, 2, 3, 2, 4, 6, 6, 8, 9, 8]

    """
    random.seed(random_seed)
    final_list = []
    if by_integers is True:
        perturbation_list = [random.randint(min, max) for _ in warped_list]
    else:
        perturbation_list = [random.uniform(min, max) for _ in warped_list]
    for x, y in zip(warped_list, perturbation_list):
        final_list.append(x + y)
    return final_list
