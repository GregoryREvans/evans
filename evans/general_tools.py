import itertools
import re
from random import randint, random, seed, uniform

from .abjad_functions.pitch_rounding import to_nearest_eighth_tone


def cyc(lst):
    """
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


def e_bonacci_cycle(n, iters, first, second, modulus, wrap_to_zero=False):
    """
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


def hexagonal_sequence(n_list=[1]):
    """
    >>> seq = evans.hexagonal_sequence(n_list=[_ for _ in range(8)])
    >>> print(seq)
    [0, 1, 6, 15, 28, 45, 66, 91]

    """
    seq = []
    for n in n_list:
        x = n * (2 * n - 1)
        seq.append(x)
    return seq


def lindenmayer(seed, rules, iters):
    """
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
    >>> print(
    ...     evans.mirror(
    ...         [0, 1, 2, 3],
    ...         sequential_duplicates=True,
    ...     )
    ... )
    ...
    [0, 1, 2, 3, 3, 2, 1, 0]

    >>> print(
    ...     evans.mirror(
    ...         [0, 1, 2, 3],
    ...         sequential_duplicates=False,
    ...     )
    ... )
    ...
    [0, 1, 2, 3, 2, 1]

    """
    if sequential_duplicates is False:
        return lst + lst[-2:0:-1]
    else:
        return lst + lst[::-1]


def mod(sequence, modulus, indices=False):
    """
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


def n_bonacci_cycle(
    n, first_number, second_number, length, modulus, wrap_to_zero=False
):
    """
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


def prime_sequence(start, end):
    """
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
    >>> walk = evans.random_walk(
    ...     random_seed=1,
    ...     length=5,
    ...     step_list=[1, 2, 1],
    ...     mapped_list=[_ for _ in range(10)],
    ... )
    ...
    >>> print(walk)
    [0, 9, 0, 2, 1, 0]

    """
    seed(random_seed)
    if step_list is not None:
        step = cyc(step_list)
    walk = []
    walk.append(-1 if random() < 0.5 else 1)
    for i in range(1, length):
        if step_list is not None:
            next_step = next(step)
            movement = -next_step if random() < 0.5 else next_step
        else:
            movement = -1 if random() < 0.5 else 1
        value = walk[i - 1] + movement
        walk.append(value)
    input_list = mapped_list
    list_ = len(input_list)
    final_list = [input_list[0]]
    final_list.extend([input_list[x] for x in reduce_mod(list_, walk)])
    return final_list


def recaman_sequence(number):
    """
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
    >>> print(reciprocal(0.5))
    2.0

    """
    return 1 / value


def reduce_mod(x, rw):
    """
    >>> mod_list = evans.reduce_mod(5, [0, 1, 2, 3, 4, 5, 6, 7, 8])
    >>> print(mod_list)
    [0, 1, 2, 3, 4, 0, 1, 2, 3]

    """
    return [(y % x) for y in rw]


def reproportion_chord(base, chord, round=False):
    """
    >>> print(
    ...     evans.reproportion_chord(
    ...         base=2,
    ...         chord=[-24, -20, -15, -14, -4, 5, 11, 19, 26, 37, 39, 42],
    ...         round=True
    ...     )
    ... )
    ...
    [-4.75, -4, -3, -2.75, -0.75, 1, 2.25, 3.75, 5.25, 7.5, 7.75, 8.5]

    """
    base_converter = base / 10.0
    collection = []
    for _ in chord:
        collection.append(_ * base_converter)
    if round is True:
        collection = [to_nearest_eighth_tone(_) for _ in collection]
    return collection


def reproportion_chromatic_decimals(base, root_int, scale_range, round=False):
    """
    >>> print(
    ...     evans.reproportion_chromatic_decimals(
    ...         base=10, root_int=0, scale_range=12, round=True
    ...     )
    ... )
    ...
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    """
    base_converter = base / 10.0
    octave = root_int + 12
    converted_octave = octave * base_converter
    collection = [root_int]
    step = converted_octave / 12
    for _ in range(scale_range):
        collection.append(collection[-1] + step)
    if round is True:
        collection = [to_nearest_eighth_tone(_) for _ in collection]
    return collection


def reproportion_harmonics(fund, scale, return_amp_reciprocals=None):
    """
    >>> print(
    ...     reproportion_harmonics(
    ...         fund=20, scale=[(_ + 1) for _ in range(5)], return_amp_reciprocals='as_tuples'
    ...     )
    ... )
    ...
    [(20, 1), (20, 1.0), (40, 0.5), (60, 0.3333333333333333), (80, 0.25), (100, 0.2)]

    >>> print(
    ...     reproportion_harmonics(
    ...         fund=20, scale=[(_ + 1) for _ in range(5)], return_amp_reciprocals='as_lists'
    ...     )
    ... )
    ...
    ([20, 20, 40, 60, 80, 100], [1, 1.0, 0.5, 0.3333333333333333, 0.25, 0.2])

    >>> print(
    ...     reproportion_harmonics(
    ...         fund=20, scale=[(_ + 1) for _ in range(5)],
    ...     )
    ... )
    ...
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
    >>> print(evans.rotate([0, 1, 2, 3], 2))
    [2, 3, 0, 1]

    """
    return lst[n:] + lst[:n]


def set_net(set, group_size, filter_depth):
    r"""
    >>> filter_depth_ = 7
    >>> set_ = "ABCDEFG"
    >>> group_size_ = 3
    >>> net = evans.set_net(set=set_, group_size=group_size_, filter_depth=filter_depth_)
    >>> print(net)
    [('A', 'B', 'C'), ('A', 'D', 'E'), ('A', 'F', 'G'), ('B', 'D', 'F'), ('B', 'E', 'G'), ('C', 'D', 'G'), ('C', 'E', 'F')]

    >>> filter_depth_ = 3
    >>> set_ = "ABCDEFGHI"
    >>> group_size_ = 4
    >>> net = evans.set_net(set=set_, group_size=group_size_, filter_depth=filter_depth_)
    >>> print(net)
    [('A', 'B', 'C', 'D'), ('A', 'E', 'F', 'G'), ('B', 'E', 'H', 'I')]

    >>> filter_depth_ = 2
    >>> set_ = "ABCDE"
    >>> group_size_ = 3
    >>> net = evans.set_net(set=set_, group_size=group_size_, filter_depth=filter_depth_)
    >>> print(net)
    [('A', 'B', 'C'), ('A', 'D', 'E')]

    """
    combination_sets = [_ for _ in itertools.combinations(set, group_size)]
    for i, letter in enumerate(range(filter_depth)):
        reference_set = combination_sets[i]
        for index, item in enumerate(reference_set):
            for set_class in combination_sets[i + 1 :]:
                if item in set_class:
                    checkable_set = [_ for _ in reference_set]
                    checkable_set.remove(item)
                    for check in checkable_set:
                        if set_class in combination_sets:
                            if check in set_class:
                                combination_sets.remove(set_class)
                            else:
                                continue
                        else:
                            continue
                else:
                    continue
    return combination_sets


def to_digit(string):
    """
    >>> evans.to_digit("2")
    2

    """
    return int(string) if string.isdigit() else string


def sorted_keys(text):
    """
    >>> evans.sorted_keys("Voice 1")
    ['Voice ', 1, '']

    """
    return [to_digit(_) for _ in re.split(r"(\d+)", text)]


def warp(min, max, random_seed, warped_list, by_integers=False):
    """
    >>> print(evans.warp(-0.5, 0.5, 3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    [-0.26203537290810863, 1.0442292252959517, 1.8699551665480794, 3.1039200385961943, 4.125720304108054, 4.565528859239813, 5.513167991554874, 7.33746908209646, 7.759354014328007, 8.734330961046696]

    >>> print(evans.warp(-1, 1, 3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], by_integers=True))
    [-1, 2, 3, 2, 4, 6, 6, 8, 9, 8]

    """
    seed(random_seed)
    final_list = []
    if by_integers is True:
        perturbation_list = [randint(min, max) for _ in warped_list]
    else:
        perturbation_list = [uniform(min, max) for _ in warped_list]
    for x, y in zip(warped_list, perturbation_list):
        final_list.append(x + y)
    return final_list
