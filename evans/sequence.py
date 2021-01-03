"""
Sequence classes and functions.
"""
import decimal
import itertools
import math
import random

import abjad
import baca
import numpy
import quicktions
import scipy
from abjadext import microtones
from scipy.integrate import odeint


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


class PitchClassSet(microtones.PitchClassSet):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.pitch_classes])
        return seq


class PitchSet(microtones.PitchSet):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.pitches])
        return seq


class PitchClassSegment(microtones.PitchClassSegment):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.pitch_classes])
        return seq


class PitchSegment(microtones.PitchSegment):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.pitches])
        return seq


class RatioClassSet(microtones.RatioClassSet):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.ratio_classes])
        return seq


class RatioSet(microtones.RatioSet):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.ratios])
        return seq


class RatioClassSegment(microtones.RatioClassSegment):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.ratio_classes])
        return seq


class RatioSegment(microtones.RatioSegment):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.ratios])
        return seq


class Ratio(abjad.Ratio):
    def extract_sub_ratios(self, reciprocal=False, as_fractions=False):
        """

        .. container:: example

            >>> ratio = evans.Ratio('9:8:7:6:5:4:3:2')
            >>> ratio.extract_sub_ratios()
            Sequence([Ratio((1, 1)), Ratio((3, 2)), Ratio((2, 1)), Ratio((5, 2)), Ratio((3, 1)), Ratio((7, 2)), Ratio((4, 1)), Ratio((9, 2))])

        .. container:: example

            >>> ratio = evans.Ratio('9:8:7:6:5:4:3:2')
            >>> ratio.extract_sub_ratios(reciprocal=True)
            Sequence([Ratio((1, 1)), Ratio((2, 3)), Ratio((1, 2)), Ratio((2, 5)), Ratio((1, 3)), Ratio((2, 7)), Ratio((1, 4)), Ratio((2, 9))])

        .. container:: example

            >>> ratio = evans.Ratio('9:8:7:6:5:4:3:2')
            >>> ratio.extract_sub_ratios(as_fractions=True)
            Sequence([Fraction(1, 1), Fraction(3, 2), Fraction(2, 1), Fraction(5, 2), Fraction(3, 1), Fraction(7, 2), Fraction(4, 1), Fraction(9, 2)])

        .. container:: example

            >>> ratio = evans.Ratio('9:8:7:6:5:4:3:2')
            >>> ratio.extract_sub_ratios(reciprocal=True, as_fractions=True)
            Sequence([Fraction(1, 1), Fraction(2, 3), Fraction(1, 2), Fraction(2, 5), Fraction(1, 3), Fraction(2, 7), Fraction(1, 4), Fraction(2, 9)])

        ..  todo::  consider using abjad.Ratio in abjadext.microtones?

        """
        returned_list = [abjad.Ratio((_, self.numbers[-1])) for _ in self.numbers[::-1]]
        if reciprocal:
            returned_list = [_.reciprocal for _ in returned_list]
        if as_fractions:
            returned_list = [
                quicktions.Fraction(_.numbers[0], _.numbers[1]) for _ in returned_list
            ]
        return Sequence(returned_list)


class Sequence(baca.Sequence):
    """

    .. todo:: add pitch and ratio operations from abjadext.microtones?

    .. todo:: add some sequence functions to sequence class with optional recursion?

    """

    def add_sequences(self, seq):
        """

        .. container:: example

            >>> s = evans.Sequence([0, 1, 2, 3])
            >>> s.add_sequences([4, 5, 6, 7, 8])
            Sequence([4, 6, 8, 10])

        .. container:: example

            >>> s = evans.Sequence([0, 1, 2, 3, 4])
            >>> s.add_sequences([5, 6, 7, 8])
            Sequence([5, 7, 9, 11, 9])

        """
        x = [_ for _ in self.items]
        returned_sequence = []
        cyc_y = CyclicList(seq, forget=False)
        for _ in x:
            y_val = cyc_y(r=1)[0]
            returned_sequence.append(_ + y_val)
        return Sequence(returned_sequence)

    def combination_addition(self, size=2):
        """

        .. container:: example

            >>> import quicktions
            >>> l = [2, 3, 4]
            >>> l = [quicktions.Fraction(_) for _ in l]
            >>> evans.Sequence(l).combination_addition(2)
            Sequence([Fraction(5, 4), Fraction(3, 2), Fraction(7, 4)])

        """
        comb = self.combinations(size, as_set=True)
        multiples = [Sequence(_).sum() for _ in comb]
        segment = RatioSet(multiples).constrain_to_octave().sorted()
        return RatioSet(segment).to_sequence()

    def combination_division(self, size=2):
        """

        .. container:: example

            >>> import quicktions
            >>> l = [2, 3, 4]
            >>> l = [quicktions.Fraction(_) for _ in l]
            >>> evans.Sequence(l).combination_division(2)
            Sequence([Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)])

        """
        comb = self.combinations(size, as_set=True)
        multiples = [Sequence(_).divide_all()[0] for _ in comb]
        segment = RatioSet(multiples).constrain_to_octave().sorted()
        return RatioSet(segment).to_sequence()

    def combination_multiplication(self, size=2):
        """

        .. container:: example

            >>> import quicktions
            >>> l = [2, 3, 4]
            >>> l = [quicktions.Fraction(_) for _ in l]
            >>> evans.Sequence(l).combination_multiplication(2)
            Sequence([Fraction(1, 1), Fraction(3, 2)])

        """
        comb = self.combinations(size, as_set=True)
        multiples = [Sequence(_).multiply_all()[0] for _ in comb]
        segment = RatioSet(multiples).constrain_to_octave().sorted()
        return RatioSet(segment).to_sequence()

    def combination_subtraction(self, size=2):
        """

        .. container:: example

            >>> import quicktions
            >>> l = [2, 3, 4]
            >>> l = [quicktions.Fraction(_) for _ in l]
            >>> evans.Sequence(l).combination_subtraction(2)
            Sequence([Fraction(10, 1), Fraction(11, 1)])

        """
        comb = self.combinations(size, as_set=True)
        multiples = [Sequence(_).subtract_all()[0] for _ in comb]
        segment = PitchClassSet(multiples).sorted()
        return PitchClassSet(segment).to_sequence()

    def combinations(self, size=2, as_set=False):
        """

        .. container:: example

            >>> l = [2, 2, 3, 3, 4, 4]
            >>> evans.Sequence(l).combinations(2)
            Sequence([(2, 2), (2, 3), (2, 3), (2, 4), (2, 4), (2, 3), (2, 3), (2, 4), (2, 4), (3, 3), (3, 4), (3, 4), (3, 4), (3, 4), (4, 4)])

        .. container:: example

            >>> l = [2, 2, 3, 3, 4, 4]
            >>> evans.Sequence(l).combinations(2, as_set=True)
            Sequence([(4, 4), (2, 4), (3, 4), (2, 3), (3, 3), (2, 2)])

        """
        out = [_ for _ in itertools.combinations(self.items, size)]
        if as_set:
            out = set(out)
        return Sequence(out)

    @staticmethod
    def chen(a, b, c, first_state, time_values, iters):
        """

        .. container:: example

            >>> c = evans.Sequence.chen(
            ...     a=40,
            ...     b=3,
            ...     c=28,
            ...     first_state=[-0.1, 0.5, -0.6],
            ...     time_values=[0.0, 40.0, 0.01],
            ...     iters=10,
            ... )
            ...
            >>> print(c)
            Sequence([[-0.1, 0.12465461315287765, 0.34050473218831634, 0.5770360314308272, 0.8626644815821614, 1.228312639285715, 1.7104499742301047, 2.3534686146396937, 3.210342581973768, 4.338499963066017], [0.5, 0.6622702530766478, 0.8942439508177749, 1.2176463222616842, 1.66295375321105, 2.2713555330407695, 3.0965468523002206, 4.204669803361282, 5.6680291136883945, 7.542293510840843], [-0.6, -0.5821525955103403, -0.5631370288024949, -0.5417183868578875, -0.5155298081524363, -0.48013350192305393, -0.4273027100127936, -0.34198524404844655, -0.19722719758314597, 0.05337630134609778]])

        """

        def vector_calc(state, t):
            x, y, z = state
            return (
                decimal.Decimal(a) * (decimal.Decimal(y) - decimal.Decimal(x)),
                (decimal.Decimal(c) - decimal.Decimal(a))
                * decimal.Decimal(x)
                * decimal.Decimal(z)
                + (decimal.Decimal(c) * decimal.Decimal(y)),
                (decimal.Decimal(x) * decimal.Decimal(y))
                - (decimal.Decimal(b) * decimal.Decimal(z)),
            )

        t = numpy.arange(time_values[0], time_values[1], time_values[2])
        states = odeint(vector_calc, first_state, t)
        return Sequence(
            [
                [_ for _ in states[:iters, 0]],
                [_ for _ in states[:iters, 1]],
                [_ for _ in states[:iters, 2]],
            ]
        )

    def derive_added_sequences(self, seq, flat=False):
        """

        .. container:: example

            >>> for _ in evans.Sequence([0, 1, 2, 3]).derive_added_sequences([4, 5, 6, 7, 8]):
            ...     _
            ...
            [4, 5, 6, 7]
            [5, 6, 7, 8]
            [6, 7, 8, 9]
            [7, 8, 9, 10]
            [8, 9, 10, 11]

        .. container:: example

            >>> for _ in evans.Sequence([0, 1, 2, 3, 4]).derive_added_sequences([5, 6, 7, 8]):
            ...     _
            ...
            [5, 6, 7, 8, 9]
            [6, 7, 8, 9, 10]
            [7, 8, 9, 10, 11]
            [8, 9, 10, 11, 12]

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3, 4]).derive_added_sequences([5, 6, 7, 8], flat=True)
            Sequence([5, 6, 7, 8, 9, 6, 7, 8, 9, 10, 7, 8, 9, 10, 11, 8, 9, 10, 11, 12])

        """
        x = [_ for _ in self.items]
        returned_sequence = []
        for val in seq:
            transposition = []
            for val_ in x:
                transposition.append(val + val_)
            returned_sequence.append(transposition)
        if flat is True:
            returned_sequence = flatten(returned_sequence)
        return Sequence(returned_sequence)

    def derive_multiplied_sequences(self, seq, flat=False):
        """

        .. container:: example

            >>> for _ in evans.Sequence([0, 1, 2, 3]).derive_multiplied_sequences([4, 5, 6, 7, 8]):
            ...     _
            ...
            [0, 4, 8, 12]
            [0, 5, 10, 15]
            [0, 6, 12, 18]
            [0, 7, 14, 21]
            [0, 8, 16, 24]

        .. container:: example

            >>> for _ in evans.Sequence([0, 1, 2, 3, 4]).derive_multiplied_sequences([5, 6, 7, 8]):
            ...     _
            ...
            [0, 5, 10, 15, 20]
            [0, 6, 12, 18, 24]
            [0, 7, 14, 21, 28]
            [0, 8, 16, 24, 32]

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3, 4]).derive_multiplied_sequences([5, 6, 7, 8], flat=True)
            Sequence([0, 5, 10, 15, 20, 0, 6, 12, 18, 24, 0, 7, 14, 21, 28, 0, 8, 16, 24, 32])

        """
        x = [_ for _ in self.items]
        returned_sequence = []
        for val in seq:
            transposition = []
            for val_ in x:
                transposition.append(val * val_)
            returned_sequence.append(transposition)
        if flat is True:
            returned_sequence = flatten(returned_sequence)
        return Sequence(returned_sequence)

    def divide_all(self):
        """

        .. container:: example

            >>> l = [1, 2, 3, 4]
            >>> evans.Sequence(l).divide_all()
            Sequence([0.041666666666666664])

        """
        x = self.items[0]
        for _ in self.items[1:]:
            x /= _
        return Sequence([x])

    @staticmethod
    def e_bonacci_cycle(n, iters, first, second, modulus, wrap_to_zero=False):
        """

        .. container:: example

            >>> evans.Sequence.e_bonacci_cycle(n=3, iters=15, first=1, second=1, modulus=7)
            Sequence([1, 1, 2, 4, 7, 6, 3, 2, 4, 2, 1, 7, 3])

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
        return Sequence(sequence)

    @staticmethod
    def e_dovan_cycle(n, iters, first, second, modulus, wrap_to_zero=False):
        """

        .. container:: example

            >>> evans.Sequence.e_dovan_cycle(n=3, iters=15, first=1, second=1, modulus=7)
            Sequence([1, 1, 1, 2, 3, 4, 6, 2, 6, 5, 7, 6, 4])

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
        return Sequence(sequence)

    @staticmethod
    def feigenbaum_bifurcations(fertility=3.59785, initial_state=0.5, iterations=10):
        """

        .. container:: example

            >>> evans.Sequence.feigenbaum_bifurcations(fertility= 2.3, initial_state=0.5, iterations=4)
            Sequence([0.5, 0.575, 0.5620625, 0.5661409660156249, 0.5649383570133959])

        """
        list_ = [initial_state]
        for _ in range(iterations):
            front = fertility * initial_state
            back = 1 - initial_state
            next_state = front * back
            list_.append(next_state)
            initial_state = next_state
        return Sequence(list_)

    def grouper(self, seq):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3, 4, 5, 6, 7]).grouper([1, 1, 2, 1, 3])
            [0, 1, [2, 3], 4, [5, 6, 7]]

        """

        def cyc(lst):
            c = 0
            while True:
                yield lst[c % len(lst)]
                c += 1

        lst1 = cyc([_ for _ in self.items])
        return [next(lst1) if i == 1 else [next(lst1) for _ in range(i)] for i in seq]

    def guerrero_morales(self, set_size=None):
        """

        .. container:: example

            >>> g_m = evans.Sequence(["A", "B", "C", "D", "E", "F", "G"]).guerrero_morales(3)
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

            >>> for _ in evans.Sequence(["A", "B", "C", "D", "E", "F", "G", "H", "I"]).guerrero_morales(5):
            ...     _
            ...
            ['A', 'B', 'C', 'D', 'E']
            ['B', 'F', 'G', 'H', 'I']

        .. container:: example

            >>> for _ in evans.Sequence(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]).guerrero_morales(4):
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

            >>> for _ in evans.Sequence(["A", "B", "C", "D", "E", "F", "G", "H", "I"]).guerrero_morales(3):
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
        terms = [_ for _ in self.items]
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
        return Sequence(returned_list)

    @staticmethod
    def henon(first_state, a, b, iters):
        """

        .. container:: example

            >>> h = evans.Sequence.henon(
            ...     first_state=[(-0.75), 0.32],
            ...     a=1.2,
            ...     b=0.3,
            ...     iters=10,
            ... )
            ...
            >>> h
            Sequence([[-0.75, Decimal('0.6450000000000000316413562021'), Decimal('0.2757699999999999778210746366'), Decimal('1.102241088520000020387803903'), Decimal('-0.375191500666105380643309098'), Decimal('1.161749931949499014986033708'), Decimal('-0.7321529354614302607193373836'), Decimal('0.7052674744991025979072557961'), Decimal('0.1834714666579601521199694779'), Decimal('1.171186107456583192487843126'), Decimal('-0.590970837961775774691947209')], [0.32, Decimal('-0.2249999999999999916733273153'), Decimal('0.1935000000000000023314683518'), Decimal('0.08273099999999999028466035597'), Decimal('0.3306723265559999938790068193'), Decimal('-0.1125574501998316100275303026'), Decimal('0.3485249795848496915977948793'), Decimal('-0.2196458806384290700872707501'), Decimal('0.2115802423497307715421348517'), Decimal('0.05504143999738804359904837692'), Decimal('0.3513558322369749447435751116')]])

        """
        x_coordinates = [first_state[0]]
        y_coordinates = [first_state[1]]
        for _ in range(iters):
            prev_x = x_coordinates[-1]
            prev_y = y_coordinates[-1]
            x_coordinates.append(
                (decimal.Decimal(prev_y) + 1)
                - (decimal.Decimal(a) * (decimal.Decimal(prev_x) ** 2))
            )
            y_coordinates.append(decimal.Decimal(b) * decimal.Decimal(prev_x))
        return Sequence([x_coordinates, y_coordinates])

    def hexagonal_sequence(self):
        """

        .. container:: example

            >>> seq = evans.Sequence([_ for _ in range(8)]).hexagonal_sequence()
            >>> seq
            Sequence([0, 1, 6, 15, 28, 45, 66, 91])

        """
        n_list = [_ for _ in self.items]
        seq = []
        for n in n_list:
            x = n * (2 * n - 1)
            seq.append(x)
        return Sequence(seq)

    def josephus(self, k):
        """

        .. container:: example

            >>> tone_row = [0, 1, 2, 3, 4]
            >>> for i in range(16):
            ...     evans.Sequence(tone_row).josephus(i + 2)
            ...
            Sequence([[0, 1, 2, 3, 4], [0, 2, 3, 4], [0, 2, 4], [2, 4], [2]])
            Sequence([[0, 1, 2, 3, 4], [0, 1, 3, 4], [1, 3, 4], [1, 3], [3]])
            Sequence([[0, 1, 2, 3, 4], [0, 1, 2, 4], [0, 1, 4], [0, 1], [0]])
            Sequence([[0, 1, 2, 3, 4], [0, 1, 2, 3], [1, 2, 3], [1, 3], [1]])
            Sequence([[0, 1, 2, 3, 4], [1, 2, 3, 4], [1, 3, 4], [3, 4], [3]])
            Sequence([[0, 1, 2, 3, 4], [0, 2, 3, 4], [0, 2, 3], [2, 3], [3]])
            Sequence([[0, 1, 2, 3, 4], [0, 1, 3, 4], [0, 3, 4], [0, 3], [0]])
            Sequence([[0, 1, 2, 3, 4], [0, 1, 2, 4], [0, 1, 2], [0, 1], [1]])
            Sequence([[0, 1, 2, 3, 4], [0, 1, 2, 3], [0, 2, 3], [0, 3], [3]])
            Sequence([[0, 1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 4], [2, 4], [4]])
            Sequence([[0, 1, 2, 3, 4], [0, 2, 3, 4], [2, 3, 4], [2, 3], [2]])
            Sequence([[0, 1, 2, 3, 4], [0, 1, 3, 4], [0, 1, 4], [0, 1], [1]])
            Sequence([[0, 1, 2, 3, 4], [0, 1, 2, 4], [1, 2, 4], [1, 4], [4]])
            Sequence([[0, 1, 2, 3, 4], [0, 1, 2, 3], [0, 1, 3], [0, 3], [0]])
            Sequence([[0, 1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3], [2, 3], [2]])
            Sequence([[0, 1, 2, 3, 4], [0, 2, 3, 4], [0, 3, 4], [0, 3], [3]])

        .. container:: example

            >>> tone_row = [0, 1, 2, 3, 4]
            >>> for i in range(16):
            ...     evans.Sequence(tone_row).josephus(i + 2).flatten()
            ...
            Sequence([0, 1, 2, 3, 4, 0, 2, 3, 4, 0, 2, 4, 2, 4, 2])
            Sequence([0, 1, 2, 3, 4, 0, 1, 3, 4, 1, 3, 4, 1, 3, 3])
            Sequence([0, 1, 2, 3, 4, 0, 1, 2, 4, 0, 1, 4, 0, 1, 0])
            Sequence([0, 1, 2, 3, 4, 0, 1, 2, 3, 1, 2, 3, 1, 3, 1])
            Sequence([0, 1, 2, 3, 4, 1, 2, 3, 4, 1, 3, 4, 3, 4, 3])
            Sequence([0, 1, 2, 3, 4, 0, 2, 3, 4, 0, 2, 3, 2, 3, 3])
            Sequence([0, 1, 2, 3, 4, 0, 1, 3, 4, 0, 3, 4, 0, 3, 0])
            Sequence([0, 1, 2, 3, 4, 0, 1, 2, 4, 0, 1, 2, 0, 1, 1])
            Sequence([0, 1, 2, 3, 4, 0, 1, 2, 3, 0, 2, 3, 0, 3, 3])
            Sequence([0, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 4, 2, 4, 4])
            Sequence([0, 1, 2, 3, 4, 0, 2, 3, 4, 2, 3, 4, 2, 3, 2])
            Sequence([0, 1, 2, 3, 4, 0, 1, 3, 4, 0, 1, 4, 0, 1, 1])
            Sequence([0, 1, 2, 3, 4, 0, 1, 2, 4, 1, 2, 4, 1, 4, 4])
            Sequence([0, 1, 2, 3, 4, 0, 1, 2, 3, 0, 1, 3, 0, 3, 0])
            Sequence([0, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 2, 3, 2])
            Sequence([0, 1, 2, 3, 4, 0, 2, 3, 4, 0, 3, 4, 0, 3, 3])

        """
        n = len(self.items)
        p, i, seq = list(range(n)), 0, []
        returned_sequences = [list(self.items)]
        while p:
            i = (i + k - 1) % len(p)
            seq.append(p.pop(i))
        sequences = [list(range(n))]
        for _ in seq:
            next = [x for x in sequences[-1]]
            next.remove(_)
            sequences.append(next)
            returned_sequences.append(list(self.retain(next).items))
        return Sequence(returned_sequences[:-1])

    @staticmethod
    def lindenmayer(seed, rules, iters):
        """

        .. container:: example

            >>> rule_dict = { "A": "ABA" , "B": "BC", "C": "BAC"}
            >>> lind_list = evans.Sequence.lindenmayer(seed='AB', rules=rule_dict, iters=2)
            >>> lind_list
            Sequence(['A', 'B', 'A', 'B', 'C', 'A', 'B', 'A', 'B', 'C', 'B', 'A', 'C'])

        """
        for _ in range(iters):
            result = ""
            for axiom in seed:
                if axiom in rules:
                    result += rules[axiom]
                else:
                    result += axiom
            seed = result
        return Sequence(seed)

    @staticmethod
    def lorenz(rho, sigma, beta, first_state, time_values, iters):
        """

        .. container:: example

            >>> evans.Sequence.lorenz(
            ...     rho=28.0,
            ...     sigma=10.0,
            ...     beta=(8.0 / 3.0),
            ...     first_state=[1.0, 1.0, 1.0],
            ...     time_values=[0.0, 40.0, 0.01],
            ...     iters=10,
            ... )
            ...
            Sequence([[1.0, 1.0125657408032651, 1.0488214579592021, 1.107206299034454, 1.1868654842333801, 1.2875548011090359, 1.4095688012763303, 1.5536887870511105, 1.721145788631946, 1.9135963877769706], [1.0, 1.2599200056984277, 1.5240008388892068, 1.798314577764884, 2.0885455352781572, 2.400160398825767, 2.738552104480127, 3.109160997057688, 3.51757713188136, 3.969623487737072], [1.0, 0.9848910446848755, 0.973114341630953, 0.9651591023109144, 0.9617373815250438, 0.9638062240116604, 0.9726082787069016, 0.9897311952182216, 1.0171865646618774, 1.057511871629279]])

        """

        def vector_calc(state, t):
            x, y, z = state
            return (
                decimal.Decimal(sigma) * (decimal.Decimal(y) - decimal.Decimal(x)),
                decimal.Decimal(x) * (decimal.Decimal(rho) - decimal.Decimal(z))
                - decimal.Decimal(y),
                decimal.Decimal(x) * decimal.Decimal(y)
                - decimal.Decimal(beta) * decimal.Decimal(z),
            )

        t = numpy.arange(time_values[0], time_values[1], time_values[2])
        states = odeint(vector_calc, first_state, t)
        return Sequence(
            [
                [_ for _ in states[:iters, 0]],
                [_ for _ in states[:iters, 1]],
                [_ for _ in states[:iters, 2]],
            ]
        )

    @staticmethod
    def lu_chen(a, b, c, u, first_state, time_values, iters):
        """

        .. container:: example

            >>> evans.Sequence.lu_chen(
            ...     a=36,
            ...     b=3,
            ...     c=20,
            ...     u=(-15.15),
            ...     first_state=[0.1, 0.3, -0.6],
            ...     time_values=[0.0, 40.0, 0.01],
            ...     iters=10,
            ... )
            ...
            Sequence([[0.1, 0.14507340240351432, 0.14323815901530343, 0.10128972203257065, 0.02212510661501916, -0.09446533541055804, -0.25134777506809247, -0.4538520580544356, -0.7097811725420128, -1.0295889433224696], [0.3, 0.20092880055892573, 0.08027594159872467, -0.06748948170440211, -0.2490165225972874, -0.4723839158805826, -0.7474651998093496, -1.0863625805752994, -1.503923707544488, -2.0183521101080717], [-0.6, -0.5819559886254813, -0.5645492876975078, -0.547848676066436, -0.5317444633853425, -0.5158905397379729, -0.4995950638053594, -0.48163813037580305, -0.4599814138948388, -0.43131546553144084]])

        """

        def vector_calc(state, t):
            x, y, z = state
            return (
                decimal.Decimal(a) * (decimal.Decimal(y) - decimal.Decimal(x)),
                decimal.Decimal(x)
                - (decimal.Decimal(x) * decimal.Decimal(z))
                + (decimal.Decimal(c) * decimal.Decimal(y))
                + decimal.Decimal(u),
                (decimal.Decimal(x) * decimal.Decimal(y))
                - (decimal.Decimal(b) * decimal.Decimal(z)),
            )

        t = numpy.arange(time_values[0], time_values[1], time_values[2])
        states = odeint(vector_calc, first_state, t)
        return Sequence(
            [
                [_ for _ in states[:iters, 0]],
                [_ for _ in states[:iters, 1]],
                [_ for _ in states[:iters, 2]],
            ]
        )

    @staticmethod
    def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, maxiter):
        """

        .. container:: example

            >>> evans.Sequence.mandelbrot_set(
            ... xmin=7,
            ... xmax=10,
            ... ymin=7,
            ... ymax=10,
            ... width=10,
            ... height=10,
            ... maxiter=10,
            ... )
            ...
            Sequence([array([ 7.        ,  7.33333333,  7.66666667,  8.        ,  8.33333333,
                    8.66666667,  9.        ,  9.33333333,  9.66666667, 10.        ]), array([ 7.        ,  7.33333333,  7.66666667,  8.        ,  8.33333333,
                    8.66666667,  9.        ,  9.33333333,  9.66666667, 10.        ]), array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                   [0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])])

        """

        def mandelbrot(c, maxiter):
            z = c
            for n in range(maxiter):
                if abs(z) > 2:
                    return n
                z = z * z + c
            return 0

        r1 = numpy.linspace(xmin, xmax, width)
        r2 = numpy.linspace(ymin, ymax, height)
        n3 = numpy.empty((width, height))
        for i in range(width):
            for j in range(height):
                n3[i, j] = mandelbrot(r1[i] + 1j * r2[j], maxiter)
        return Sequence([r1, r2, n3])

    def map_dict(self, mapping_dict):
        """

        .. container:: example

            >>> mapping_dict = {
            ...     "A": 0,
            ...     "B": 1,
            ...     "C": 2,
            ...     "D": 3,
            ... }
            ...
            >>> evans.Sequence(["A", "C", "B", "D"]).map_dict(mapping_dict)
            Sequence([0, 2, 1, 3])

        """
        returned_seq = Sequence([mapping_dict[_] for _ in self.items])
        return returned_seq

    def map_indices(self, index_list):
        """

        .. container:: example

            >>> evans.Sequence([2, 3, 4, 5]).map_indices([0, 0, 1, 0, 2, 3, 2])
            Sequence([2, 2, 3, 2, 4, 5, 4])

        """
        items_list = list(self.items)
        returned_list = []
        for index in index_list:
            val = items_list[index]
            returned_list.append(val)
        return Sequence(returned_list)

    def mirror(self, sequential_duplicates):
        """

        .. container:: example

            >>> print(
            ...     evans.Sequence([0, 1, 2, 3]).mirror(
            ...         sequential_duplicates=True,
            ...     )
            ... )
            Sequence([0, 1, 2, 3, 3, 2, 1, 0])

        .. container:: example

            >>> print(
            ...     evans.Sequence([0, 1, 2, 3]).mirror(
            ...         sequential_duplicates=False,
            ...     )
            ... )
            Sequence([0, 1, 2, 3, 2, 1])

        """
        lst = list(self.items)
        if sequential_duplicates is False:
            return Sequence(lst + lst[-2:0:-1])
        else:
            return Sequence(lst + lst[::-1])

    def mod(self, modulus, indices=False):
        """

        .. container:: example

            >>> evans.Sequence([7, 8, 9, 10]).mod(7)
            Sequence([7, 1, 2, 3])

        .. container:: example

            >>> evans.Sequence([7, 8, 9, 10]).mod(7, indices=True)
            Sequence([0, 1, 2, 3])

        """
        new_seq = [(_ % modulus) for _ in self.items]
        for i, _ in enumerate(new_seq):
            if indices is False:
                if _ == 0:
                    new_seq[i] = _ + modulus
                else:
                    continue
            else:
                continue
        return Sequence(new_seq)

    def multiply(self, x):
        """

        .. container:: example

            >>> evans.Sequence([7, 8, 9, 10]).multiply(7)
            Sequence([49, 56, 63, 70])

        .. container:: example

            >>> evans.Sequence([7, 8, 9, 10]).multiply((12 / 10))
            Sequence([8.4, 9.6, 10.799999999999999, 12.0])

        """
        l_ = list(self.items)
        returned_seq = []
        for _ in l_:
            returned_seq.append(_ * x)
        return Sequence(returned_seq)

    def multiply_all(self):
        """

        .. container:: example

            >>> evans.Sequence([7, 8, 9, 10]).multiply_all()
            Sequence([5040])

        """
        x = 1
        for _ in self.items:
            x *= _
        return Sequence([x])

    def multiply_sequences(self, seq):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3]).multiply_sequences([4, 5, 6, 7, 8])
            Sequence([0, 5, 12, 21])

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3, 4]).multiply_sequences([5, 6, 7, 8])
            Sequence([0, 6, 14, 24, 20])

        """
        x = list(self.items)
        returned_sequence = []
        cyc_y = CyclicList(seq, forget=False)
        for _ in x:
            y_val = cyc_y(r=1)[0]
            returned_sequence.append(_ * y_val)
        return Sequence(returned_sequence)

    @staticmethod
    def n_bonacci_cycle(
        n, first_number, second_number, length, modulus, wrap_to_zero=False
    ):
        """

        .. container:: example

            >>> evans.Sequence.n_bonacci_cycle(n=3, first_number=1, second_number=3, length=8, modulus=7)
            Sequence([1, 3, 3, 5, 4, 3, 6, 7, 6, 4])

        """
        sequence = [first_number, second_number]
        for _ in range(length):
            sequence.append(sequence[-2] + (sequence[-1] * n))
        sequence = [(_ % modulus) for _ in sequence]
        if wrap_to_zero is False:
            for index, item in enumerate(sequence):
                if item == 0:
                    sequence[index] = item + modulus
        return Sequence(sequence)

    def normalize_to_sum(self, desired_sum=1):
        """

        .. container:: example

            >>> weights = [15, 6, 14, 4, 16, 6, 14, 4, 16, 5]
            >>> evans.Sequence(weights).normalize_to_sum(1)
            Sequence([0.15, 0.06, 0.14, 0.04, 0.16, 0.06, 0.14, 0.04, 0.16, 0.05])

        """
        integer_list = list(self.items)
        sum = 0
        for _ in integer_list:
            sum = sum + _ / desired_sum
        normalized_list = []
        for _ in integer_list:
            normalized_list.append(_ / sum)
        return Sequence(normalized_list)

    def normalize_to_indices(self):
        """

        .. container:: example

            >>> evans.Sequence([1, 0.24, -12, [-4, 0.7], -0.5]).normalize_to_indices()
            Sequence([4, 1, -50, Sequence([-5, 1]), -2])

        """
        raw_list = list(self.items)
        out = []
        flat_raw = [abs(float(_)) for _ in flatten(raw_list)]
        minimum_value = min(flat_raw)
        if minimum_value == 0:
            minimum_value = 0.000001
        for _ in raw_list:
            if isinstance(_, list):
                out.append(Sequence(_).normalize_to_indices())
            else:
                out.append(int(float(_) / minimum_value))
        return Sequence(out)

    @staticmethod
    def orbits(initial_state=0.4, iterations=10):
        """

        .. container:: example

            >>> evans.Sequence.orbits(initial_state=0.4, iterations=5)
            Sequence([0.96, 0.15360000000000013, 0.5200281600000003, 0.9983954912280576, 0.006407737294172653])

        """
        list_ = []
        for _ in range(iterations):
            front = 4 * initial_state
            back = 1 - initial_state
            next_state = front * back
            list_.append(next_state)
            initial_state = next_state
        return Sequence(list_)

    def permutations(self):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2]).permutations()
            Sequence([[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]])

        .. container:: example

            >>> evans.Sequence([0, [1, 2], 3]).permutations()
            Sequence([[0, [1, 2], 3], [0, 3, [1, 2]], [[1, 2], 0, 3], [[1, 2], 3, 0], [3, 0, [1, 2]], [3, [1, 2], 0]])

        .. todo:: Add recursive permutations?

        """
        lst = list(self.items)
        if len(lst) == 0:
            return []
        if len(lst) == 1:
            return [lst]
        else:
            list_ = []
            for i in range(len(lst)):
                x = lst[i]
                ba = lst[:i] + lst[i + 1 :]
                for p in Sequence(ba).permutations():
                    list_.append([x] + p)
            return Sequence(list_)

    def pitch_warp(self, warp_values=(0.5, -0.5), *, boolean_vector=(1)):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3, 4]).pitch_warp([0.5, -0.5], boolean_vector=[0, 1, 1])
            Sequence([0, 1.5, 1.5, 3, 4.5])

        """
        pitch_list = list(self.items)
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
        return Sequence(pitch_list)

    @staticmethod
    def prime_sequence(start, end):
        """

        .. container:: example

            >>> evans.Sequence.prime_sequence(start=11, end=25)
            Sequence([11, 13, 15, 17, 19, 21, 23, 25])

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
        return Sequence(seq)

    def prism_sequence(self):
        """

        .. container:: example

            >>> evans.Sequence([_ for _ in range(8)]).prism_sequence()
            Sequence([1, 14, 57, 148, 305, 546, 889, 1352])

        """
        n_list = list(self.items)
        seq = []
        for n in n_list:
            x = (n + 1) * (3 * n ** 2 + 3 * n + 1)
            seq.append(x)
        return Sequence(seq)

    def random_walk(self, length, step_list, random_seed=1):
        """

        .. container:: example

            >>> evans.Sequence([_ for _ in range(10)]).random_walk(
            ...     length=5,
            ...     step_list=[1, 2, 1],
            ...     random_seed=1,
            ... )
            Sequence([0, 9, 0, 2, 1, 0])

        """

        def reduce_mod(x, rw):
            return [(y % x) for y in rw]

        mapped_list = list(self.items)
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
        return Sequence(final_list)

    def recaman_sequence(self):
        """

        .. container:: example

            >>> evans.Sequence([_ + 1 for _ in range(10)]).recaman_sequence()
            Sequence([1, 3, 6, 2, 7, 1, 8, 16, 7, 17])

        """
        seq = list(self.items)
        returned_list = []

        def calc_number(number):
            temp_list = []
            if number == 1:
                temp_list.append(number)
                return number
            else:
                a = calc_number(number - 1)
                am = a - number
                ap = a + number
                if am > 0 and am not in temp_list:
                    temp_list.append(am)
                    return am
                else:
                    temp_list.append(ap)
                    return ap

        for _ in seq:
            val = calc_number(_)
            returned_list.append(val)
        return Sequence(returned_list)

    def reciprocals(self):
        """

        .. container:: example

            >>> evans.Sequence([0.5]).reciprocals()
            Sequence([2.0])

        """
        lst = list(self.items)
        returned_list = []
        for _ in lst:
            val = 1 / _
            returned_list.append(val)
        return Sequence(returned_list)

    def reproportion_by_base(self, base, round=None):
        """

        .. container:: example

            >>> rounder = evans.to_nearest_eighth_tone
            >>> print(
            ...     evans.Sequence(
            ...         [-24, -20, -15, -14, -4, 5, 11, 19, 26, 37, 39, 42]
            ...         ).reproportion_by_base(
            ...         base=2,
            ...         round=rounder,
            ...     )
            ... )
            Sequence([-4.75, -4, -3, -2.75, -0.75, 1, 2.25, 3.75, 5.25, 7.5, 7.75, 8.5])

        """
        chord = list(self.items)
        base_converter = base / 10.0
        collection = []
        for _ in chord:
            collection.append(_ * base_converter)
        if round is not None:
            collection = [round(_) for _ in collection]
        return Sequence(collection)

    def rotate(self, n):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3]).rotate(2)
            Sequence([2, 3, 0, 1])

        """
        lst = list(self.items)
        return Sequence(lst[n:] + lst[:n])

    @staticmethod
    def roessler(a, b, c, t_ini, t_fin, h):
        """

        .. container:: example

            >>> import numpy
            >>> evans.Sequence.roessler(
            ...     a=0.13,
            ...     b=0.2,
            ...     c=6.5,
            ...     t_ini=0,
            ...     t_fin=(3 * (numpy.pi)),
            ...     h=0.0001,
            ... )
            ...
            Sequence([array([ 0.00000000e+00,  0.00000000e+00, -2.00007553e-09, ...,
                    1.86024565e-03,  1.86567571e-03,  1.87110585e-03]), array([ 0.        ,  0.        ,  0.        , ..., -0.08504001,
                   -0.08504093, -0.08504185]), array([0.00000000e+00, 2.00003777e-05, 3.99877548e-05, ...,
                   3.07404473e-02, 3.07404717e-02, 3.07404962e-02])])

        """

        def calc_coordinates(x_n, y_n, z_n, h, a_, b_, c_):
            x_n1 = x_n + h * (-y_n - z_n)
            y_n1 = y_n + h * (x_n + a_ * y_n)
            z_n1 = z_n + h * (b_ + z_n * (x_n - c_))
            return x_n1, y_n1, z_n1

        numsteps = int((t_fin - t_ini) / h)
        t = scipy.linspace(t_ini, t_fin, numsteps)
        x = numpy.zeros(numsteps)
        y = numpy.zeros(numsteps)
        z = numpy.zeros(numsteps)
        x[0] = 0
        y[0] = 0
        z[0] = 0
        for _ in range(x.size - 1):
            [x[_ + 1], y[_ + 1], z[_ + 1]] = calc_coordinates(
                x[_], y[_], z[_], t[_ + 1] - t[_], a, b, c
            )
        return Sequence([x, y, z])

    def stack_intervals(self):
        """

        .. container:: example

            >>> s = evans.Sequence([1, -2, 3])
            >>> s.stack_intervals()
            Sequence([1, -1, 2])

        """
        returned_list = [self.items[0]]
        for _ in self.items[1:]:
            returned_list.append(_ + returned_list[-1])
        seq = Sequence(returned_list)
        return seq

    def stack_pitches(self):
        """

        .. container:: example

            >>> s = evans.Sequence([1, -2, 3])
            >>> s.stack_pitches()
            Sequence([1, 10, 15])

        """
        returned_list = [self.items[0]]
        for _ in self.items[1:]:
            while _ < returned_list[-1]:
                _ += 12
            returned_list.append(_)
        seq = Sequence(returned_list)
        return seq

    def subtract_all(self):
        """

        .. container:: example

            >>> l = [1, 2, 3, 4]
            >>> evans.Sequence(l).subtract_all()
            Sequence([-8])

        """
        x = self.items[0]
        for _ in self.items[1:]:
            x -= _
        return Sequence([x])

    def transpose(self, n):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3]).transpose(10)
            Sequence([10, 11, 12, 13])

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3]).transpose(10).mod(12, indices=True)
            Sequence([10, 11, 0, 1])

        """
        values = list(self.items)
        returned_list = []
        for _ in values:
            val = _ + n
            returned_list.append(val)
        return Sequence(returned_list)

    def warp(self, min, max, random_seed, by_integers=False):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).warp(-0.5, 0.5, 3)
            Sequence([-0.26203537290810863, 1.0442292252959517, 1.8699551665480794, 3.1039200385961943, 4.125720304108054, 4.565528859239813, 5.513167991554874, 7.33746908209646, 7.759354014328007, 8.734330961046696])

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).warp(-1, 1, 3, by_integers=True)
            Sequence([-1, 2, 3, 2, 4, 6, 6, 8, 9, 8])

        """
        warped_list = list(self.items)
        random.seed(random_seed)
        final_list = []
        if by_integers is True:
            perturbation_list = [random.randint(min, max) for _ in warped_list]
        else:
            perturbation_list = [random.uniform(min, max) for _ in warped_list]
        for x, y in zip(warped_list, perturbation_list):
            final_list.append(x + y)
        return Sequence(final_list)


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


def julia_set(c, z0, max_iter):
    """

    .. container:: example

        >>> s = evans.julia_set(
        ...     c=0.25,
        ...     z0=1.5,
        ...     max_iter=10,
        ... )
        ...
        >>> print(s)
        1.7209086512090908

    """
    z = z0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1

    if n == max_iter:
        return max_iter

    return n + 1 - math.log(math.log2(abs(z)))
