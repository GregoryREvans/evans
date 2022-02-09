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

        >>> prob = {
        ...     'one': {'one': 0.8, 'two': 0.19, 'three': 0.01},
        ...     'two': {'one': 0.2, 'two': 0.7, 'three': 0.1},
        ...     'three': {'one': 0.1, 'two': 0.2, 'three': 0.7}
        ... }
        >>> chain = evans.MarkovChain(transition_prob=prob, seed=7)
        >>> key_list = [
        ...     x for x in chain.generate_states(
        ...         current_state='one', no=14
        ...         )
        ...     ]
        >>> key_list
        ['one', 'one', 'one', 'one', 'two', 'two', 'two', 'one', 'one', 'one', 'one', 'two', 'two', 'one']

    """

    def __init__(self, transition_prob, seed):
        self.transition_prob = transition_prob
        self.states = list(transition_prob.keys())
        numpy.random.seed(seed)

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
    def alpha(self, category):
        """

        .. container:: example

            >>> s = evans.PitchClassSet([_ for _ in range(12)])
            >>> s.alpha(category=1)
            PitchClassSet([Fraction(1, 1), Fraction(0, 1), Fraction(3, 1), Fraction(2, 1), Fraction(5, 1), Fraction(4, 1), Fraction(7, 1), Fraction(6, 1), Fraction(9, 1), Fraction(8, 1), Fraction(11, 1), Fraction(10, 1)])

        .. container:: example

            >>> s = evans.PitchClassSet([_ for _ in range(12)])
            >>> s.alpha(category=2)
            PitchClassSet([Fraction(11, 1), Fraction(2, 1), Fraction(1, 1), Fraction(4, 1), Fraction(3, 1), Fraction(6, 1), Fraction(5, 1), Fraction(8, 1), Fraction(7, 1), Fraction(10, 1), Fraction(9, 1), Fraction(0, 1)])

        """
        numbers = []
        if category == 1:
            for _ in self:
                _ = abs(float(_))
                is_integer = True
                if not abjad.math.is_integer_equivalent_number(_):
                    is_integer = False
                    fraction_part = _ - int(_)
                    _ = int(_)
                if abs(_) % 2 == 0:
                    number = abs(_) + 1
                else:
                    number = abs(_) - 1
                if not is_integer:
                    number += fraction_part
                else:
                    number = int(number)
                numbers.append(number)
        elif category == 2:
            for _ in self:
                _ = abs(float(_))
                is_integer = True
                if not abjad.math.is_integer_equivalent_number(_):
                    is_integer = False
                    fraction_part = _ - int(_)
                    _ = int(_)
                if abs(_) % 2 == 0:
                    number = abs(_) - 1
                else:
                    number = abs(_) + 1
                if not is_integer:
                    number += fraction_part
                else:
                    number = int(number)
                numbers.append(number)
        else:
            numbers = [_ for _ in self]
        return type(self)(numbers)

    def to_sequence(self):
        seq = Sequence([_ for _ in self.pitch_classes])
        return seq


class PitchSet(microtones.PitchSet):
    def alpha(self, category):
        """

        .. container:: example

            >>> s = evans.PitchSet([_ for _ in range(12)])
            >>> s.alpha(category=1)
            PitchSet([Fraction(1, 1), Fraction(0, 1), Fraction(3, 1), Fraction(2, 1), Fraction(5, 1), Fraction(4, 1), Fraction(7, 1), Fraction(6, 1), Fraction(9, 1), Fraction(8, 1), Fraction(11, 1), Fraction(10, 1)])

        .. container:: example

            >>> s = evans.PitchSet([_ for _ in range(12)])
            >>> s.alpha(category=2)
            PitchSet([Fraction(-1, 1), Fraction(2, 1), Fraction(1, 1), Fraction(4, 1), Fraction(3, 1), Fraction(6, 1), Fraction(5, 1), Fraction(8, 1), Fraction(7, 1), Fraction(10, 1), Fraction(9, 1), Fraction(12, 1)])

        """
        numbers = []
        if category == 1:
            for _ in self:
                _ = abs(float(_))
                is_integer = True
                if not abjad.math.is_integer_equivalent_number(_):
                    is_integer = False
                    fraction_part = _ - int(_)
                    _ = int(_)
                if abs(_) % 2 == 0:
                    number = abs(_) + 1
                else:
                    number = abs(_) - 1
                if not is_integer:
                    number += fraction_part
                else:
                    number = int(number)
                numbers.append(number)
        elif category == 2:
            for _ in self:
                _ = abs(float(_))
                is_integer = True
                if not abjad.math.is_integer_equivalent_number(_):
                    is_integer = False
                    fraction_part = _ - int(_)
                    _ = int(_)
                if abs(_) % 2 == 0:
                    number = abs(_) - 1
                else:
                    number = abs(_) + 1
                if not is_integer:
                    number += fraction_part
                else:
                    number = int(number)
                numbers.append(number)
        else:
            numbers = [_ for _ in self]
        return type(self)(numbers)

    def to_sequence(self):
        seq = Sequence([_ for _ in self.pitches])
        return seq


class PitchClassSegment(microtones.PitchClassSegment):
    def alpha(self, category):
        """

        .. container:: example

            >>> s = evans.PitchClassSegment([_ for _ in range(12)])
            >>> s.alpha(category=1)
            PitchClassSegment([Fraction(1, 1), Fraction(0, 1), Fraction(3, 1), Fraction(2, 1), Fraction(5, 1), Fraction(4, 1), Fraction(7, 1), Fraction(6, 1), Fraction(9, 1), Fraction(8, 1), Fraction(11, 1), Fraction(10, 1)])

        .. container:: example

            >>> s = evans.PitchClassSegment([_ for _ in range(12)])
            >>> s.alpha(category=2)
            PitchClassSegment([Fraction(11, 1), Fraction(2, 1), Fraction(1, 1), Fraction(4, 1), Fraction(3, 1), Fraction(6, 1), Fraction(5, 1), Fraction(8, 1), Fraction(7, 1), Fraction(10, 1), Fraction(9, 1), Fraction(0, 1)])

        """
        numbers = []
        if category == 1:
            for _ in self:
                _ = abs(float(_))
                is_integer = True
                if not abjad.math.is_integer_equivalent_number(_):
                    is_integer = False
                    fraction_part = _ - int(_)
                    _ = int(_)
                if abs(_) % 2 == 0:
                    number = abs(_) + 1
                else:
                    number = abs(_) - 1
                if not is_integer:
                    number += fraction_part
                else:
                    number = int(number)
                numbers.append(number)
        elif category == 2:
            for _ in self:
                _ = abs(float(_))
                is_integer = True
                if not abjad.math.is_integer_equivalent_number(_):
                    is_integer = False
                    fraction_part = _ - int(_)
                    _ = int(_)
                if abs(_) % 2 == 0:
                    number = abs(_) - 1
                else:
                    number = abs(_) + 1
                if not is_integer:
                    number += fraction_part
                else:
                    number = int(number)
                numbers.append(number)
        else:
            numbers = [_ for _ in self]
        return type(self)(numbers)

    def to_sequence(self):
        seq = Sequence([_ for _ in self.pitch_classes])
        return seq


class PitchSegment(microtones.PitchSegment):
    def alpha(self, category):
        """

        .. container:: example

            >>> s = evans.PitchSegment([_ for _ in range(12)])
            >>> s.alpha(category=1)
            PitchSegment([Fraction(1, 1), Fraction(0, 1), Fraction(3, 1), Fraction(2, 1), Fraction(5, 1), Fraction(4, 1), Fraction(7, 1), Fraction(6, 1), Fraction(9, 1), Fraction(8, 1), Fraction(11, 1), Fraction(10, 1)])

        .. container:: example

            >>> s = evans.PitchSegment([_ for _ in range(12)])
            >>> s.alpha(category=2)
            PitchSegment([Fraction(-1, 1), Fraction(2, 1), Fraction(1, 1), Fraction(4, 1), Fraction(3, 1), Fraction(6, 1), Fraction(5, 1), Fraction(8, 1), Fraction(7, 1), Fraction(10, 1), Fraction(9, 1), Fraction(12, 1)])

        """
        numbers = []
        if category == 1:
            for _ in self:
                _ = abs(float(_))
                is_integer = True
                if not abjad.math.is_integer_equivalent_number(_):
                    is_integer = False
                    fraction_part = _ - int(_)
                    _ = int(_)
                if abs(_) % 2 == 0:
                    number = abs(_) + 1
                else:
                    number = abs(_) - 1
                if not is_integer:
                    number += fraction_part
                else:
                    number = int(number)
                numbers.append(number)
        elif category == 2:
            for _ in self:
                _ = abs(float(_))
                is_integer = True
                if not abjad.math.is_integer_equivalent_number(_):
                    is_integer = False
                    fraction_part = _ - int(_)
                    _ = int(_)
                if abs(_) % 2 == 0:
                    number = abs(_) - 1
                else:
                    number = abs(_) + 1
                if not is_integer:
                    number += fraction_part
                else:
                    number = int(number)
                numbers.append(number)
        else:
            numbers = [_ for _ in self]
        return type(self)(numbers)

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
        return type(self)(returned_sequence)

    def alpha(self, category):
        """

        .. container:: example

            >>> s = evans.Sequence([_ for _ in range(12)])
            >>> s.alpha(category=1)
            Sequence([1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10])

        .. container:: example

            >>> s = evans.Sequence([_ for _ in range(12)])
            >>> s.alpha(category=2)
            Sequence([-1, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12])

        """
        numbers = []
        if category == 1:
            for _ in self:
                _ = abs(float(_))
                is_integer = True
                if not abjad.math.is_integer_equivalent_number(_):
                    is_integer = False
                    fraction_part = _ - int(_)
                    _ = int(_)
                if abs(_) % 2 == 0:
                    number = abs(_) + 1
                else:
                    number = abs(_) - 1
                if not is_integer:
                    number += fraction_part
                else:
                    number = int(number)
                numbers.append(number)
        elif category == 2:
            for _ in self:
                _ = abs(float(_))
                is_integer = True
                if not abjad.math.is_integer_equivalent_number(_):
                    is_integer = False
                    fraction_part = _ - int(_)
                    _ = int(_)
                if abs(_) % 2 == 0:
                    number = abs(_) - 1
                else:
                    number = abs(_) + 1
                if not is_integer:
                    number += fraction_part
                else:
                    number = int(number)
                numbers.append(number)
        else:
            numbers = [_ for _ in self]
        return type(self)(numbers)

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
        multiples = [Sequence(_).dividend()[0] for _ in comb]
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
        multiples = [Sequence(_).product()[0] for _ in comb]
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
        multiples = [Sequence(_).difference()[0] for _ in comb]
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
        return type(self)(out)

    @classmethod
    def chen(class_, a, b, c, first_state, time_values, iters):
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
            Sequence([[-0.1, 0.125, 0.341, 0.577, 0.863, 1.228, 1.71, 2.353, 3.21, 4.338], [0.5, 0.662, 0.894, 1.218, 1.663, 2.271, 3.097, 4.205, 5.668, 7.542], [-0.6, -0.582, -0.563, -0.542, -0.516, -0.48, -0.427, -0.342, -0.197, 0.053]])

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
        return class_(
            [
                [round(_, 3) for _ in states[:iters, 0]],
                [round(_, 3) for _ in states[:iters, 1]],
                [round(_, 3) for _ in states[:iters, 2]],
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
        return type(self)(returned_sequence)

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
        return type(self)(returned_sequence)

    def dividend(self):
        """

        .. container:: example

            >>> l = [1, 2, 3, 4]
            >>> evans.Sequence(l).dividend()
            Sequence([0.041666666666666664])

        """
        x = self.items[0]
        for _ in self.items[1:]:
            x /= _
        return type(self)([x])

    @classmethod
    def e_bonacci_cycle(class_, n, iters, first, second, modulus, wrap_to_zero=False):
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
        return class_(sequence)

    @classmethod
    def e_dovan_cycle(class_, n, iters, first, second, modulus, wrap_to_zero=False):
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
        return class_(sequence)

    @classmethod
    def equal_divisions(
        class_, fundamental_frequency, interval_of_repetition, number_of_divisions
    ):
        """

        .. container:: example

            >>> evans.Sequence.equal_divisions(fundamental_frequency=440, interval_of_repetition=5/2, number_of_divisions=13)
            Sequence([440, 472.13201032057583, 506.6105344757916, 543.6069320264475, 583.3050764587438, 625.9022690424179, 671.6102194254697, 720.6560978390684, 773.2836641421384, 829.7544793170199, 890.3492054373801, 955.3690005692673, 1025.1370155380173, 1099.9999999999986])

        .. container:: example

            >>> evans.Sequence.equal_divisions(fundamental_frequency=440, interval_of_repetition=3, number_of_divisions=30)
            Sequence([440, 456.41164681329826, 473.4354348791521, 491.0941965749178, 509.4116159072997, 528.412260277441, 548.1216134308273, 568.5661096361954, 589.7731691392869, 611.7712349389996, 634.589810935259, 658.2595014997754, 682.8120525227575, 708.2803939906365, 734.6986841519048, 762.102355330305, 790.5281614468134, 820.0142273141569, 850.6000997699742, 882.3268007172038, 915.2368821428361, 949.3744831888192, 984.7853893516657, 1021.5170938901565, 1059.6188615235021, 1099.1417945053952, 1140.138901162571, 1182.665166989803, 1226.777628396683, 1272.5354492050965, 1319.9999999999964])

        """
        step = interval_of_repetition ** quicktions.Fraction(1, number_of_divisions)
        out = [fundamental_frequency]
        for i in range(number_of_divisions):
            degree = i + 1
            step_size = step ** degree
            freq = fundamental_frequency * step_size
            out.append(freq)
        return class_(out)

    @classmethod
    def feigenbaum_bifurcations(
        class_, fertility=3.59785, initial_state=0.5, iterations=10
    ):
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
        return class_(list_)

    def grouper(self, seq):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3, 4, 5, 6, 7]).grouper([1, 1, 2, 1, 3])
            Sequence([0, 1, [2, 3], 4, [5, 6, 7]])

        """

        def cyc(lst):
            c = 0
            while True:
                yield lst[c % len(lst)]
                c += 1

        lst1 = cyc([_ for _ in self.items])
        return type(self)(
            [next(lst1) if i == 1 else [next(lst1) for _ in range(i)] for i in seq]
        )

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
        return type(self)(returned_list)

    @classmethod
    def henon(class_, first_state, a, b, iters):
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
        return class_([x_coordinates, y_coordinates])

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
        return type(self)(seq)

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
        return type(self)(returned_sequences[:-1])

    def linear_asymmetric_inversion(self):
        """

        .. container:: example

            >>> evans.Sequence([0, 3, 4, 7, 9]).linear_asymmetric_inversion()
            [-3, 2, 1, 5]

        """
        out = []
        for i in range(len(self) - 1):
            pitch1 = self[i]
            pitch2 = self[i + 1]
            interval = abjad.NamedInterval.from_pitch_carriers(pitch1, pitch2)
            inverted_interval = abjad.NamedInterval("P1") - interval
            new_pitch = inverted_interval.transpose(abjad.NumberedPitch(pitch1))
            out.append(new_pitch.number)
        return out

    @classmethod
    def lindenmayer(class_, seed, rules, iters):
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
        return class_(seed)

    @classmethod
    def lorenz(class_, rho, sigma, beta, first_state, time_values, iters):
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
            Sequence([[1.0, 1.013, 1.049, 1.107, 1.187, 1.288, 1.41, 1.554, 1.721, 1.914], [1.0, 1.26, 1.524, 1.798, 2.089, 2.4, 2.739, 3.109, 3.518, 3.97], [1.0, 0.985, 0.973, 0.965, 0.962, 0.964, 0.973, 0.99, 1.017, 1.058]])

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
        return class_(
            [
                [round(_, 3) for _ in states[:iters, 0]],
                [round(_, 3) for _ in states[:iters, 1]],
                [round(_, 3) for _ in states[:iters, 2]],
            ]
        )

    @classmethod
    def lu_chen(class_, a, b, c, u, first_state, time_values, iters):
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
            Sequence([[0.1, 0.145, 0.143, 0.101, 0.022, -0.094, -0.251, -0.454, -0.71, -1.03], [0.3, 0.201, 0.08, -0.067, -0.249, -0.472, -0.747, -1.086, -1.504, -2.018], [-0.6, -0.582, -0.565, -0.548, -0.532, -0.516, -0.5, -0.482, -0.46, -0.431]])

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
        return class_(
            [
                [round(_, 3) for _ in states[:iters, 0]],
                [round(_, 3) for _ in states[:iters, 1]],
                [round(_, 3) for _ in states[:iters, 2]],
            ]
        )

    @classmethod
    def mandelbrot_set(class_, xmin, xmax, ymin, ymax, width, height, maxiter):
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
        return class_([r1, r2, n3])

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
        returned_seq = type(self)([mapping_dict[_] for _ in self.items])
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
        return type(self)(returned_list)

    @classmethod
    def markov(class_, transition_prob, first_state, length, seed):
        """

        .. container:: example

            >>> prob = {
            ...     "one": {"one": 0.8, "two": 0.19, "three": 0.01},
            ...     "two": {"one": 0.2, "two": 0.7, "three": 0.1},
            ...     "three": {"one": 0.1, "two": 0.2, "three": 0.7},
            ... }
            >>> evans.Sequence.markov(
            ...     transition_prob=prob,
            ...     first_state="one",
            ...     length=14,
            ...     seed=7,
            ... )
            Sequence(['one', 'one', 'one', 'one', 'two', 'two', 'two', 'one', 'one', 'one', 'one', 'two', 'two', 'one'])

        """
        chain = MarkovChain(transition_prob, seed)
        key_list = [
            x for x in chain.generate_states(current_state=first_state, no=length)
        ]
        seq = class_(key_list)
        return seq

    def matrix(self, padded=False):
        """

        .. container:: example

            >>> evans.Sequence([0, [1, 2], 3, [4, 5, 6, 7], [7, 8], 9]).matrix()
            Sequence([[Fraction(0, 1), Fraction(1, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(7, 1), Fraction(7, 1), Fraction(8, 1), Fraction(9, 1)], [Fraction(-1, 1), Fraction(0, 1), Fraction(1, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1), Fraction(6, 1), Fraction(7, 1), Fraction(8, 1)], [Fraction(-2, 1), Fraction(-1, 1), Fraction(0, 1), Fraction(1, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(5, 1), Fraction(5, 1), Fraction(6, 1), Fraction(7, 1)], [Fraction(-3, 1), Fraction(-2, 1), Fraction(-1, 1), Fraction(0, 1), Fraction(1, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1)], [Fraction(-4, 1), Fraction(-3, 1), Fraction(-2, 1), Fraction(-1, 1), Fraction(0, 1), Fraction(1, 1), Fraction(2, 1), Fraction(3, 1), Fraction(3, 1), Fraction(4, 1), Fraction(5, 1)], [Fraction(-5, 1), Fraction(-4, 1), Fraction(-3, 1), Fraction(-2, 1), Fraction(-1, 1), Fraction(0, 1), Fraction(1, 1), Fraction(2, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1)], [Fraction(-6, 1), Fraction(-5, 1), Fraction(-4, 1), Fraction(-3, 1), Fraction(-2, 1), Fraction(-1, 1), Fraction(0, 1), Fraction(1, 1), Fraction(1, 1), Fraction(2, 1), Fraction(3, 1)], [Fraction(-7, 1), Fraction(-6, 1), Fraction(-5, 1), Fraction(-4, 1), Fraction(-3, 1), Fraction(-2, 1), Fraction(-1, 1), Fraction(0, 1), Fraction(0, 1), Fraction(1, 1), Fraction(2, 1)], [Fraction(-7, 1), Fraction(-6, 1), Fraction(-5, 1), Fraction(-4, 1), Fraction(-3, 1), Fraction(-2, 1), Fraction(-1, 1), Fraction(0, 1), Fraction(0, 1), Fraction(1, 1), Fraction(2, 1)], [Fraction(-8, 1), Fraction(-7, 1), Fraction(-6, 1), Fraction(-5, 1), Fraction(-4, 1), Fraction(-3, 1), Fraction(-2, 1), Fraction(-1, 1), Fraction(-1, 1), Fraction(0, 1), Fraction(1, 1)], [Fraction(-9, 1), Fraction(-8, 1), Fraction(-7, 1), Fraction(-6, 1), Fraction(-5, 1), Fraction(-4, 1), Fraction(-3, 1), Fraction(-2, 1), Fraction(-2, 1), Fraction(-1, 1), Fraction(0, 1)]])

        .. container:: example

            >>> evans.Sequence([0, [1, 2], 3, [4, 5, 6, 7], [7, 8], 9]).matrix(padded=True)
            Sequence([[0, None, None, None], [1, 2, None, None], [3, None, None, None], [4, 5, 6, 7], [7, 8, None, None], [9, None, None, None]])

        """
        if not padded:
            row = PitchSegment([_ for _ in self])
            inverted_row = row.invert(row[0]).transpose(0 - row[0])
            material = type(self)(row).derive_added_sequences(inverted_row)
            return material
        else:
            out = []
            temp = type(self)()
            for _ in self:
                if not isinstance(_, list):
                    temp += [[_]]
                else:
                    temp += [_]
            sorted_self = type(self)(temp).sort(key=lambda x: len(x))
            largest = len(sorted_self[-1])
            for _ in temp:
                while len(_) < largest:
                    _.append(None)
                out.append(_)
            return type(self)(out)

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
            return type(self)(lst + lst[-2:0:-1])
        else:
            return type(self)(lst + lst[::-1])

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
        return type(self)(new_seq)

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
        return type(self)(returned_seq)

    def product(self):
        """

        .. container:: example

            >>> evans.Sequence([7, 8, 9, 10]).product()
            Sequence([5040])

        """
        x = 1
        for _ in self.items:
            x *= _
        return type(self)([x])

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
        return type(self)(returned_sequence)

    @classmethod
    def n_bonacci_cycle(
        class_, n, first_number, second_number, length, modulus, wrap_to_zero=False
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
        return class_(sequence)

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
        return type(self)(normalized_list)

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
        return type(self)(out)

    @classmethod
    def orbits(class_, initial_state=0.4, iterations=10):
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
        return class_(list_)

    def permutations(self):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2]).permutations()
            Sequence([[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]])

        .. container:: example

            >>> evans.Sequence([0, [1, 2], 3]).permutations()
            Sequence([[0, [1, 2], 3], [0, 3, [1, 2]], [[1, 2], 0, 3], [[1, 2], 3, 0], [3, 0, [1, 2]], [3, [1, 2], 0]])

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
                for p in type(self)(ba).permutations():
                    list_.append([x] + p)
            return type(self)(list_)

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
        return type(self)(pitch_list)

    def potamia(self, columns=False, retrograde=False):
        """

        .. container:: example

            >>> s = evans.Sequence([0, 1, [2, 3, 4], 5, [6, 7]]).matrix(padded=True)
            >>> s = s.potamia()
            >>> s.flatten().remove_none()
            Sequence([0, 1, 2, 3, 4, 5, 6, 7])

        .. container:: example

            >>> s = evans.Sequence([0, 1, [2, 3, 4], 5, [6, 7]]).matrix(padded=True)
            >>> s = s.potamia(columns=True)
            >>> s.flatten().remove_none()
            Sequence([0, 1, 2, 5, 6, 7, 3, 4])

        .. container:: example

            >>> s = evans.Sequence([0, 1, [2, 3, 4], 5, [6, 7]]).matrix(padded=True)
            >>> s = s.potamia(retrograde=True)
            >>> s.flatten().remove_none()
            Sequence([0, 1, 4, 3, 2, 5, 7, 6])

        .. container:: example

            >>> s = evans.Sequence([0, 1, [2, 3, 4], 5, [6, 7]]).matrix(padded=True)
            >>> s = s.potamia(columns=True, retrograde=True)
            >>> s.flatten().remove_none()
            Sequence([6, 5, 2, 1, 0, 3, 7, 4])

        """
        out = []
        array = numpy.array([_ for _ in self])
        if columns:
            array = array.transpose()
        for i, _ in enumerate(array):
            if not retrograde:
                if i % 2 == 0:
                    temp = [value for value in _]
                    out.append(temp)
                else:
                    temp = type(self)([value for value in _]).reverse()
                    out.append(temp)
            else:
                if i % 2 == 0:
                    temp = type(self)([value for value in _]).reverse()
                    out.append(temp)
                else:
                    temp = [value for value in _]
                    out.append(temp)
        return type(self)(out)

    @classmethod
    def prime_sequence(class_, start, end):
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
        return class_(seq)

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
        return type(self)(seq)

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
        return type(self)(final_list)

    @classmethod
    def ratio(class_, ratio, reciprocals=False):
        """

        .. container:: example

            >>> evans.Sequence.ratio("9:8:7:6:5:4")
            Sequence([Fraction(1, 1), Fraction(5, 4), Fraction(3, 2), Fraction(7, 4), Fraction(2, 1), Fraction(9, 4)])

        """
        ratio = Ratio(ratio)
        seq = ratio.extract_sub_ratios(
            as_fractions=True,
            reciprocal=reciprocals,
        )
        return class_([_ for _ in seq])

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
        return type(self)(returned_list)

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
        return type(self)(returned_list)

    def remove_none(self):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2, None, 3, None, 4, 5, None, None]).remove_none()
            Sequence([0, 1, 2, 3, 4, 5])

        """
        out = []
        for _ in self:
            if not isinstance(_, type(None)):
                out.append(_)
        return type(self)(out)

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
        return type(self)(collection)

    def rotate(self, n):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3]).rotate(2)
            Sequence([2, 3, 0, 1])

        """
        lst = list(self.items)
        return type(self)(lst[n:] + lst[:n])

    @classmethod
    def roessler(class_, a, b, c, t_ini, t_fin, h):
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
        return class_([x, y, z])

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
        seq = type(self)(returned_list)
        return seq

    def stack_pitches(self, as_ratios=False):
        """

        .. container:: example

            >>> s = evans.Sequence([1, -2, 3])
            >>> s.stack_pitches()
            Sequence([1, 10, 15])

        """
        returned_list = [self.items[0]]
        if as_ratios:
            for _ in self.items[1:]:
                while _ < returned_list[-1]:
                    _ *= 2
                returned_list.append(_)
            seq = type(self)(returned_list)
        else:
            for _ in self.items[1:]:
                while _ < returned_list[-1]:
                    _ += 12
                returned_list.append(_)
            seq = type(self)(returned_list)
        return seq

    def difference(self):
        """

        .. container:: example

            >>> l = [1, 2, 3, 4]
            >>> evans.Sequence(l).difference()
            Sequence([-8])

        """
        x = self.items[0]
        for _ in self.items[1:]:
            x -= _
        return type(self)([x])

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
        return type(self)(returned_list)

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
        return type(self)(final_list)

    def zipped_bifurcation(self, reversed=True):
        """

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3]).zipped_bifurcation()
            Sequence([0, 3, 1, 2])

        .. container:: example

            >>> evans.Sequence([0, 1, 2, 3]).zipped_bifurcation(reversed=False)
            Sequence([0, 2, 1, 3])

        """
        center = len(self) // 2
        first_half = self[:center]
        second_half = type(self)(self[center:])
        if reversed:
            second_half = second_half.reverse()
        out = [_ for _ in zip(first_half, second_half)]
        return type(self)(out).flatten()


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
