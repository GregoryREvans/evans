"""
Sequence classes and functions.
"""
import collections
import copy
import decimal
import itertools
import math
import random
import sys
import typing

import abjad
import black
import numpy
import quicktions
import scipy
from abjadext import microtones
from scipy.integrate import odeint
from scipy.ndimage import convolve

from . import consort


def is_coprime(a, b):
    return math.gcd(a, b) == 1


def integer_sequence_to_boolean_vector(integers, sides=[abjad.RIGHT]):
    cyc_side = CyclicList(sides, forget=False)
    out = []
    for i in integers:
        side = cyc_side(r=1)[0]
        falses = [False for _ in range(i - 1)]
        if side == abjad.RIGHT:
            sub_vector = falses + [True]
        elif side == abjad.LEFT:
            sub_vector = [True] + falses
        else:
            raise Exception(
                f"BAD DIRECTION. Must be abjad.LEFT or abjad.RIGHT. Got {side}"
            )
        out.extend(sub_vector)
    return out


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
        return f"<{type(self).__name__}()>"

    def __repr__(self):
        items = ", ".join([repr(_) for _ in self.lst])
        string = f"{type(self).__name__}([{items}])"
        return string

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
        return f"<{type(self).__name__}()>"

    def __repr__(self):
        items = ", ".join([repr(_) for _ in self.transition_prob])
        string = f"{type(self).__name__}([{items}])"
        return string

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


class KlumpenhouwerNetwork:
    def __init__(self, items):
        self.items = items

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, data):
        self.items[index] = data

    def __iter__(self):
        for item in self.items:
            yield item

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        string = str(self)
        string = black.format_str(string, mode=black.mode.Mode())
        return string

    def __str__(self):
        output = "("
        for i, item in enumerate(self.items):
            output += f"{item}"
            if i != len(self.items) - 1:
                output += ", "
        output += ")"
        return output

    def __add__(self, argument):
        if (
            isinstance(argument, PitchClassSet)
            or isinstance(argument, PitchClassSegment)
            or isinstance(argument, PitchSet)
            or isinstance(argument, PitchSegment)
        ):
            items = self.items + argument.pitches
        elif (
            isinstance(argument, RatioClassSet)
            or isinstance(argument, RatioClassSegment)
            or isinstance(argument, RatioSet)
            or isinstance(argument, RatioSegment)
        ):
            items = self.items + argument.ratios
        else:
            items = self.items + argument.items
        return type(self)(items)

    def __contains__(self, argument):
        return argument in self.items

    @staticmethod
    def _binary_value(i):
        value = 0
        for bit in i:
            value += 2**bit
        return value

    def alpha(self, category):
        numbers = [_.alpha(category) for _ in self]
        return type(self)(numbers)

    def constrain_to_octave(self):
        constrained = [_.constrain_to_octave() for _ in self]
        return type(self)(constrained)

    def complement(self, argument):
        complements = []
        for arg in argument:
            if arg not in self.items:
                complements.append(arg)
        return type(self)(complements)

    def hexpole(self):
        out = [_.hexpole() for _ in self]
        return type(self)(out)

    def invert(self, axis=1):
        inverse = [_.invert(axis) for _ in self]
        return type(self)(inverse)

    def leittonwechsel(self):
        out = [_.leittonwechsel() for _ in self]
        return type(self)(out)

    def multiply(self, n):
        multiplied_pitch_classes = [_.multiply(n) for _ in self]
        return type(self)(multiplied_pitch_classes)

    def nebenverwandt(self):
        out = [_.nebenverwandt() for _ in self]
        return type(self)(out)

    def octpole(self):
        out = [_.octpole() for _ in self]
        return type(self)(out)

    def parallel(self):
        out = [_.parallel() for _ in self]
        return type(self)(out)

    def prime_form(self):
        out = [_.prime_form() for _ in self]
        return type(self)(out)

    def relative(self):
        out = [_.relative() for _ in self]
        return type(self)(out)

    def retrograde(self):
        rev = [_.retrograde() for _ in self]
        return type(self)(rev)

    def rotate(self, n):
        copied_list = [_.rotate(n) for _ in self]
        return type(self)(copied_list)

    def slide(self):
        out = [_.slide() for _ in self]
        return type(self)(out)

    def sorted(self, recurse=False):
        try:
            sorted_self = [_.sorted(recurse=recurse) for _ in self]
        except:
            sorted_self = [_.sorted() for _ in self]
        return type(self)(sorted_self)

    def to_sequence(self):
        out = []
        for _ in self:
            if type(_) == type(self):
                out.append(Sequence([x.to_sequence() for x in _]))
            else:
                out.append(_.to_sequence())
        seq = Sequence(out)
        return seq

    def transpose(self, n):
        transposed = [_.transpose(n) for _ in self]
        return type(self)(transposed)

    def wedge(self, origin, destination, step_size):
        transposed = [_.wedge(origin, destination, step_size) for _ in self]
        return type(self)(transposed)


# # TODO: find a system to accumulate sequences derived from transforms of one of the following classes
# something like
# def accumulate_transforms(source=None, operations=None):
#     out = [source]
#     for operation in operations:
#         if len(operations) == 1:
#             # do one and append it
#             if operation == "h":
#                 out.append(out[1].hexpole())
#             elif operation == "l":
#                 out.append(out[1].leittonwechsel())
#             elif operation == "n":
#                 out.append(out[1].nebenverwandt())
#             elif operation == "o":
#                 out.append(out[1].octpole())
#             elif operation == "p":
#                 out.append(out[1].parallel())
#             elif operation == "r":
#                 out.append(out[1].relative())
#             elif operation == "s":
#                 out.append(out[1].slide())
#                 # add rp, pr, sl, ls, transpose by n, mod by n, alpha by n, permute by n, rotate by n, modalverwandt, dominant
#             else:
#                 raise Exception("OPERATIONS MUST BE THESE ONLY: XYZ...")
#         else:
#             temp = accumulate_transforms(out[-1], [_ for _ in operation])
#             out.append(temp[-1])


class PitchClassSet(microtones.PitchClassSet):
    def alpha(self, category):
        """

        .. container:: example

            >>> s = evans.PitchClassSet([_ for _ in range(12)])
            >>> s.alpha(category=1)
            {1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10}
            <BLANKLINE>

        .. container:: example

            >>> s = evans.PitchClassSet([_ for _ in range(12)])
            >>> s.alpha(category=2)
            {11, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 0}
            <BLANKLINE>

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

    def hexpole(self):
        out = (
            self.invert(0).transpose(11).invert(0).transpose(7).invert(0).transpose(11)
        )
        return out

    def leittonwechsel(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(11)
        return transposed

    def mod(self, i=12, preserve_negatives=False):
        if preserve_negatives is False:
            reduced = [_ % i for _ in self]
        else:
            reduced = [0 - (_ % i) if _ < 0 else _ % i for _ in self]
        return type(self)(reduced)

    def nebenverwandt(self):
        out = self.invert(0).transpose(4).invert(0).transpose(11).invert(0).transpose(7)
        return out

    def octpole(self):
        out = (
            self.invert(0)
            .transpose(7)
            .invert(0)
            .transpose(4)
            .invert(0)
            .transpose(7)
            .invert(0)
            .transpose(4)
        )
        return out

    def parallel(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(7)
        return transposed

    def relative(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(4)
        return transposed

    def slide(self):
        out = self.invert(0).transpose(11).invert(0).transpose(7).invert(0).transpose(4)
        return out

    def wedge(self, origin, destination, step_size):
        def is_left_of_desintation(arg):
            return (destination - arg) % 12 < (destination - origin) % 12

        out = []
        for _ in self:
            if _ == origin or _ == destination:  # correct
                out.append(_)
            elif is_left_of_desintation(_):  # ?
                temp = _ + step_size
                out.append(temp)
            elif not is_left_of_desintation(_):  # ?
                temp = _ - step_size
                out.append(temp)
            else:
                raise Exception(f"Improper value: {_}")
        return type(self)(out)


class PitchSet(microtones.PitchSet):
    def alpha(self, category):
        """

        .. container:: example

            >>> s = evans.PitchSet([_ for _ in range(12)])
            >>> s.alpha(category=1)
            {1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10}
            <BLANKLINE>

        .. container:: example

            >>> s = evans.PitchSet([_ for _ in range(12)])
            >>> s.alpha(category=2)
            {-1, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12}
            <BLANKLINE>

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

    def hexpole(self):
        out = (
            self.invert(0).transpose(11).invert(0).transpose(7).invert(0).transpose(11)
        )
        return out

    def leittonwechsel(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(11)
        return transposed

    def mod(self, i=12, preserve_negatives=False):
        if preserve_negatives is False:
            reduced = [_ % i for _ in self]
        else:
            reduced = [0 - (_ % i) if _ < 0 else _ % i for _ in self]
        return type(self)(reduced)

    def nebenverwandt(self):
        out = self.invert(0).transpose(4).invert(0).transpose(11).invert(0).transpose(7)
        return out

    def octpole(self):
        out = (
            self.invert(0)
            .transpose(7)
            .invert(0)
            .transpose(4)
            .invert(0)
            .transpose(7)
            .invert(0)
            .transpose(4)
        )
        return out

    def parallel(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(7)
        return transposed

    def relative(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(4)
        return transposed

    def slide(self):
        out = self.invert(0).transpose(11).invert(0).transpose(7).invert(0).transpose(4)
        return out

    def wedge(self, origin, destination, step_size):
        def is_left_of_desintation(arg):
            return (destination - arg) % 12 < (destination - origin) % 12

        out = []
        for _ in self:
            if _ == origin or _ == destination:  # correct
                out.append(_)
            elif is_left_of_desintation(_):  # ?
                temp = _ + step_size
                out.append(temp)
            elif not is_left_of_desintation(_):  # ?
                temp = _ - step_size
                out.append(temp)
            else:
                raise Exception(f"Improper value: {_}")
        return type(self)(out)


class PitchClassSegment(microtones.PitchClassSegment):
    def alpha(self, category):
        """

        .. container:: example

            >>> s = evans.PitchClassSegment([_ for _ in range(12)])
            >>> s.alpha(category=1)
            (1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10)
            <BLANKLINE>

        .. container:: example

            >>> s = evans.PitchClassSegment([_ for _ in range(12)])
            >>> s.alpha(category=2)
            (11, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 0)
            <BLANKLINE>

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

    def hexpole(self):
        out = (
            self.invert(0).transpose(11).invert(0).transpose(7).invert(0).transpose(11)
        )
        return out

    def leittonwechsel(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(11)
        return transposed

    def mod(self, i=12, preserve_negatives=False):
        if preserve_negatives is False:
            reduced = [_ % i for _ in self]
        else:
            reduced = [0 - (_ % i) if _ < 0 else _ % i for _ in self]
        return type(self)(reduced)

    def nebenverwandt(self):
        out = self.invert(0).transpose(4).invert(0).transpose(11).invert(0).transpose(7)
        return out

    def octpole(self):
        out = (
            self.invert(0)
            .transpose(7)
            .invert(0)
            .transpose(4)
            .invert(0)
            .transpose(7)
            .invert(0)
            .transpose(4)
        )
        return out

    def parallel(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(7)
        return transposed

    def relative(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(4)
        return transposed

    def slide(self):
        out = self.invert(0).transpose(11).invert(0).transpose(7).invert(0).transpose(4)
        return out

    def wedge(self, origin, destination, step_size):
        def is_left_of_desintation(arg):
            return (destination - arg) % 12 < (destination - origin) % 12

        out = []
        for _ in self:
            if _ == origin or _ == destination:  # correct
                out.append(_)
            elif is_left_of_desintation(_):  # ?
                temp = _ + step_size
                out.append(temp)
            elif not is_left_of_desintation(_):  # ?
                temp = _ - step_size
                out.append(temp)
            else:
                raise Exception(f"Improper value: {_}")
        return type(self)(out)


class PitchSegment(microtones.PitchSegment):
    def alpha(self, category):
        """

        .. container:: example

            >>> s = evans.PitchSegment([_ for _ in range(12)])
            >>> s.alpha(category=1)
            (1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10)
            <BLANKLINE>

        .. container:: example

            >>> s = evans.PitchSegment([_ for _ in range(12)])
            >>> s.alpha(category=2)
            (-1, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12)
            <BLANKLINE>

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

    def hexpole(self):
        out = (
            self.invert(0).transpose(11).invert(0).transpose(7).invert(0).transpose(11)
        )
        return out

    def leittonwechsel(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(11)
        return transposed

    def mod(self, i=12, preserve_negatives=False):
        if preserve_negatives is False:
            reduced = [_ % i for _ in self]
        else:
            reduced = [0 - (_ % i) if _ < 0 else _ % i for _ in self]
        return type(self)(reduced)

    def nebenverwandt(self):
        out = self.invert(0).transpose(4).invert(0).transpose(11).invert(0).transpose(7)
        return out

    def octpole(self):
        out = (
            self.invert(0)
            .transpose(7)
            .invert(0)
            .transpose(4)
            .invert(0)
            .transpose(7)
            .invert(0)
            .transpose(4)
        )
        return out

    def parallel(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(7)
        return transposed

    def relative(self):
        inverse = self.invert(0)
        transposed = inverse.transpose(4)
        return transposed

    def slide(self):
        out = self.invert(0).transpose(11).invert(0).transpose(7).invert(0).transpose(4)
        return out

    def wedge(self, origin, destination, step_size):
        def is_left_of_desintation(arg):
            return (destination - arg) % 12 < (destination - origin) % 12

        out = []
        for _ in self:
            if _ == origin or _ == destination:  # correct
                out.append(_)
            elif is_left_of_desintation(_):  # ?
                temp = _ + step_size
                out.append(temp)
            elif not is_left_of_desintation(_):  # ?
                temp = _ - step_size
                out.append(temp)
            else:
                raise Exception(f"Improper value: {_}")
        return type(self)(out)


class RatioClassSet(microtones.RatioClassSet):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.ratio_classes])
        return seq

    # EXPERIMENTAL

    def hexpole(self):
        out = (
            self.invert("1/1")
            .multiply("15/8")
            .invert("1/1")
            .multiply("3/2")
            .invert("1/1")
            .multiply("15/8")
        )
        return out

    def leittonwechsel(self):
        inverse = self.invert("1/1")
        transposed = inverse.multiply("15/8")
        return transposed

    def nebenverwandt(self):
        out = (
            self.invert("1/1")
            .multiply("5/4")
            .invert("1/1")
            .multiply("15/8")
            .invert("1/1")
            .multiply("3/2")
        )
        return out

    def parallel(self):
        inverse = self.invert("1/1")
        transposed = inverse.multiply("3/2")
        return transposed

    def relative(self):
        inverse = self.invert("1/1")
        transposed = inverse.multiply("5/4")
        return transposed

    def slide(self):
        out = (
            self.invert("1/1")
            .multiply("15/8")
            .invert("1/1")
            .multiply("3/2")
            .invert("1/1")
            .multiply("5/4")
        )
        return out

    def wedge(self, origin, destination, step_size):
        raise Exception(f"Wedge Operation Not Yet Implemented for {type(self)}")


class RatioSet(microtones.RatioSet):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.ratios])
        return seq

    def wedge(self, origin, destination, step_size):
        raise Exception(f"Wedge Operation Not Yet Implemented for {type(self)}")


class RatioClassSegment(microtones.RatioClassSegment):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.ratio_classes])
        return seq

    def wedge(self, origin, destination, step_size):
        raise Exception(f"Wedge Operation Not Yet Implemented for {type(self)}")


class RatioSegment(microtones.RatioSegment):
    def to_sequence(self):
        seq = Sequence([_ for _ in self.ratios])
        return seq

    def wedge(self, origin, destination, step_size):
        raise Exception(f"Wedge Operation Not Yet Implemented for {type(self)}")


class Ratio(abjad.Ratio):
    def extract_sub_ratios(self, reciprocal=False, as_fractions=False):
        """

        .. container:: example

            >>> ratio = evans.Ratio('9:8:7:6:5:4:3:2')
            >>> ratio.extract_sub_ratios()
            Sequence([Ratio(numbers=(1, 1)), Ratio(numbers=(3, 2)), Ratio(numbers=(2, 1)), Ratio(numbers=(5, 2)), Ratio(numbers=(3, 1)), Ratio(numbers=(7, 2)), Ratio(numbers=(4, 1)), Ratio(numbers=(9, 2))])

        .. container:: example

            >>> ratio = evans.Ratio('9:8:7:6:5:4:3:2')
            >>> ratio.extract_sub_ratios(reciprocal=True)
            Sequence([Ratio(numbers=(1, 1)), Ratio(numbers=(2, 3)), Ratio(numbers=(1, 2)), Ratio(numbers=(2, 5)), Ratio(numbers=(1, 3)), Ratio(numbers=(2, 7)), Ratio(numbers=(1, 4)), Ratio(numbers=(2, 9))])

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


class Sequence(collections.abc.Sequence):

    """
    Sequence.

    ..  container:: example

        Initializes sequence:

        ..  container:: example

            >>> evans.Sequence([1, 2, 3, 4, 5, 6])
            Sequence([1, 2, 3, 4, 5, 6])

    ..  container:: example

        Initializes and reverses sequence:

        ..  container:: example

            >>> sequence = evans.Sequence([1, 2, 3, 4, 5, 6])
            >>> sequence.reverse()
            Sequence([6, 5, 4, 3, 2, 1])

    ..  container:: example

        Initializes, reverses and flattens sequence:

        ..  container:: example

            >>> sequence = evans.Sequence([1, 2, 3, [4, 5, [6]]])
            >>> sequence = sequence.reverse()
            >>> sequence = sequence.flatten(depth=-1)
            >>> sequence
            Sequence([4, 5, 6, 3, 2, 1])

    ..  container:: example

        REGRESSION:

        >>> evans.Sequence(0)
        Sequence([0])

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_items",)

    ### INITIALIZER ###

    def __init__(self, items=None):
        if items is None:
            items = ()
        if not isinstance(items, collections.abc.Iterable):
            items = [items]
        self._items = tuple(items)

    ### SPECIAL METHODS ###

    def __add__(self, argument) -> "Sequence":
        r"""
        Adds ``argument`` to sequence.

        ..  container:: example

            Adds tuple to sequence:

            ..  container:: example

                >>> evans.Sequence([1, 2, 3]) + (4, 5, 6)
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds list to sequence:

            ..  container:: example

                >>> evans.Sequence([1, 2, 3]) + [4, 5, 6]
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds sequence to sequence:

            ..  container:: example

                >>> sequence_1 = evans.Sequence([1, 2, 3])
                >>> sequence_2 = evans.Sequence([4, 5, 6])
                >>> sequence_1 + sequence_2
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Reverses result:

            ..  container:: example

                >>> sequence_1 = evans.Sequence([1, 2, 3])
                >>> sequence_2 = evans.Sequence([4, 5, 6])
                >>> sequence = sequence_1 + sequence_2
                >>> sequence.reverse()
                Sequence([6, 5, 4, 3, 2, 1])

        """
        argument = type(self)(items=argument)
        items = self.items + argument.items
        return type(self)(items)

    def __eq__(self, argument) -> bool:
        """
        Compares ``items``.

        ..  container:: example

            Is true when ``argument`` is a sequence with items equal to those
            of this sequence:

            >>> evans.Sequence([1, 2, 3, 4, 5, 6]) == evans.Sequence([1, 2, 3, 4, 5, 6])
            True

        ..  container:: example

            Is false when ``argument`` is not a sequence with items equal to
            those of this sequence:

            >>> evans.Sequence([1, 2, 3, 4, 5, 6]) == ([1, 2, 3, 4, 5, 6])
            False

        """
        if isinstance(argument, type(self)):
            return self.items == argument.items
        return False

    def __getitem__(self, argument) -> typing.Any:
        r"""
        Gets item or slice identified by ``argument``.

        ..  container:: example

            Gets first item in sequence:

            ..  container:: example

                >>> sequence = evans.Sequence([1, 2, 3, 4, 5, 6])

                >>> sequence[0]
                1

        ..  container:: example

            Gets last item in sequence:

            ..  container:: example

                >>> sequence = evans.Sequence([1, 2, 3, 4, 5, 6])

                >>> sequence[-1]
                6

        ..  container:: example

            Gets slice from sequence:

            ..  container:: example

                >>> sequence = evans.Sequence([1, 2, 3, 4, 5, 6])
                >>> sequence = sequence[:3]

                >>> sequence
                Sequence([1, 2, 3])

        ..  container:: example

            Gets item in sequence and wraps result in new sequence:

            ..  container:: example

                >>> sequence = evans.Sequence([1, 2, 3, 4, 5, 6])
                >>> sequence = evans.Sequence(sequence[0])

                >>> sequence
                Sequence([1])

        ..  container:: example

            Gets slice from sequence and flattens slice:

            ..  container:: example

                >>> sequence = evans.Sequence([1, 2, [3, [4]], 5])
                >>> sequence = sequence[:-1]
                >>> sequence = sequence.flatten(depth=-1)

                >>> sequence
                Sequence([1, 2, 3, 4])

        Returns item or new sequence.
        """
        result = self._items.__getitem__(argument)
        if isinstance(argument, slice):
            return type(self)(result)
        return result

    def __hash__(self) -> int:
        """
        Hashes sequence.
        """
        return hash(self.__class__.__name__ + str(self))

    def __len__(self) -> int:
        """
        Gets length of sequence.

        ..  container:: example

            Gets length of sequence:

            >>> len(evans.Sequence([1, 2, 3, 4, 5, 6]))
            6

        ..  container:: example

            Gets length of sequence:

            >>> len(evans.Sequence('text'))
            4

        """
        return len(self._items)

    def __radd__(self, argument) -> "Sequence":
        r"""
        Adds sequence to ``argument``.

        ..  container:: example

            Adds sequence to tuple:

            ..  container:: example

                >>> (1, 2, 3) + evans.Sequence([4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds sequence to list:

            ..  container:: example

                >>> [1, 2, 3] + evans.Sequence([4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds sequence to sequence:

            ..  container:: example

                >>> evans.Sequence([1, 2, 3]) + evans.Sequence([4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

        """
        argument = type(self)(items=argument)
        items = argument.items + self.items
        return type(self)(items)

    def __repr__(self) -> str:
        """
        Gets interpreter representation of sequence.

        ..  container:: example

            Gets interpreter representation:

            >>> evans.Sequence([99])
            Sequence([99])

        ..  container:: example

            Gets interpreter representation:

            >>> evans.Sequence([1, 2, 3, 4, 5, 6])
            Sequence([1, 2, 3, 4, 5, 6])

        """
        items = ", ".join([repr(_) for _ in self.items])
        string = f"{type(self).__name__}([{items}])"
        return string

    ### PRIVATE METHODS ###

    # creates an iterator that can generate a flattened list,
    # descending down into child elements to a depth given in the arguments.
    # note that depth < 0 is effectively equivalent to infinity.
    @staticmethod
    def _flatten_helper(sequence, classes, depth):
        if not isinstance(sequence, classes):
            yield sequence
        elif depth == 0:
            for item in sequence:
                yield item
        else:
            for item in sequence:
                # flatten an iterable by one level
                depth_ = depth - 1
                for item_ in Sequence._flatten_helper(item, classes, depth_):
                    yield item_

    @classmethod
    def _partition_sequence_cyclically_by_weights_at_least(
        class_, sequence, weights, overhang=False
    ):
        l_copy = list(sequence)
        result = []
        current_part = []
        target_weight_index = 0
        len_weights = len(weights)
        while l_copy:
            target_weight = weights[target_weight_index % len_weights]
            item = l_copy.pop(0)
            current_part.append(item)
            if target_weight <= abjad.math.weight(current_part):
                result.append(current_part)
                current_part = []
                target_weight_index += 1
        assert not l_copy
        if current_part:
            if overhang:
                result.append(current_part)
        # return result
        result = [class_(_) for _ in result]
        return class_(items=result)

    @classmethod
    def _partition_sequence_cyclically_by_weights_at_most(
        class_, sequence, weights, overhang=False
    ):
        result = []
        current_part = []
        current_target_weight_index = 0
        current_target_weight = weights[current_target_weight_index]
        l_copy = list(sequence)
        while l_copy:
            current_target_weight = weights[current_target_weight_index % len(weights)]
            item = l_copy.pop(0)
            current_part_weight = abjad.math.weight(current_part)
            candidate_part_weight = current_part_weight + abjad.math.weight([item])
            if candidate_part_weight < current_target_weight:
                current_part.append(item)
            elif candidate_part_weight == current_target_weight:
                current_part.append(item)
                result.append(current_part)
                current_part = []
                current_target_weight_index += 1
            elif current_target_weight < candidate_part_weight:
                if current_part:
                    l_copy.insert(0, item)
                    result.append(current_part)
                    current_part = []
                    current_target_weight_index += 1
                else:
                    raise Exception("elements in sequence too big.")
            else:
                raise ValueError("candidate and target rates must compare.")
        if current_part:
            if overhang:
                result.append(current_part)
        # return result
        result = [class_(_) for _ in result]
        return class_(items=result)

    @classmethod
    def _partition_sequence_once_by_weights_at_least(
        class_, sequence, weights, overhang=False
    ):
        result = []
        current_part = []
        l_copy = list(sequence)
        for num_weight, target_weight in enumerate(weights):
            while True:
                try:
                    item = l_copy.pop(0)
                except IndexError:
                    if num_weight + 1 == len(weights):
                        if current_part:
                            result.append(current_part)
                            break
                    raise Exception("too few elements in sequence.")
                current_part.append(item)
                if target_weight <= abjad.math.weight(current_part):
                    result.append(current_part)
                    current_part = []
                    break
        if l_copy:
            if overhang:
                result.append(l_copy)
        result = [class_(_) for _ in result]
        return class_(items=result)

    @classmethod
    def _partition_sequence_once_by_weights_at_most(
        class_, sequence, weights, overhang=False
    ):
        l_copy = list(sequence)
        result = []
        current_part = []
        for target_weight in weights:
            while True:
                try:
                    item = l_copy.pop(0)
                except IndexError:
                    raise Exception("too few elements in sequence.")
                current_weight = abjad.math.weight(current_part)
                candidate_weight = current_weight + abjad.math.weight([item])
                if candidate_weight < target_weight:
                    current_part.append(item)
                elif candidate_weight == target_weight:
                    current_part.append(item)
                    result.append(current_part)
                    current_part = []
                    break
                elif target_weight < candidate_weight:
                    if current_part:
                        result.append(current_part)
                        current_part = []
                        l_copy.insert(0, item)
                        break
                    else:
                        raise Exception("elements in sequence too big.")
                else:
                    raise ValueError("candidate and target weights must compare.")
        if overhang:
            left_over = current_part + l_copy
            if left_over:
                result.append(left_over)
        result = [class_(_) for _ in result]
        return class_(items=result)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self) -> typing.Tuple[typing.Any, ...]:
        """
        Gets sequence items.

        ..  container:: example

            ..  container:: example

                Initializes items positionally:

                >>> evans.Sequence([1, 2, 3, 4, 5, 6]).items
                (1, 2, 3, 4, 5, 6)

                Initializes items from keyword:

                >>> evans.Sequence([1, 2, 3, 4, 5, 6]).items
                (1, 2, 3, 4, 5, 6)

        """
        return self._items

    ### PUBLIC METHODS ###

    def get_intervals(self, direction="literal"):  # no ratios yet
        if direction == "literal":
            intervals = [_[1] - _[0] for _ in self.nwise(2)]
        elif direction == "up":
            stacked_row = self.stack_pitches(direction="up")
            intervals = [_[1] - _[0] for _ in stacked_row.nwise(2)]
        elif direction == "down":
            stacked_row = self.stack_pitches(direction="down")
            intervals = [_[1] - _[0] for _ in stacked_row.nwise(2)]  # interval classes?
        else:
            raise Exception(f"direction must be literal, up, or down! not {direction}")
        return type(self)(intervals)

    def helianthate(sequence, n=0, m=0):
        start = list(sequence[:])
        result = list(sequence[:])
        assert isinstance(n, int), repr(n)
        assert isinstance(m, int), repr(m)
        original_n = n
        original_m = m

        def _generalized_rotate(argument, n=0):
            if hasattr(argument, "rotate"):
                return argument.rotate(n=n)
            argument_type = type(argument)
            argument = type(sequence)(argument).rotate(n=n)
            argument = argument_type(argument)
            return argument

        i = 0
        while True:
            inner = [_generalized_rotate(_, m) for _ in sequence]
            candidate = _generalized_rotate(inner, n)
            if candidate == start:
                break
            result.extend(candidate)
            n += original_n
            m += original_m
            i += 1
            if i == 1000:
                message = "1000 iterations without identity."
                raise Exception(message)
        return type(sequence)(result)

    def filter(self, predicate=None) -> "Sequence":
        """
        Filters sequence by ``predicate``.

        ..  container:: example

            By length:

            >>> items = [[1], [2, 3, [4]], [5], [6, 7, [8]]]
            >>> sequence = evans.Sequence(items)

            >>> sequence.filter(lambda _: len(_) == 1)
            Sequence([[1], [5]])

            By duration:

            >>> staff = abjad.Staff("c'4. d'8 e'4. f'8 g'2")
            >>> sequence = evans.Sequence(staff)

            >>> sequence.filter(lambda _: _.written_duration == abjad.Duration(1, 8))
            Sequence([Note("d'8"), Note("f'8")])

        """
        if predicate is None:
            return self[:]
        items = []
        for item in self:
            if predicate(item):
                items.append(item)
        return type(self)(items)

    def flatten(self, classes=None, depth=1) -> "Sequence":
        r"""
        Flattens sequence.

        ..  container:: example

            Flattens sequence:

            ..  container:: example

                >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                >>> sequence = evans.Sequence(items)

                >>> sequence.flatten()
                Sequence([1, 2, 3, [4], 5, 6, 7, [8]])

        ..  container:: example

            Flattens sequence to depth 2:

            ..  container:: example

                >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                >>> sequence = evans.Sequence(items)

                >>> sequence.flatten(depth=2)
                Sequence([1, 2, 3, 4, 5, 6, 7, 8])

        ..  container:: example

            Flattens sequence to depth -1:

            ..  container:: example

                >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                >>> sequence = evans.Sequence(items)

                >>> sequence.flatten(depth=-1)
                Sequence([1, 2, 3, 4, 5, 6, 7, 8])

        ..  container:: example

            Flattens tuples in sequence only:

            ..  container:: example

                >>> items = ['ab', 'cd', ('ef', 'gh'), ('ij', 'kl')]
                >>> sequence = evans.Sequence(items)

                >>> sequence.flatten(classes=(tuple,))
                Sequence(['ab', 'cd', 'ef', 'gh', 'ij', 'kl'])

        """
        if classes is None:
            classes = (collections.abc.Sequence,)
        if Sequence not in classes:
            classes = tuple(list(classes) + [Sequence])
        items = self._flatten_helper(self, classes, depth)
        return type(self)(items)

    def group_by(self, predicate=None) -> "Sequence":
        """
        Groups sequence items by value of items.

        ..  container:: example

            >>> items = [0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5]
            >>> sequence = evans.Sequence(items)
            >>> for item in sequence.group_by():
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1, -1])
            Sequence([2])
            Sequence([3])
            Sequence([-5])
            Sequence([1, 1])
            Sequence([5])
            Sequence([-5])

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d' d' e' e' e'")
            >>> predicate = lambda _: abjad.PitchSet([_.written_pitch])
            >>> for item in evans.Sequence(staff).group_by(predicate):
            ...     item
            ...
            Sequence([Note("c'8")])
            Sequence([Note("d'8"), Note("d'8")])
            Sequence([Note("e'8"), Note("e'8"), Note("e'8")])

        Returns nested sequence.
        """
        items = []
        if predicate is None:
            pairs = itertools.groupby(self, lambda _: _)
            for count, group in pairs:
                item = type(self)(group)
                items.append(item)
        else:
            pairs = itertools.groupby(self, predicate)
            for count, group in pairs:
                item = type(self)(group)
                items.append(item)
        return type(self)(items)

    def is_decreasing(self, strict=True) -> bool:
        """
        Is true when sequence decreases.

        ..  container:: example

            Is true when sequence is strictly decreasing:

            >>> evans.Sequence([5, 4, 3, 2, 1, 0]).is_decreasing(strict=True)
            True

            >>> evans.Sequence([3, 3, 3, 2, 1, 0]).is_decreasing(strict=True)
            False

            >>> evans.Sequence([3, 3, 3, 3, 3, 3]).is_decreasing(strict=True)
            False

            >>> evans.Sequence().is_decreasing(strict=True)
            True

        ..  container:: example

            Is true when sequence decreases monotonically:

            >>> evans.Sequence([5, 4, 3, 2, 1, 0]).is_decreasing(strict=False)
            True

            >>> evans.Sequence([3, 3, 3, 2, 1, 0]).is_decreasing(strict=False)
            True

            >>> evans.Sequence([3, 3, 3, 3, 3, 3]).is_decreasing(strict=False)
            True

            >>> evans.Sequence().is_decreasing(strict=False)
            True

        """
        if strict:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not current < previous:
                            return False
                    previous = current
                return True
            except TypeError:
                return False
        else:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not current <= previous:
                            return False
                    previous = current
                return True
            except TypeError:
                return False

    def is_increasing(self, strict=True) -> bool:
        """
        Is true when sequence increases.

        ..  container:: example

            Is true when sequence is strictly increasing:

            >>> evans.Sequence([0, 1, 2, 3, 4, 5]).is_increasing(strict=True)
            True

            >>> evans.Sequence([0, 1, 2, 3, 3, 3]).is_increasing(strict=True)
            False

            >>> evans.Sequence([3, 3, 3, 3, 3, 3]).is_increasing(strict=True)
            False

            >>> evans.Sequence().is_increasing(strict=True)
            True

        ..  container:: example

            Is true when sequence increases monotonically:

            >>> evans.Sequence([0, 1, 2, 3, 4, 5]).is_increasing(strict=False)
            True

            >>> evans.Sequence([0, 1, 2, 3, 3, 3]).is_increasing(strict=False)
            True

            >>> evans.Sequence([3, 3, 3, 3, 3, 3]).is_increasing(strict=False)
            True

            >>> evans.Sequence().is_increasing(strict=False)
            True

        """
        if strict:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not previous < current:
                            return False
                    previous = current
                return True
            except TypeError:
                return False
        else:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not previous <= current:
                            return False
                    previous = current
                return True
            except TypeError:
                return False

    def is_permutation(self, length=None) -> bool:
        """
        Is true when sequence is a permutation.

        ..  container:: example

            Is true when sequence is a permutation:

            >>> evans.Sequence([4, 5, 0, 3, 2, 1]).is_permutation()
            True

        ..  container:: example

            Is false when sequence is not a permutation:

            >>> evans.Sequence([1, 1, 5, 3, 2, 1]).is_permutation()
            False

        """
        return tuple(sorted(self)) == tuple(range(len(self)))

    def is_repetition_free(self) -> bool:
        """
        Is true when sequence is repetition-free.

        ..  container:: example

            Is true when sequence is repetition-free:

            >>> evans.Sequence([0, 1, 2, 6, 7, 8]).is_repetition_free()
            True

        ..  container:: example

            Is true when sequence is empty:

            >>> evans.Sequence().is_repetition_free()
            True

        ..  container:: example

            Is false when sequence contains repetitions:

            >>> evans.Sequence([0, 1, 2, 2, 7, 8]).is_repetition_free()
            False

        """
        try:
            for left, right in self.nwise():
                if left == right:
                    return False
            return True
        except TypeError:
            return False

    def join(self) -> "Sequence":
        r"""
        Join subsequences in ``sequence``.

        ..  container:: example

            >>> items = [(1, 2, 3), (), (4, 5), (), (6,)]
            >>> sequence = evans.Sequence(items)
            >>> sequence
            Sequence([(1, 2, 3), (), (4, 5), (), (6,)])

            >>> sequence.join()
            Sequence([(1, 2, 3, 4, 5, 6)])

        """
        if not self:
            return type(self)()
        item = self[0]
        for item_ in self[1:]:
            item += item_
        return type(self)([item])

    def map(self, operand=None) -> "Sequence":
        r"""
        Maps ``operand`` to sequence items.

        ..  container:: example

            Partitions sequence and sums parts:

            ..  container:: example

                >>> sequence = evans.Sequence(range(1, 10+1))
                >>> sequence = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     )
                >>> sequence = sequence.map(sum)

                >>> sequence
                Sequence([6, 15, 24])

        ..  container:: example

            Maps identity:

            >>> sequence = evans.Sequence([1, 2, 3, 4, 5, 6])
            >>> sequence.map()
            Sequence([1, 2, 3, 4, 5, 6])

        """
        if operand is not None:
            items = []
            for i, item_ in enumerate(self):
                item_ = operand(item_)
                items.append(item_)
        else:
            items = list(self.items[:])
        return type(self)(items)

    def nwise(self, n=2, cyclic=False, wrapped=False) -> typing.Generator:
        """
        Iterates sequence ``n`` at a time.

        ..  container:: example

            Iterates iterable by pairs:

            >>> sequence = evans.Sequence(range(10))
            >>> for item in sequence.nwise():
            ...     item
            ...
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])
            Sequence([5, 6])
            Sequence([6, 7])
            Sequence([7, 8])
            Sequence([8, 9])

        ..  container:: example

            Iterates iterable by triples:

            >>> sequence = evans.Sequence(range(10))
            >>> for item in sequence.nwise(n=3):
            ...     item
            ...
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])
            Sequence([5, 6, 7])
            Sequence([6, 7, 8])
            Sequence([7, 8, 9])

        ..  container:: example

            Iterates iterable by pairs. Wraps around at end:

            >>> sequence = evans.Sequence(range(10))
            >>> for item in sequence.nwise(n=2, wrapped=True):
            ...     item
            ...
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])
            Sequence([5, 6])
            Sequence([6, 7])
            Sequence([7, 8])
            Sequence([8, 9])
            Sequence([9, 0])

        ..  container:: example

            Iterates iterable by triples. Wraps around at end:

            >>> sequence = evans.Sequence(range(10))
            >>> for item in sequence.nwise(n=3, wrapped=True):
            ...     item
            ...
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])
            Sequence([5, 6, 7])
            Sequence([6, 7, 8])
            Sequence([7, 8, 9])
            Sequence([8, 9, 0])
            Sequence([9, 0, 1])

        ..  container:: example

            Iterates iterable by pairs. Cycles indefinitely:

            >>> sequence = evans.Sequence(range(10))
            >>> pairs = sequence.nwise(n=2, cyclic=True)
            >>> for _ in range(15):
            ...     next(pairs)
            ...
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])
            Sequence([5, 6])
            Sequence([6, 7])
            Sequence([7, 8])
            Sequence([8, 9])
            Sequence([9, 0])
            Sequence([0, 1])
            Sequence([1, 2])
            Sequence([2, 3])
            Sequence([3, 4])
            Sequence([4, 5])

            Returns infinite generator.

        ..  container:: example

            Iterates iterable by triples. Cycles indefinitely:

            >>> sequence = evans.Sequence(range(10))
            >>> triples = sequence.nwise(n=3, cyclic=True)
            >>> for _ in range(15):
            ...     next(triples)
            ...
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])
            Sequence([5, 6, 7])
            Sequence([6, 7, 8])
            Sequence([7, 8, 9])
            Sequence([8, 9, 0])
            Sequence([9, 0, 1])
            Sequence([0, 1, 2])
            Sequence([1, 2, 3])
            Sequence([2, 3, 4])
            Sequence([3, 4, 5])
            Sequence([4, 5, 6])

            Returns infinite generator.

        ..  container:: example

            Iterates items one at a time:

            >>> sequence = evans.Sequence(range(10))
            >>> for item in sequence.nwise(n=1):
            ...     item
            ...
            Sequence([0])
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4])
            Sequence([5])
            Sequence([6])
            Sequence([7])
            Sequence([8])
            Sequence([9])

        Ignores ``wrapped`` when ``cyclic`` is true.
        """
        if cyclic:
            item_buffer = []
            long_enough = False
            for item in self:
                item_buffer.append(item)
                if not long_enough:
                    if n <= len(item_buffer):
                        long_enough = True
                if long_enough:
                    yield type(self)(item_buffer[-n:])
            len_sequence = len(item_buffer)
            current = len_sequence - n + 1
            while True:
                output = []
                for local_offset in range(n):
                    index = (current + local_offset) % len_sequence
                    output.append(item_buffer[index])
                yield type(self)(output)
                current += 1
                current %= len_sequence
        elif wrapped:
            first_n_minus_1: typing.List[typing.Any] = []
            item_buffer = []
            for item in self:
                item_buffer.append(item)
                if len(item_buffer) == n:
                    yield type(self)(item_buffer)
                    item_buffer.pop(0)
                if len(first_n_minus_1) < n - 1:
                    first_n_minus_1.append(item)
            item_buffer = item_buffer + first_n_minus_1
            if item_buffer:
                for x in range(n - 1):
                    stop = x + n
                    yield type(self)(item_buffer[x:stop])
        else:
            item_buffer = []
            for item in self:
                item_buffer.append(item)
                if len(item_buffer) == n:
                    yield type(self)(item_buffer)
                    item_buffer.pop(0)

    def order_pitch_sequence_by_tonerow(
        self, tonerow, return_pitch_classes=True, prefer_lowest_pitch=True
    ):
        sequence = [abjad.NumberedPitchClass(_) for _ in self]
        pc_tonerow = [abjad.NumberedPitchClass(_) for _ in tonerow]
        out = []
        for pitch_class in pc_tonerow:
            if pitch_class in sequence:
                if return_pitch_classes is True:
                    out.append(pitch_class.number)
                else:
                    found_matches = [
                        _ for _ in self if abjad.NumberedPitchClass(_) == pitch_class
                    ]
                    if prefer_lowest_pitch is True:
                        out.append(abjad.NumberedPitch(found_matches[0]).number)
                    else:
                        out.append(abjad.NumberedPitch(found_matches[-1]).number)
        return type(self)(out)

    def partition_by_counts(
        self,
        counts,
        cyclic=False,
        enchain=False,
        overhang=False,
        reversed_=False,
    ) -> "Sequence":
        r"""
        Partitions sequence by ``counts``.

        ..  container:: example

            Partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> sequence = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )

                >>> sequence
                Sequence([Sequence([0, 1, 2])])

                >>> for part in sequence:
                ...     part
                Sequence([0, 1, 2])

        ..  container:: example

            Partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])

        ..  container:: example

            Partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5])
                Sequence([6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14])

        ..  container:: example

            Partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10])
                Sequence([11, 12, 13])

        ..  container:: example

            Partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

        ..  container:: example

            Partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10, 11, 12, 13, 14, 15])

        ..  container:: example

            Partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5])
                Sequence([6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14])
                Sequence([15])

        ..  container:: example

            Partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9, 10])
                Sequence([11, 12, 13])
                Sequence([14, 15])

        ..  container:: example

            Reverse-partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence once by counts without overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9])
                Sequence([10, 11, 12])
                Sequence([13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence cyclically by counts without overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=False,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
                Sequence([13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence once by counts with overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0])
                Sequence([1, 2, 3])
                Sequence([4, 5, 6])
                Sequence([7, 8, 9])
                Sequence([10, 11, 12])
                Sequence([13, 14, 15])

        ..  container:: example

            Reverse-partitions sequence cyclically by counts with overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [4, 3],
                ...     cyclic=True,
                ...     overhang=True,
                ...     reversed_=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14, 15])

        ..  container:: example

            Partitions sequence once by counts and asserts that sequence
            partitions exactly (with no overhang):

            ..  container:: example

                >>> sequence = evans.Sequence(range(10))
                >>> parts = sequence.partition_by_counts(
                ...     [2, 3, 5],
                ...     cyclic=False,
                ...     overhang=abjad.EXACT,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([2, 3, 4])
                Sequence([5, 6, 7, 8, 9])

        ..  container:: example

            Partitions sequence cyclically by counts and asserts that sequence
            partitions exactly Exact partitioning means partitioning with no
            overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(10))
                >>> parts = sequence.partition_by_counts(
                ...     [2],
                ...     cyclic=True,
                ...     overhang=abjad.EXACT,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([2, 3])
                Sequence([4, 5])
                Sequence([6, 7])
                Sequence([8, 9])

        ..  container:: example

            Partitions string:

            ..  container:: example

                >>> sequence = evans.Sequence('some text')
                >>> parts = sequence.partition_by_counts(
                ...     [3],
                ...     cyclic=False,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence(['s', 'o', 'm'])
                Sequence(['e', ' ', 't', 'e', 'x', 't'])

        ..  container:: example

            Partitions sequence cyclically into enchained parts by counts;
            truncates overhang:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [2, 6],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=False,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([1, 2, 3, 4, 5, 6])
                Sequence([6, 7])
                Sequence([7, 8, 9, 10, 11, 12])
                Sequence([12, 13])

        ..  container:: example

            Partitions sequence cyclically into enchained parts by counts;
            returns overhang at end:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [2, 6],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1])
                Sequence([1, 2, 3, 4, 5, 6])
                Sequence([6, 7])
                Sequence([7, 8, 9, 10, 11, 12])
                Sequence([12, 13])
                Sequence([13, 14, 15])

        ..  container:: example

            REGRESSION: partitions sequence cyclically into enchained parts by
            counts; does not return false 1-element part at end:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts(
                ...     [5],
                ...     cyclic=True,
                ...     enchain=True,
                ...     overhang=True,
                ...     )

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4])
                Sequence([4, 5, 6, 7, 8])
                Sequence([8, 9, 10, 11, 12])
                Sequence([12, 13, 14, 15])

        ..  container:: example

            Edge case: empty counts nests sequence and ignores keywords:

            ..  container:: example

                >>> sequence = evans.Sequence(range(16))
                >>> parts = sequence.partition_by_counts([])

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

        Returns nested sequence.
        """
        if not all(isinstance(_, int) and 0 <= _ for _ in counts):
            raise Exception(f"must be nonnegative integers: {counts!r}.")
        sequence = self
        if reversed_:
            sequence = type(self)(reversed(sequence))
        if counts:
            counts = abjad.cyclictuple.CyclicTuple(counts)
        else:
            return type(self)([sequence])
        result = []
        i, start = 0, 0
        while True:
            count = counts[i]
            stop = start + count
            part = sequence[start:stop]
            if len(sequence) < stop:
                if enchain and len(part) == 1:
                    part = None
                break
            result.append(part)
            start = stop
            i += 1
            if not cyclic and len(counts) <= i:
                part = sequence[start:]
                break
            if enchain:
                start -= 1
        if part:
            if overhang is True:
                result.append(part)
            elif overhang is abjad.enums.EXACT and len(part) == count:
                result.append(part)
            elif overhang is abjad.enums.EXACT and len(part) != count:
                raise Exception("sequence does not partition exactly.")
        if reversed_:
            result_ = []
            for part in reversed(result):
                part_type = type(part)
                part = reversed(part)
                part = part_type(part)
                result_.append(part)
            result = result_
        return type(self)(result)

    def partition_by_predicate(self, predicate):
        """
        Partitions sequence by predicate test function.

        ..  container:: example

            >>> seq = evans.Sequence([abjad.TimeSignature(_) for _ in [(4, 4), (3, 4), (1, 6), (4, 4), (1, 6), (1, 6), (5, 4), (3, 4)]])
            >>> def test_case(arg):
            ...     return arg.pair == abjad.Duration((1, 6)).pair
            ...
            >>> partitions = seq.partition_by_predicate(test_case)
            >>> print(partitions)
            Sequence([[TimeSignature(pair=(4, 4), hide=False, partial=None), TimeSignature(pair=(3, 4), hide=False, partial=None)], [TimeSignature(pair=(1, 6), hide=False, partial=None)], [TimeSignature(pair=(4, 4), hide=False, partial=None)], [TimeSignature(pair=(1, 6), hide=False, partial=None), TimeSignature(pair=(1, 6), hide=False, partial=None)], [TimeSignature(pair=(5, 4), hide=False, partial=None), TimeSignature(pair=(3, 4), hide=False, partial=None)]])

        """
        input_list = [_ for _ in self]
        previous_result = predicate(input_list[0])
        lengths = []
        count = 0
        for item in input_list:
            match = predicate(item) == previous_result
            if match is True:
                count += 1
            if match is False:
                lengths.append(count)
                count = 1
                previous_result = predicate(item)
        lengths.append(count)
        assert sum(lengths) == len(input_list)
        partitions = abjad.sequence.partition_by_counts(input_list, lengths)

        return type(self)(partitions)

    def partition_by_predicate_list(self, predicate_list):
        """
        Partitions sequence by ordered list of predicate test functions.

        ..  container:: example

            >>> seq = evans.Sequence([abjad.TimeSignature(_) for _ in [(4, 4), (3, 4), (1, 6), (4, 4), (1, 6), (1, 6), (5, 4), (3, 4)]])
            >>> def test_case_1(arg):
            ...     return arg.pair == abjad.Duration((1, 6)).pair
            ...
            >>> def test_case_2(arg):
            ...     return arg.pair < abjad.Duration((5, 4)).pair
            ...
            >>> partitions = seq.partition_by_predicate_list([test_case_1, test_case_2])
            >>> print(partitions)
            Sequence([[TimeSignature(pair=(4, 4), hide=False, partial=None), TimeSignature(pair=(3, 4), hide=False, partial=None)], [TimeSignature(pair=(1, 6), hide=False, partial=None)], [TimeSignature(pair=(4, 4), hide=False, partial=None)], [TimeSignature(pair=(1, 6), hide=False, partial=None), TimeSignature(pair=(1, 6), hide=False, partial=None)], [TimeSignature(pair=(5, 4), hide=False, partial=None)], [TimeSignature(pair=(3, 4), hide=False, partial=None)]])

        """
        input_list = [_ for _ in self]

        def recurse(input, predicates):
            out = []
            initial_partitions = type(self)(input).partition_by_predicate(predicates[0])
            if 1 < len(predicates):
                new_predicates = [_ for _ in predicates[1:]]
                for partition in initial_partitions:
                    if predicates[0](partition[0]):
                        out.append(partition)
                    else:
                        recursed_result = recurse(partition, new_predicates)
                        out.extend(recursed_result)
            else:
                for partition in initial_partitions:
                    out.append(partition)
            return out

        partitions = recurse(input_list, predicate_list)

        return type(self)(partitions)

    def partition_by_ratio_of_lengths(self, ratio) -> "Sequence":
        r"""
        Partitions sequence by ``ratio`` of lengths.

        ..  container:: example

            Partitions sequence by ``1:1:1`` ratio:

            ..  container:: example

                >>> numbers = evans.Sequence(range(10))
                >>> ratio = abjad.Ratio((1, 1, 1))

                >>> for part in numbers.partition_by_ratio_of_lengths(ratio):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5, 6])
                Sequence([7, 8, 9])

        ..  container:: example

            Partitions sequence by ``1:1:2`` ratio:

            ..  container:: example

                >>> numbers = evans.Sequence(range(10))
                >>> ratio = abjad.Ratio((1, 1, 2))

                >>> for part in numbers.partition_by_ratio_of_lengths(ratio):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4])
                Sequence([5, 6, 7, 8, 9])

        Returns nested sequence.
        """
        ratio = abjad.Ratio(ratio)
        length = len(self)
        counts = ratio.partition_integer(length)
        parts = self.partition_by_counts(
            counts, cyclic=False, overhang=abjad.enums.EXACT
        )
        return type(self)(parts)

    def partition_by_ratio_of_weights(self, weights) -> "Sequence":
        """
        Partitions sequence by ratio of ``weights``.

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1])
            >>> sequence = evans.Sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1])
            Sequence([1, 1, 1, 1])
            Sequence([1, 1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1, 1])
            >>> sequence = evans.Sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1])
            Sequence([1, 1])
            Sequence([1, 1, 1])
            Sequence([1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([2, 2, 3])
            >>> sequence = evans.Sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1])
            Sequence([1, 1, 1])
            Sequence([1, 1, 1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([3, 2, 2])
            >>> sequence = evans.Sequence(10 * [1])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1, 1])
            Sequence([1, 1, 1])
            Sequence([1, 1, 1])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1])
            >>> items = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
            >>> sequence = evans.Sequence(items)
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1, 1, 1, 1, 2, 2])
            Sequence([2, 2, 2, 2])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1])
            >>> items = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
            >>> sequence = evans.Sequence(items)
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([1, 1, 1, 1, 1, 1])
            Sequence([2, 2, 2])
            Sequence([2, 2, 2])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1])
            >>> sequence = evans.Sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([5])
            Sequence([])

        ..  container:: example

            >>> ratio = abjad.Ratio([1, 1, 1, 1])
            >>> sequence = evans.Sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([])
            Sequence([5])
            Sequence([])

        ..  container:: example

            >>> ratio = abjad.Ratio([2, 2, 3])
            >>> sequence = evans.Sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([5])
            Sequence([])

        ..  container:: example

            >>> ratio = abjad.Ratio([3, 2, 2])
            >>> sequence = evans.Sequence([5, 5])
            >>> sequence = sequence.partition_by_ratio_of_weights(ratio)
            >>> for item in sequence:
            ...     item
            ...
            Sequence([5])
            Sequence([5])
            Sequence([])

        Rounded weight-proportions of sequences returned equal to rounded
        ``weights``.

        Returns nested sequence.
        """
        list_weight = abjad.math.weight(self)
        weights_parts = abjad.Ratio(weights).partition_integer(list_weight)
        cumulative_weights = abjad.math.cumulative_sums(weights_parts, start=None)
        items = []
        sublist: typing.List[typing.Any] = []
        items.append(sublist)
        current_cumulative_weight = cumulative_weights.pop(0)
        for item in self:
            if not isinstance(item, (int, float, quicktions.Fraction)):
                raise TypeError(f"must be number: {item!r}.")
            sublist.append(item)
            while current_cumulative_weight <= abjad.math.weight(
                type(self)(items).flatten(depth=-1)
            ):
                try:
                    current_cumulative_weight = cumulative_weights.pop(0)
                    sublist = []
                    items.append(sublist)
                except IndexError:
                    break
        items_ = [type(self)(_) for _ in items]
        return type(self)(items_)

    def partition_by_weights(
        self,
        weights,
        # TODO: make keyword-only:
        cyclic=False,
        overhang=False,
        allow_part_weights=abjad.enums.EXACT,
    ) -> "Sequence":
        r"""
        Partitions sequence by ``weights`` exactly.

        >>> sequence = evans.Sequence([3, 3, 3, 3, 4, 4, 4, 4, 5])

        ..  container:: example

            Partitions sequence once by weights with overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [3, 9],
            ...     cyclic=False,
            ...     overhang=False,
            ...     ):
            ...     item
            ...
            Sequence([3])
            Sequence([3, 3, 3])

        ..  container:: example

            Partitions sequence once by weights. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [3, 9],
            ...     cyclic=False,
            ...     overhang=True,
            ...     ):
            ...     item
            ...
            Sequence([3])
            Sequence([3, 3, 3])
            Sequence([4, 4, 4, 4, 5])

        ..  container:: example

            Partitions sequence cyclically by weights:

            >>> for item in sequence.partition_by_weights(
            ...     [12],
            ...     cyclic=True,
            ...     overhang=False,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4, 4, 4])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [12],
            ...     cyclic=True,
            ...     overhang=True,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4, 4, 4])
            Sequence([4, 5])

        >>> sequence = evans.Sequence([3, 3, 3, 3, 4, 4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence once by weights. Allows part weights to be just
            less than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=False,
            ...     allow_part_weights=abjad.LESS,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])

        ..  container:: example

            Partitions sequence once by weights. Allows part weights to be just
            less than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=True,
            ...     allow_part_weights=abjad.LESS,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])
            Sequence([4, 4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just less than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 5],
            ...     cyclic=True,
            ...     overhang=False,
            ...     allow_part_weights=abjad.LESS,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])
            Sequence([4, 4])
            Sequence([4])
            Sequence([4, 5])
            Sequence([5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just less than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 5],
            ...     cyclic=True,
            ...     overhang=True,
            ...     allow_part_weights=abjad.LESS,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3])
            Sequence([3])
            Sequence([4, 4])
            Sequence([4])
            Sequence([4, 5])
            Sequence([5])

        >>> sequence = evans.Sequence([3, 3, 3, 3, 4, 4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence once by weights. Allow part weights to be just
            more than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=False,
            ...     allow_part_weights=abjad.MORE,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])

        ..  container:: example

            Partitions sequence once by weights. Allows part weights to be just
            more than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=False,
            ...     overhang=True,
            ...     allow_part_weights=abjad.MORE,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])
            Sequence([4, 4, 4, 5, 5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just more than specified:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=True,
            ...     overhang=False,
            ...     allow_part_weights=abjad.MORE,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])
            Sequence([4, 4, 4])
            Sequence([5])

        ..  container:: example

            Partitions sequence cyclically by weights. Allows part weights to
            be just more than specified. Allows overhang:

            >>> for item in sequence.partition_by_weights(
            ...     [10, 4],
            ...     cyclic=True,
            ...     overhang=True,
            ...     allow_part_weights=abjad.MORE,
            ...     ):
            ...     item
            ...
            Sequence([3, 3, 3, 3])
            Sequence([4])
            Sequence([4, 4, 4])
            Sequence([5])
            Sequence([5])

        Returns nested sequence.
        """
        if allow_part_weights is abjad.enums.EXACT:
            candidate = type(self)(self)
            candidate = candidate.split(weights, cyclic=cyclic, overhang=overhang)
            flattened_candidate = candidate.flatten(depth=-1)
            if flattened_candidate == self[: len(flattened_candidate)]:
                return candidate
            else:
                raise Exception("can not partition exactly.")
        elif allow_part_weights is abjad.enums.MORE:
            if not cyclic:
                return Sequence._partition_sequence_once_by_weights_at_least(
                    self, weights, overhang=overhang
                )
            else:
                return Sequence._partition_sequence_cyclically_by_weights_at_least(
                    self, weights, overhang=overhang
                )
        elif allow_part_weights is abjad.enums.LESS:
            if not cyclic:
                return Sequence._partition_sequence_once_by_weights_at_most(
                    self, weights, overhang=overhang
                )
            else:
                return Sequence._partition_sequence_cyclically_by_weights_at_most(
                    self, weights, overhang=overhang
                )
        else:
            message = "allow_part_weights must be ordinal constant: {!r}."
            message = message.format(allow_part_weights)
            raise ValueError(message)

    def permute(self, permutation) -> "Sequence":
        r"""
        Permutes sequence by ``permutation``.

        ..  container:: example

            >>> sequence = evans.Sequence([10, 11, 12, 13, 14, 15])
            >>> sequence.permute([5, 4, 0, 1, 2, 3])
            Sequence([15, 14, 10, 11, 12, 13])

        ..  container:: example

            >>> sequence = evans.Sequence([11, 12, 13, 14])
            >>> sequence.permute([1, 0, 3, 2])
            Sequence([12, 11, 14, 13])

        ..  container:: example

            Raises exception when lengths do not match:

            >>> sequence = evans.Sequence([1, 2, 3, 4, 5, 6])
            >>> sequence.permute([3, 0, 1, 2])
            Traceback (most recent call last):
                ...
            ValueError: permutation Sequence([3, 0, 1, 2]) must match length of Sequence([1, 2, 3, 4, 5, 6]).

        """
        permutation = type(self)(permutation)
        if not permutation.is_permutation():
            raise ValueError(f"must be permutation: {permutation!r}.")
        if len(permutation) != len(self):
            message = f"permutation {permutation!r} must match length of {self !r}."
            raise ValueError(message)
        result = []
        for i, item in enumerate(self):
            j = permutation[i]
            item_ = self[j]
            result.append(item_)
        return type(self)(result)

    # TODO: change input to pattern
    def remove(self, indices=None, period=None) -> "Sequence":
        """
        Removes items at ``indices``.

        ..  container:: example

            >>> sequence = evans.Sequence(range(15))

        ..  container:: example

            >>> sequence.remove()
            Sequence([])

        ..  container:: example

            >>> sequence.remove(indices=[2, 3])
            Sequence([0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        ..  container:: example

            Removes elements and indices -2 and -3:

            >>> sequence.remove(indices=[-2, -3])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14])

        ..  container:: example

            >>> sequence.remove(indices=[2, 3], period=4)
            Sequence([0, 1, 4, 5, 8, 9, 12, 13])

        ..  container:: example

            >>> sequence.remove(indices=[-2, -3], period=4)
            Sequence([2, 3, 6, 7, 10, 11, 14])

        ..  container:: example

            >>> sequence.remove(indices=[])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        ..  container:: example

            >>> sequence.remove(indices=[97, 98, 99])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        ..  container:: example

            Removes no elements:

            >>> sequence.remove(indices=[-97, -98, -99])
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])

        """
        items = []
        length = len(self)
        period = period or length
        if indices is None:
            indices = range(length)
        new_indices = []
        for i in indices:
            if length < abs(i):
                continue
            if i < 0:
                i = length + i
            i = i % period
            new_indices.append(i)
        indices = new_indices
        indices.sort()
        for i, item in enumerate(self):
            if i % period not in indices:
                items.append(item)
        return type(self)(items)

    def remove_duplications(self):
        """
        Removes repeats from ``sequence``.

        ..  container:: example

            >>> items = [31, 31, 35, 35, 31, 31, 31, 31, 35]
            >>> sequence = evans.Sequence(items)
            >>> sequence.remove_duplications()
            Sequence([31, 35])

        """
        seen = set()
        seen_add = seen.add
        return type(self)([x for x in self.items if not (x in seen or seen_add(x))])

    def remove_repeats(self) -> "Sequence":
        """
        Removes repeats from ``sequence``.

        ..  container:: example

            >>> items = [31, 31, 35, 35, 31, 31, 31, 31, 35]
            >>> sequence = evans.Sequence(items)
            >>> sequence.remove_repeats()
            Sequence([31, 35, 31, 35])

        """
        items = [self[0]]
        for item in self[1:]:
            if item != items[-1]:
                items.append(item)
        return type(self)(items)

    def repeat(self, n=1) -> "Sequence":
        r"""
        Repeats sequence.

        ..  container:: example

            ..  container:: example

                >>> evans.Sequence([1, 2, 3]).repeat(n=0)
                Sequence([])

        ..  container:: example

            ..  container:: example

                >>> evans.Sequence([1, 2, 3]).repeat(n=1)
                Sequence([Sequence([1, 2, 3])])

        ..  container:: example

            ..  container:: example

                >>> evans.Sequence([1, 2, 3]).repeat(n=2)
                Sequence([Sequence([1, 2, 3]), Sequence([1, 2, 3])])

        Returns nested sequence.
        """
        items = []
        for i in range(n):
            items.append(self[:])
        return type(self)(items)

    def repeat_to_length(self, length=None, start=0) -> "Sequence":
        """
        Repeats sequence to ``length``.

        ..  container:: example

            Repeats list to length 11:

            >>> evans.Sequence(range(5)).repeat_to_length(11)
            Sequence([0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0])

        ..  container:: example

            >>> evans.Sequence(range(5)).repeat_to_length(11, start=2)
            Sequence([2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2])

        ..  container:: example

            >>> sequence = evans.Sequence([0, -1, -2, -3, -4])
            >>> sequence.repeat_to_length(11)
            Sequence([0, -1, -2, -3, -4, 0, -1, -2, -3, -4, 0])

        ..  container:: example

            >>> sequence.repeat_to_length(0)
            Sequence([])

        ..  container:: example

            >>> evans.Sequence([1, 2, 3]).repeat_to_length(10, start=100)
            Sequence([2, 3, 1, 2, 3, 1, 2, 3, 1, 2])

        """
        assert abjad.math.is_nonnegative_integer(length), repr(length)
        assert len(self), repr(self)
        items = []
        start %= len(self)
        stop_index = start + length
        repetitions = int(math.ceil(float(stop_index) / len(self)))
        for i in range(repetitions):
            for item in self:
                items.append(item)
        return type(self)(items[start:stop_index])

    def repeat_to_weight(self, weight, allow_total=abjad.enums.EXACT) -> "Sequence":
        """
        Repeats sequence to ``weight``.

        ..  container:: example

            Repeats sequence to weight of 23 exactly:

            >>> evans.Sequence([5, -5, -5]).repeat_to_weight(23)
            Sequence([5, -5, -5, 5, -3])

        ..  container:: example

            Repeats sequence to weight of 23 more:

            >>> sequence = evans.Sequence([5, -5, -5])
            >>> sequence.repeat_to_weight(23, allow_total=abjad.MORE)
            Sequence([5, -5, -5, 5, -5])

        ..  container:: example

            Repeats sequence to weight of 23 or less:

            >>> sequence = evans.Sequence([5, -5, -5])
            >>> sequence.repeat_to_weight(23, allow_total=abjad.LESS)
            Sequence([5, -5, -5, 5])

        ..  container:: example

            >>> items = [abjad.NonreducedFraction(3, 16)]
            >>> sequence = evans.Sequence(items)
            >>> weight = abjad.NonreducedFraction(5, 4)
            >>> sequence = sequence.repeat_to_weight(weight)
            >>> sum(sequence)
            NonreducedFraction(20, 16)

            >>> [_.pair for _ in sequence]
            [(3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (2, 16)]

        """
        assert 0 <= weight
        if allow_total is abjad.enums.EXACT:
            sequence_weight = abjad.math.weight(self)
            complete_repetitions = int(
                math.ceil(float(weight) / float(sequence_weight))
            )
            items = list(self)
            items = complete_repetitions * items
            overage = complete_repetitions * sequence_weight - weight
            for item in reversed(items):
                if 0 < overage:
                    element_weight = abs(item)
                    candidate_overage = overage - element_weight
                    if 0 <= candidate_overage:
                        overage = candidate_overage
                        items.pop()
                    else:
                        absolute_amount_to_keep = element_weight - overage
                        assert 0 < absolute_amount_to_keep
                        signed_amount_to_keep = absolute_amount_to_keep
                        signed_amount_to_keep *= abjad.math.sign(item)
                        items.pop()
                        items.append(signed_amount_to_keep)
                        break
                else:
                    break
        elif allow_total is abjad.enums.LESS:
            items = [self[0]]
            i = 1
            while abjad.math.weight(items) < weight:
                items.append(self[i % len(self)])
                i += 1
            if weight < abjad.math.weight(items):
                items = items[:-1]
            return type(self)(items)
        elif allow_total is abjad.enums.MORE:
            items = [self[0]]
            i = 1
            while abjad.math.weight(items) < weight:
                items.append(self[i % len(self)])
                i += 1
            return type(self)(items)
        else:
            raise ValueError(f"is not an ordinal value constant: {allow_total!r}.")
        return type(self)(items=items)

    def replace(self, old, new) -> "Sequence":
        """
        Replaces ``old`` with ``new``.

        ..  container:: example

            >>> sequence = evans.Sequence([0, 2, 3, 0, 2, 3, 0, 2, 3])
            >>> sequence.replace(0, 1)
            Sequence([1, 2, 3, 1, 2, 3, 1, 2, 3])

        """
        items = []
        for item in self:
            if item == old:
                new_copy = copy.copy(new)
                items.append(new_copy)
            else:
                items.append(item)
        return type(self)(items=items)

    def replace_at(self, indices, new_material) -> "Sequence":
        """
        Replaces items at ``indices`` with ``new_material``.

        ..  container:: example

            Replaces items at indices 0, 2, 4, 6:

            >>> sequence = evans.Sequence(range(16))
            >>> sequence.replace_at(
            ...     ([0], 2),
            ...     (['A', 'B', 'C', 'D'], None),
            ...     )
            Sequence(['A', 1, 'B', 3, 'C', 5, 'D', 7, 8, 9, 10, 11, 12, 13, 14, 15])

        ..  container:: example

            Replaces elements at indices 0, 1, 8, 13:

            >>> sequence = evans.Sequence(range(16))
            >>> sequence.replace_at(
            ...     ([0, 1, 8, 13], None),
            ...     (['A', 'B', 'C', 'D'], None),
            ...     )
            Sequence(['A', 'B', 2, 3, 4, 5, 6, 7, 'C', 9, 10, 11, 12, 'D', 14, 15])

        ..  container:: example

            Replaces every item at even index:

            >>> sequence = evans.Sequence(range(16))
            >>> sequence.replace_at(
            ...     ([0], 2),
            ...     (['*'], 1),
            ...     )
            Sequence(['*', 1, '*', 3, '*', 5, '*', 7, '*', 9, '*', 11, '*', 13, '*', 15])

        ..  container:: example

            Replaces every element at an index congruent to 0 (mod 6) with
            ``'A'``; replaces every element at an index congruent to 2 (mod 6)
            with ``'B'``:

            >>> sequence = evans.Sequence(range(16))
            >>> sequence.replace_at(
            ...     ([0], 2),
            ...     (['A', 'B'], 3),
            ...     )
            Sequence(['A', 1, 'B', 3, 4, 5, 'A', 7, 'B', 9, 10, 11, 'A', 13, 'B', 15])

        """
        assert isinstance(indices, collections.abc.Sequence)
        assert len(indices) == 2
        index_values, index_period = indices
        assert isinstance(index_values, collections.abc.Sequence)
        index_values = list(index_values)
        assert isinstance(index_period, (int, type(None)))
        assert isinstance(new_material, collections.abc.Sequence)
        assert len(new_material) == 2
        material_values, material_period = new_material
        assert isinstance(material_values, collections.abc.Sequence)
        material_values = list(material_values)
        assert isinstance(material_period, (int, type(None)))
        maxsize = sys.maxsize
        if index_period is None:
            index_period = maxsize
        if material_period is None:
            material_period = maxsize
        items = []
        material_index = 0
        for index, item in enumerate(self):
            if index % index_period in index_values:
                try:
                    cyclic_material_index = material_index % material_period
                    material_value = material_values[cyclic_material_index]
                    items.append(material_value)
                except IndexError:
                    items.append(item)
                material_index += 1
            else:
                items.append(item)
        return type(self)(items=items)

    # TODO: remove in favor of self.retain_pattern()
    def retain(self, indices=None, period=None) -> "Sequence":
        """
        Retains items at ``indices``.

        ..  container:: example

            >>> sequence = evans.Sequence(range(10))
            >>> sequence.retain()
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        ..  container:: example

            >>> sequence.retain(indices=[2, 3])
            Sequence([2, 3])

        ..  container:: example

            >>> sequence.retain(indices=[-2, -3])
            Sequence([7, 8])

        ..  container:: example

            >>> sequence.retain(indices=[2, 3], period=4)
            Sequence([2, 3, 6, 7])

        ..  container:: example

            >>> sequence.retain(indices=[-2, -3], period=4)
            Sequence([0, 3, 4, 7, 8])

        ..  container:: example

            >>> sequence.retain(indices=[])
            Sequence([])

        ..  container:: example

            >>> sequence.retain(indices=[97, 98, 99])
            Sequence([])

        ..  container:: example

            >>> sequence.retain(indices=[-97, -98, -99])
            Sequence([])

        """
        length = len(self)
        period = period or length
        if indices is None:
            indices = range(length)
        new_indices = []
        for i in indices:
            if length < abs(i):
                continue
            if i < 0:
                i = length + i
            i = i % period
            new_indices.append(i)
        indices = new_indices
        indices.sort()
        items = []
        for i, item in enumerate(self):
            if i % period in indices:
                items.append(item)
        return type(self)(items=items)

    def retain_pattern(self, pattern) -> "Sequence":
        """
        Retains items at indices matching ``pattern``.

        ..  container:: example

            >>> sequence = evans.Sequence(range(10))
            >>> sequence.retain_pattern(abjad.index_all())
            Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([2, 3]))
            Sequence([2, 3])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([-2, -3]))
            Sequence([7, 8])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([2, 3], 4))
            Sequence([2, 3, 6, 7])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([-2, -3], 4))
            Sequence([0, 3, 4, 7, 8])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([97, 98, 99]))
            Sequence([])

        ..  container:: example

            >>> sequence.retain_pattern(abjad.index([-97, -98, -99]))
            Sequence([])

        """
        length = len(self)
        items = []
        for i, item in enumerate(self):
            if pattern.matches_index(i, length):
                items.append(item)
        return type(self)(items=items)

    def reverse(self, recurse=False) -> "Sequence":
        r"""
        Reverses sequence.

        ..  container:: example

            Reverses sequence:

            ..  container:: example

                >>> sequence = evans.Sequence([[1, 2], 3, [4, 5]])

                >>> sequence.reverse()
                Sequence([[4, 5], 3, [1, 2]])

        ..  container:: example

            Reverses recursively:

            ..  container:: example

                >>> segment_1 = abjad.PitchClassSegment([1, 2])
                >>> pitch = abjad.NumberedPitch(3)
                >>> segment_2 = abjad.PitchClassSegment([4, 5])
                >>> sequence = evans.Sequence([segment_1, pitch, segment_2])

                >>> for item in sequence.reverse(recurse=True):
                ...     item
                ...
                PitchClassSegment([5, 4])
                NumberedPitch(3)
                PitchClassSegment([2, 1])

        """
        if not recurse:
            return type(self)(items=reversed(self))

        def _reverse_helper(item):
            if isinstance(item, collections.abc.Iterable):
                subitems_ = [_reverse_helper(_) for _ in reversed(item)]
                return type(item)(subitems_)
            else:
                return item

        items = _reverse_helper(self.items)
        return type(self)(items=items)

    #
    # def rotate(self, n=0) -> "Sequence":
    #     r"""
    #     Rotates sequence by index ``n``.
    #
    #     ..  container:: example
    #
    #         Rotates sequence to the right:
    #
    #         ..  container:: example
    #
    #             >>> sequence = evans.Sequence(range(10))
    #
    #             >>> sequence.rotate(n=4)
    #             Sequence([6, 7, 8, 9, 0, 1, 2, 3, 4, 5])
    #
    #     ..  container:: example
    #
    #         Rotates sequence to the left:
    #
    #         ..  container:: example
    #
    #             >>> sequence = evans.Sequence(range(10))
    #
    #             >>> sequence.rotate(n=-3)
    #             Sequence([3, 4, 5, 6, 7, 8, 9, 0, 1, 2])
    #
    #     ..  container:: example
    #
    #         Rotates sequence neither to the right nor the left:
    #
    #         ..  container:: example
    #
    #             >>> sequence = evans.Sequence(range(10))
    #
    #             >>> sequence.rotate(n=0)
    #             Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    #
    #     """
    #     n = n or 0
    #     items = []
    #     if len(self):
    #         n = n % len(self)
    #         for item in self[-n : len(self)] + self[:-n]:
    #             items.append(item)
    #     return type(self)(items=items)

    def sort(self, key=None, reverse=False) -> "Sequence":
        """
        Sorts sequence.

        ..  container:: example

            >>> sequence = evans.Sequence([3, 2, 5, 4, 1, 6])
            >>> sequence.sort()
            Sequence([1, 2, 3, 4, 5, 6])

            >>> sequence
            Sequence([3, 2, 5, 4, 1, 6])

        """
        items = list(self)
        items.sort(key=key, reverse=reverse)
        return type(self)(items=items)

    def split(self, weights, cyclic=False, overhang=False) -> "Sequence":
        r"""
        Splits sequence by ``weights``.

        ..  container:: example

            Splits sequence cyclically by weights with overhang:

            ..  container:: example

                >>> sequence = evans.Sequence([10, -10, 10, -10])

                >>> for part in sequence.split(
                ...     (3, 15, 3),
                ...     cyclic=True,
                ...     overhang=True,
                ...     ):
                ...     part
                ...
                Sequence([3])
                Sequence([7, -8])
                Sequence([-2, 1])
                Sequence([3])
                Sequence([6, -9])
                Sequence([-1])

        ..  container:: example

            Splits sequence once by weights with overhang:

            >>> for part in sequence.split(
            ...     (3, 15, 3),
            ...     cyclic=False,
            ...     overhang=True,
            ...     ):
            ...     part
            ...
            Sequence([3])
            Sequence([7, -8])
            Sequence([-2, 1])
            Sequence([9, -10])

        ..  container:: example

            Splits sequence once by weights without overhang:

            >>> for part in sequence.split(
            ...     (3, 15, 3),
            ...     cyclic=False,
            ...     overhang=False,
            ...     ):
            ...     part
            ...
            Sequence([3])
            Sequence([7, -8])
            Sequence([-2, 1])

        ..  container:: example

            REGRESSION. Splits sequence of nonreduced fractions cyclically by
            weights with overhang:

            ..  container:: example

                >>> sequence = evans.Sequence([
                ...     abjad.NonreducedFraction(20, 2),
                ...     abjad.NonreducedFraction(-20, 2),
                ...     abjad.NonreducedFraction(20, 2),
                ...     abjad.NonreducedFraction(-20, 2),
                ... ])

                >>> for part in sequence.split(
                ...     (3, 15, 3),
                ...     cyclic=True,
                ...     overhang=True,
                ...     ):
                ...     part
                ...
                Sequence([NonreducedFraction(6, 2)])
                Sequence([NonreducedFraction(14, 2), NonreducedFraction(-16, 2)])
                Sequence([NonreducedFraction(-4, 2), NonreducedFraction(2, 2)])
                Sequence([NonreducedFraction(6, 2)])
                Sequence([NonreducedFraction(12, 2), NonreducedFraction(-18, 2)])
                Sequence([NonreducedFraction(-2, 2)])

        """
        result = []
        current_index = 0
        current_piece: typing.List[typing.Any] = []
        if cyclic:
            weights = Sequence(weights).repeat_to_weight(
                abjad.math.weight(self), allow_total=abjad.enums.LESS
            )
        for weight in weights:
            current_piece_weight = abjad.math.weight(current_piece)
            while current_piece_weight < weight:
                current_piece.append(self[current_index])
                current_index += 1
                current_piece_weight = abjad.math.weight(current_piece)
            if current_piece_weight == weight:
                current_piece_ = type(self)(current_piece)
                result.append(current_piece_)
                current_piece = []
            elif weight < current_piece_weight:
                overage = current_piece_weight - weight
                current_last_element = current_piece.pop(-1)
                needed = abs(current_last_element) - overage
                needed *= abjad.math.sign(current_last_element)
                current_piece.append(needed)
                current_piece_ = type(self)(current_piece)
                result.append(current_piece_)
                overage *= abjad.math.sign(current_last_element)
                current_piece = [overage]
        if overhang:
            last_piece = current_piece
            last_piece.extend(self[current_index:])
            if last_piece:
                last_piece_ = type(self)(last_piece)
                result.append(last_piece_)
        return type(self)(items=result)

    def sum(self) -> typing.Any:
        r"""
        Sums sequence.

        ..  container:: example

            Sums sequence of positive numbers:

            ..  container:: example

                >>> sequence = evans.Sequence([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

                >>> sequence.sum()
                55

        ..  container:: example

            Sum sequence of numbers with mixed signs:

            ..  container:: example

                >>> sequence = evans.Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])

                >>> sequence.sum()
                5

        ..  container:: example

            Sums sequence and wraps result in new sequence:

            ..  container:: example

                >>> sequence = evans.Sequence(range(1, 10+1))
                >>> result = sequence.sum()
                >>> sequence = evans.Sequence(result)

                >>> sequence
                Sequence([55])

        """
        if len(self) == 0:
            return 0
        result = self[0]
        for item in self[1:]:
            result += item
        return result

    def sum_by_sign(self, sign=(-1, 0, 1)) -> "Sequence":
        """
        Sums consecutive sequence items by ``sign``.

        >>> items = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]
        >>> sequence = evans.Sequence(items)

        ..  container:: example

            >>> sequence.sum_by_sign()
            Sequence([0, -2, 5, -5, 8, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1])
            Sequence([0, 0, -2, 2, 3, -5, 1, 2, 5, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[0])
            Sequence([0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[1])
            Sequence([0, 0, -1, -1, 5, -5, 8, -5, -6])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1, 0])
            Sequence([0, -2, 2, 3, -5, 1, 2, 5, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1, 1])
            Sequence([0, 0, -2, 5, -5, 8, -11])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[0, 1])
            Sequence([0, -1, -1, 5, -5, 8, -5, -6])

        ..  container:: example

            >>> sequence.sum_by_sign(sign=[-1, 0, 1])
            Sequence([0, -2, 5, -5, 8, -11])

        Sumsn consecutive negative elements when ``-1`` in ``sign``.

        Sums consecutive zero-valued elements when ``0`` in ``sign``.

        Sums consecutive positive elements when ``1`` in ``sign``.
        """
        items = []
        generator = itertools.groupby(self, abjad.math.sign)
        for current_sign, group in generator:
            if current_sign in sign:
                items.append(sum(group))
            else:
                for item in group:
                    items.append(item)
        return type(self)(items=items)

    def truncate(self, sum_=None, weight=None) -> "Sequence":
        """
        Truncates sequence.

        >>> sequence = evans.Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])

        ..  container:: example

            Truncates sequence to weights ranging from 1 to 10:

            >>> for weight in range(1, 11):
            ...     result = sequence.truncate(weight=weight)
            ...     print(weight, result)
            ...
            1 Sequence([-1])
            2 Sequence([-1, 1])
            3 Sequence([-1, 2])
            4 Sequence([-1, 2, -1])
            5 Sequence([-1, 2, -2])
            6 Sequence([-1, 2, -3])
            7 Sequence([-1, 2, -3, 1])
            8 Sequence([-1, 2, -3, 2])
            9 Sequence([-1, 2, -3, 3])
            10 Sequence([-1, 2, -3, 4])

        ..  container:: example

            Truncates sequence to sums ranging from 1 to 10:

            >>> for sum_ in range(1, 11):
            ...     result = sequence.truncate(sum_=sum_)
            ...     print(sum_, result)
            ...
            1 Sequence([-1, 2])
            2 Sequence([-1, 2, -3, 4])
            3 Sequence([-1, 2, -3, 4, -5, 6])
            4 Sequence([-1, 2, -3, 4, -5, 6, -7, 8])
            5 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            6 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            7 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            8 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            9 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            10 Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])

        ..  container:: example

            Truncates sequence to zero weight:

            >>> sequence.truncate(weight=0)
            Sequence([])

        ..  container:: example

            Truncates sequence to zero sum:

            >>> sequence.truncate(sum_=0)
            Sequence([])

        Ignores ``sum`` when ``weight`` and ``sum`` are both set.

        Raises value error on negative ``sum``.
        """
        if weight is not None:
            assert 0 <= weight, repr(weight)
            items = []
            if 0 < weight:
                total = 0
                for item in self:
                    total += abs(item)
                    if total < weight:
                        items.append(item)
                    else:
                        sign = abjad.math.sign(item)
                        trimmed_part = weight - abjad.math.weight(items)
                        trimmed_part *= sign
                        items.append(trimmed_part)
                        break
        elif sum_ is not None:
            assert 0 <= sum_, repr(sum_)
            items = []
            if 0 < sum_:
                total = 0
                for item in self:
                    total += item
                    if total < sum_:
                        items.append(item)
                    else:
                        items.append(sum_ - sum(items))
                        break
        return type(self)(items=items)

    def weight(self) -> typing.Any:
        """
        Gets weight.

        ..  container:: example

            >>> evans.Sequence([]).weight()
            0

            >>> evans.Sequence([1]).weight()
            1

            >>> evans.Sequence([1, 2, 3]).weight()
            6

            >>> evans.Sequence([1, 2, -3]).weight()
            6

            >>> evans.Sequence([-1, -2, -3]).weight()
            6

            >>> sequence = evans.Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
            >>> sequence.weight()
            55

        ..  container:: example

            >>> evans.Sequence([[1, -7, -7], [1, -8 -8]]).weight()
            32

        """
        weights = []
        for item in self:
            if hasattr(item, "weight"):
                weights.append(item.weight())
            elif isinstance(item, collections.abc.Iterable):
                item = Sequence(item)
                weights.append(item.weight())
            else:
                weights.append(abs(item))
        return sum(weights)

    def zip(self, cyclic=False, truncate=True) -> "Sequence":
        """
        Zips sequences in sequence.

        ..  container:: example

            Zips cyclically:

            >>> sequence = evans.Sequence([[1, 2, 3], ['a', 'b']])
            >>> for item in sequence.zip(cyclic=True):
            ...     item
            ...
            Sequence([1, 'a'])
            Sequence([2, 'b'])
            Sequence([3, 'a'])

            >>> items = [[10, 11, 12], [20, 21], [30, 31, 32, 33]]
            >>> sequence = evans.Sequence(items)
            >>> for item in sequence.zip(cyclic=True):
            ...     item
            ...
            Sequence([10, 20, 30])
            Sequence([11, 21, 31])
            Sequence([12, 20, 32])
            Sequence([10, 21, 33])

        ..  container:: example

            Zips without truncation:

            >>> items = [[1, 2, 3, 4], [11, 12, 13], [21, 22, 23]]
            >>> sequence = evans.Sequence(items)
            >>> for item in sequence.zip(truncate=False):
            ...     item
            ...
            Sequence([1, 11, 21])
            Sequence([2, 12, 22])
            Sequence([3, 13, 23])
            Sequence([4])

        ..  container:: example

            Zips strictly:

            >>> items = [[1, 2, 3, 4], [11, 12, 13], [21, 22, 23]]
            >>> for item in evans.Sequence(items).zip():
            ...     item
            ...
            Sequence([1, 11, 21])
            Sequence([2, 12, 22])
            Sequence([3, 13, 23])

        Returns nested sequence.
        """
        for item in self:
            if not isinstance(item, collections.abc.Iterable):
                raise Exception(f"must by iterable: {item!r}.")
        items: typing.List[typing.Any] = []
        if cyclic:
            if not min(len(_) for _ in self):
                return type(self)(items=items)
            maximum_length = max([len(_) for _ in self])
            for i in range(maximum_length):
                part = []
                for item in self:
                    index = i % len(item)
                    element = item[index]
                    part.append(element)
                part_ = type(self)(items=part)
                items.append(part_)
        elif not truncate:
            maximum_length = max([len(_) for _ in self])
            for i in range(maximum_length):
                part = []
                for item in self:
                    try:
                        part.append(item[i])
                    except IndexError:
                        pass
                part_ = type(self)(items=part)
                items.append(part_)
        elif truncate:
            for item in zip(*self):
                item = type(self)(items=item)
                items.append(item)
        return type(self)(items=items)

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

    def cartesian_product(self, product_sequence):
        """

        .. container:: example

            >>> import quicktions
            >>> l = [2, 3, 4]
            >>> l = [quicktions.Fraction(_) for _ in l]
            >>> evans.Sequence(l).combination_addition(2)
            Sequence([Fraction(5, 4), Fraction(3, 2), Fraction(7, 4)])

        """
        if isinstance(product_sequence[0], list):
            product_generator = itertools.product(self.items, *product_sequence)
        else:
            product_generator = itertools.product(self.items, product_sequence)
        out = [_ for _ in product_generator]
        return type(self)(out)

    def cartesian_product_products(self, product_sequence):
        """

        .. container:: example

            >>> import quicktions
            >>> l = [2, 3, 4]
            >>> l = [quicktions.Fraction(_) for _ in l]
            >>> evans.Sequence(l).combination_addition(2)
            Sequence([Fraction(5, 4), Fraction(3, 2), Fraction(7, 4)])

        """
        products = self.cartesian_product(product_sequence)
        out = [Sequence(_).product()[0] for _ in products]
        return type(self)(out)

    def cartesian_product_sums(self, product_sequence):
        """

        .. container:: example

            >>> import quicktions
            >>> l = [2, 3, 4]
            >>> l = [quicktions.Fraction(_) for _ in l]
            >>> evans.Sequence(l).combination_addition(2)
            Sequence([Fraction(5, 4), Fraction(3, 2), Fraction(7, 4)])

        """
        products = self.cartesian_product(product_sequence)
        out = [sum(_) for _ in products]
        return type(self)(out)

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

    def convolve_1D(self, kernel=[0.25, 0.5, 0.25], mode="valid"):
        # modes can be full, valid, or same
        convolution = numpy.convolve(self.items, kernel, mode=mode)
        out = [_ for _ in convolution]
        return type(self)(out)

    def convolve_2D(
        self,
        kernel=[[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]],
        mode="nearest",
    ):
        # modes can be reflect, constant, nearest, mirror, or wrap
        convolution = convolve(self.items, kernel, mode=mode)
        out = [[y for y in x] for x in convolution]
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

    def derive_intervals(self, intervals, cyclic=True, match_longest=False):
        out = []
        if match_longest is True:
            if len(self.items) < len(intervals):
                cyc_items = CyclicList(self.items, forget=False)
                items = cyc_items(r=len(intervals))
            else:
                items = self.items
        if cyclic is True:
            cyc_intervals = CyclicList(intervals, forget=False)
            intervals = cyc_intervals(r=len(items))
        for base, interval in zip(items, intervals):
            if interval is not None:
                temp = [base, base + interval]
                out.append(temp)
            else:
                out.append(base)
        return type(self)(out)

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

    def durations_from_vector(self):
        vector = [_ for _ in self]
        first_onset = 0
        for val in vector:
            if val != 1:
                first_onset += 1
            else:
                break
        rotated_vector = abjad.sequence.rotate(vector, 0 - first_onset)
        counter = 1
        durations = []
        for i, pair in enumerate(abjad.sequence.nwise(rotated_vector, 2)):
            if 0 < i:
                if pair[0] == 1:
                    durations.append(counter)
                    counter = 1
                elif pair[0] == 0:
                    counter += 1
        counter += 1
        durations.append(counter)
        return type(self)(durations)

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
            step_size = step**degree
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
            if hasattr(index, "__iter__"):
                val = list(type(self)(items_list).map_indices(index).items)
            else:
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

    def mod(self, modulus, indices=False, preserve_negatives=False):
        """

        .. container:: example

            >>> evans.Sequence([7, 8, 9, 10]).mod(7)
            Sequence([7, 1, 2, 3])

        .. container:: example

            >>> evans.Sequence([7, 8, 9, 10]).mod(7, indices=True)
            Sequence([0, 1, 2, 3])

        """
        if preserve_negatives is False:
            new_seq = [_ % modulus for _ in self]
        else:
            new_seq = [0 - (_ % modulus) if _ < 0 else _ % modulus for _ in self]
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

    def permutational_parsimony(self, cycles, debug=False, accumulate=False):

        # def make_h_cycle(i):
        #     out = []
        #     for _ in range(12):
        #         out.append((_, (((7 * _) + i) % 12)))
        #     return out

        # tritone (0, 6)
        # aug 5 (0, 4, 8)
        # dim 7 (0, 3, 6, 9)
        # alt 7 (0, 2, 6, 8)
        # double fifths (0, 1, 6, 7)
        # mode 1 (0, 2, 4, 6, 8, 10)
        # mode 2 (0, 1, 3, 4, 6, 7, 9, 10)
        # mode 3 (0, 1, 2, 4, 5, 6, 8, 9, 10)
        # mode 4 (0, 1, 2, 3, 6, 7, 8, 9)
        # mode 5 (0, 1, 2, 6, 7, 8)
        # mode 6 (0, 1, 2, 4, 6, 7, 8, 10)
        # mode 7 (0, 1, 2, 3, 4, 6, 7, 8, 9, 10)
        # mode A (0, 1, 4, 5, 8, 9)
        # mode B (0, 1, 3, 6, 7, 9)
        # mode C (0, 1, 4, 6, 7, 10)
        # chromatic scale (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)

        predefined_cycles = {
            "p": [(0, 7), (1, 6), (2, 5), (3, 4), (8, 11), (9, 10)],
            "r": [(0, 4), (1, 3), (5, 11), (6, 10), (7, 9)],
            "l": [(0, 11), (1, 10), (2, 9), (3, 8), (4, 7), (5, 6)],
            "h1": [(0, 1, 8, 9, 4, 5), (2, 3, 10, 11, 6, 7)],  # 7x + 1
            "h2": [(0, 4, 8), (1, 11, 9, 7, 5, 3), (2, 6, 10)],  # 7x + 4
            "h3": [(0, 7, 8, 3, 4, 11), (1, 2, 9, 10, 5, 6)],  # 7x + 7
            "h4": [(0, 10, 8, 6, 4, 2), (1, 5, 9), (3, 7, 11)],  # 7x + 10
            "messiaen a": [(0, 1, 6, 7), (2, 11, 8, 5), (3, 4, 9, 10)],
            "messiaen b": [(0, 3, 6, 9), (1, 8, 7, 2), (4, 11, 10, 5)],
            "feu a": [(0, 6, 9, 1, 5, 3, 4, 8, 10, 11), (2, 7)],
            "feu b": [(0, 5, 8, 1, 6, 2, 4, 3, 7, 9, 10)],
            "morris M5": [(1, 5), (2, 10), (4, 8), (7, 11)],  # x * 5 % 12
            "morris M7": [(1, 7), (3, 9), (5, 11)],  # x * 7 % 12
            "morris I": [(1, 11), (2, 10), (3, 9), (4, 8), (5, 7)],
            "morris T1": [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)],
            "morris alpha": [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11)],
            "morris beta": [(0, 2), (1, 3), (4, 6), (5, 7), (8, 10), (9, 11)],
            "morris gamma": [(0, 3), (1, 4), (2, 5), (6, 9), (7, 10), (8, 11)],
            "morris delta": [(4, 8), (5, 9), (6, 10), (7, 11)],
            "knot 14": [(0, 1), (2, 3), (4, 6), (5, 8), (7, 10), (9, 11)],
            "knot 19": [(0, 1), (2, 3), (4, 6), (5, 9), (7, 11), (8, 10)],
            "knot 20": [(0, 1), (2, 3), (4, 6), (5, 10), (7, 9), (8, 11)],
            "knot 33": [(0, 1), (2, 3), (4, 7), (5, 9), (6, 11), (8, 10)],
            "knot 34": [(0, 1), (2, 3), (4, 7), (5, 10), (6, 9), (8, 11)],
            "knot 35": [(0, 1), (2, 3), (4, 7), (5, 11), (6, 9), (8, 10)],
            "knot 38": [(0, 1), (2, 3), (4, 9), (5, 7), (6, 11), (8, 10)],
            "knot 39": [(0, 1), (2, 3), (4, 11), (5, 7), (6, 9), (8, 10)],
            # TODO: add more knots from all-interval sets in book
            # xenakis nomos alpha cube
            "cube a-90": [(1, 2, 3, 4), (5, 6, 7, 8)],  # limit 1-8
            "cube a-180": [(1, 3), (2, 4), (5, 7), (6, 8)],
            "cube a-270": [(2, 1, 4, 3), (6, 5, 8, 7)],
            "cube b-90": [(1, 4, 8, 5), (2, 3, 7, 6)],
            "cube b-180": [(1, 8), (4, 5), (2, 7), (3, 6)],
            "cube b-270": [(4, 1, 5, 8), (3, 2, 6, 7)],
            "cube c-90": [(1, 5, 6, 2), (4, 8, 7, 3)],
            "cube c-180": [(1, 6), (5, 2), (4, 7), (8, 3)],
            "cube c-270": [(5, 1, 2, 6), (8, 4, 3, 7)],
            "cube 4a": [(2, 5, 4), (3, 6, 8)],
            "cube 4b": [(5, 2, 4), (6, 3, 8)],
            "cube 5a": [(1, 6, 8), (2, 7, 4)],
            "cube 5b": [(6, 1, 8), (7, 2, 4)],
            "cube 6a": [(1, 6, 3), (4, 5, 7)],
            "cube 6b": [(6, 1, 3), (5, 4, 7)],
            "cube 7a": [(1, 8, 3), (2, 5, 7)],
            "cube 7b": [(8, 1, 3), (5, 2, 7)],
            "cube 8": [(2, 4), (6, 8)],  # reflection
            "cube 9": [(1, 3), (5, 7)],  # reflection
            "cube 10": [(1, 2), (3, 4), (5, 6), (7, 8)],  # reflection
            "cube 11": [(1, 4), (2, 3), (5, 8), (6, 7)],  # reflection
            # alternative cube names (without identity): https://www.euclideanspace.com/maths/discrete/groups/categorise/finite/cube/index.htm
            "cube x": [(1, 4, 8, 5), (2, 3, 7, 6)],
            "cube y": [(1, 5, 6, 2), (4, 8, 7, 3)],
            "cube xx": [(8, 1), (7, 2), (6, 3), (5, 4)],
            "cube xy": [(8, 6, 1), (4, 7, 2)],
            "cube yx": [(4, 5, 2), (8, 6, 3)],
            "cube yy": [(6, 1), (5, 2), (8, 3), (7, 4)],
            "cube xxx": [(5, 8, 4, 1), (6, 7, 3, 2)],
            "cube xxy": [(7, 1), (3, 2), (6, 4), (8, 5)],
            "cube xyx": [(5, 1), (8, 2), (7, 3), (6, 4)],
            "cube xyy": [(7, 1), (8, 2), (4, 3), (6, 5)],
            "cube yxx": [(4, 1), (8, 2), (5, 3), (7, 6)],
            "cube yyx": [(2, 1), (5, 3), (6, 4), (8, 7)],
            "cube yyy": [(2, 6, 5, 1), (7, 8, 4, 3)],
            "cube xxxy": [(6, 3, 1), (5, 7, 4)],
            "cube xxyx": [(6, 8, 1), (7, 4, 2)],
            "cube xxyy": [(3, 1), (4, 2), (7, 5), (8, 6)],
            "cube xyxx": [(5, 4, 2), (6, 8, 3)],
            "cube xyyy": [(3, 8, 1), (7, 5, 2)],
            "cube yxxx": [(8, 3, 1), (5, 7, 2)],
            "cube yyyx": [(3, 6, 1), (7, 5, 4)],
            "cube xxxyx": [(2, 3, 4, 1), (6, 7, 8, 5)],
            "cube xyxxx": [(4, 3, 2, 1), (8, 7, 6, 5)],
            "cube xyyyx": [(7, 1), (6, 2), (5, 3), (8, 4)],
            # extension of cube octahedral group to vertices of octahedron
            "octahedron 1a": [(3, 2, 5, 4)],  # limit 1-6
            "octahedron 1b": [(2, 3, 4, 5)],
            "octahedron 2a": [(1, 5, 6, 3)],
            "octahedron 2b": [(5, 1, 3, 6)],
            "octahedron 3a": [(1, 5, 2), (3, 4, 6)],
            "octahedron 3b": [(5, 1, 2), (4, 3, 6)],
            "octahedron 4a": [(1, 4, 3), (2, 5, 6)],
            "octahedron 4b": [(4, 1, 3), (5, 2, 6)],
            "octahedron 5a": [(1, 5, 4), (2, 6, 3)],
            "octahedron 5b": [(5, 1, 4), (6, 2, 3)],
            "octahedron 6a": [(1, 2, 3), (4, 5, 6)],
            "octahedron 6b": [(2, 1, 3), (5, 4, 6)],
        }
        if accumulate is False:
            if isinstance(cycles, str):
                cycles = predefined_cycles[cycles]

            verbose_cycles = []
            for cycle in cycles:
                adjacent_pairs = []
                for i, num in enumerate(cycle):
                    if num != cycle[-1]:
                        pair = (num, cycle[i + 1])
                    else:
                        pair = (num, cycle[0])
                    adjacent_pairs.append(pair)
                if debug is True:
                    print(f"adjacent pairs: {adjacent_pairs}")
                verbose_cycles.append(adjacent_pairs)
            if debug is True:
                print(f"verbose cycles: {verbose_cycles}")

            new_items = []

            for item in self.items:
                treated = False
                reduced_item = item % 12
                if debug is True:
                    print(f"reduced item: {reduced_item}")
                for verbose_cycle in verbose_cycles:
                    for pair in verbose_cycle:
                        if reduced_item == pair[0]:
                            if debug is True:
                                print(f"chosen cycle: {verbose_cycle}")
                                print(f"chosen pair: {pair}")
                            distance = pair[1] - pair[0]
                            if debug is True:
                                print(f"distance: {distance}")
                            new_value = item + distance
                            if debug is True:
                                print(f"new value: {new_value}\n")
                            new_items.append(new_value)
                            treated = True
                if treated is False:
                    new_items.append(item)
            return type(self)(new_items)
        else:
            out = [self.items]
            for cycle in cycles:
                out.append(type(self)(out[-1]).permutational_parsimony(cycle).items)
            return type(self)(out)

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
            x = (n + 1) * (3 * n**2 + 3 * n + 1)
            seq.append(x)
        return type(self)(seq)

    def random_sequence(self, total_length=1, random_seed=1, weights=None):
        out = []
        choices = list(self.items)
        random.seed(random_seed)
        if weights is None:
            for _ in range(total_length):
                out.append(random.choice(choices))
        else:
            out = random.choices(choices, weights=weights, k=total_length)
        return type(self)(out)

    def random_funnel(self, destination, random_ranges, random_seed=1):
        random.seed(random_seed)

        def are_sequences_matched(sequence, target):
            boolean_sequence = []
            for i, val in enumerate(sequence):
                if val == target[i]:
                    boolean_sequence.append(True)
                else:
                    boolean_sequence.append(False)
            return all(boolean_sequence)

        arrived_at_destination = False
        compiled_ranges = []
        for range_ in random_ranges:
            sub_list = [_ for _ in range(range_[0], range_[1])]
            compiled_ranges.append(sub_list)
        out = [list(self.items)]
        current_funnel = list(self.items)
        while not are_sequences_matched(out[-1], destination):
            temp_funnel = []
            for i, val in enumerate(current_funnel):
                if val == destination[i]:
                    temp_funnel.append(val)
                else:
                    choice_options = compiled_ranges[i]
                    random_choice = random.choice(choice_options)
                    temp_funnel.append(random_choice)
            out.append(temp_funnel)
            current_funnel = temp_funnel
        return type(self)(out)

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
    def range(class_, start, stop, step):
        def drange(x, y, jump):
            while x < y:
                yield float(x)
                x += decimal.Decimal(jump)

        returned_list = list(drange(start, stop, decimal.Decimal(f"{step}")))
        return class_(returned_list)

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

    def reduce_time_signatures_in_list(self):
        ts_l = [_ for _ in self]

        def reduce_time_signature(t):
            nf = abjad.NonreducedFraction(t.pair)
            f = quicktions.Fraction(t.pair[0], t.pair[1])
            if f.denominator < 4:
                nf_ = nf.with_denominator(4)
                nt = abjad.TimeSignature(nf_.pair)
            else:
                nt = abjad.TimeSignature((f.numerator, f.denominator))
            return nt

        out = []
        for _ in ts_l:
            nt = reduce_time_signature(_)
            out.append(nt)
        return type(self)(out)

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
        n = n % len(lst)
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

    def stack_pitches(self, as_ratios=False, direction="up"):
        """

        .. container:: example

            >>> s = evans.Sequence([1, -2, 3])
            >>> s.stack_pitches()
            Sequence([1, 10, 15])

        """
        returned_list = [self.items[0]]
        if as_ratios:
            for _ in self.items[1:]:
                if direction == "up":
                    while _ < returned_list[-1]:
                        _ *= 2
                else:
                    while returned_list[-1] < _:
                        _ /= 2
                returned_list.append(_)
            seq = type(self)(returned_list)
        else:
            for _ in self.items[1:]:
                if direction == "up":
                    while _ < returned_list[-1]:
                        _ += 12
                else:
                    while returned_list[-1] < _:
                        _ -= 12
                returned_list.append(_)
            seq = type(self)(returned_list)
        return seq

    def string_to_morse_durations(self):
        text = self.text_to_morse()
        out = []
        cleaned_out = []
        for char in text:
            if char == ".":
                out.append(1)
            elif char == "-":
                out.append(3)
            elif char == "˽":
                out.append(-3)
            elif char == " ":
                out.append(-7)
            else:
                raise Exception(f"WRONG CHAR TYPE: {char}")
        for i, duration in enumerate(out):
            if i + 1 < len(out):
                if duration == -3 and out[i + 1] == -7:
                    continue
                else:
                    cleaned_out.append(duration)
        return type(self)(cleaned_out)

    def string_to_morse_tuplets(self):
        text = self.text_to_morse()
        out = []
        temp = []
        for char in text:
            if char == ".":
                temp.append(1)
            elif char == "-":
                temp.append(2)
            elif char == "˽":
                temp_tuple = tuple(temp)
                out.append(temp_tuple)
                temp = []
            elif char == " ":
                out.append((-1,))
            else:
                raise Exception(f"WRONG CHAR TYPE: {char}")
        return type(self)(out)

    def stutter(self, counts=[2], indices=[0], period=1, cyclic=True):
        out = []
        cyc_counts = CyclicList(counts, forget=False)
        for i, item in enumerate(self.items):
            if cyclic is True:
                if i % period in indices:
                    count = cyc_counts(r=1)[0]
                    for _ in range(count):
                        out.append(item)
                else:
                    out.append(item)
            else:
                if i in indices:
                    count = cyc_counts(r=1)[0]
                    for _ in range(count):
                        out.append(item)
                else:
                    out.append(item)
        seq = type(self)(out)
        return seq

    def text_to_morse(self):
        text = "".join(self)

        morse_dict = {
            "a": ".-",
            "b": "-...",
            "c": "-.-.",
            "d": "-..",
            "e": ".",
            "f": "..-.",
            "g": "--.",
            "h": "....",
            "i": "..",
            "j": ".---",
            "k": "-.-",
            "l": ".-..",
            "m": "--",
            "n": "-.",
            "o": "---",
            "p": ".--.",
            "q": "--.-",
            "r": ".-.",
            "s": "...",
            "t": "-",
            "u": "..-",
            "v": "...-",
            "w": ".--",
            "x": "-..-",
            "y": "-.--",
            "z": "--..",
            "á": ".--.-",
            "ä": ".-.-",
            "à": ".--.-",
            "é": "..-..",
            "è": ".-..-",
            "ñ": "--.--",
            "ö": "---.",
            "ó": "---.",
            "ü": "..---",
            " ": " ",  # Word separation
        }

        morse_code = ""
        for char in text.lower():
            if char in morse_dict:
                if char != " ":
                    morse_code += morse_dict[char] + "˽"
                else:
                    morse_code += morse_dict[char]
            else:
                continue

        return morse_code

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
            if _ is not None:
                val = _ + n
                returned_list.append(val)
            else:
                returned_list.append(_)
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
        out = [_ for _ in itertools.zip_longest(first_half, second_half)]
        return type(self)(out).flatten().remove_none()


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


class CompoundMelody:
    def __init__(
        self,
        foreground,
        background,
        foreground_partitions=[1],
        background_partitions=[1],
        foreground_second=False,
        force_matching_lengths=True,
        repartition_counts=None,
        overhang=False,
    ):
        self._foreground = foreground
        self._background = background
        self.foreground_partitions = foreground_partitions
        self.background_partitions = background_partitions
        self.foreground_second = foreground_second
        self.force_matching_lengths = force_matching_lengths
        self.repartition_counts = repartition_counts
        self.overhang = overhang
        self._partitioned_foreground = abjad.sequence.partition_by_counts(
            foreground,
            foreground_partitions,
            cyclic=True,
            overhang=True,
        )
        self._partitioned_background = abjad.sequence.partition_by_counts(
            background,
            background_partitions,
            cyclic=True,
            overhang=True,
        )
        if force_matching_lengths is True:
            assert len(self._partitioned_foreground) == len(
                self._partitioned_background
            )
        if foreground_second is False:
            zip_generator = [
                _
                for _ in zip(self._partitioned_foreground, self._partitioned_background)
            ]
            self._zipped_partitions = []
            for i, _ in enumerate(zip_generator):
                self._zipped_partitions.append(_)
            if self.overhang is True:
                if i + 1 < len(self._partitioned_foreground):
                    for extra_value in self._partitioned_foreground[i + 1 :]:
                        self._zipped_partitions.append(extra_value)
                if i + 1 < len(self._partitioned_background):
                    for extra_value in self._partitioned_background[i + 1 :]:
                        self._zipped_partitions.append(extra_value)
        else:
            zip_generator = [
                _
                for _ in zip(self._partitioned_background, self._partitioned_foreground)
            ]
            self._zipped_partitions = []
            for i, _ in enumerate(zip_generator):
                self._zipped_partitions.append(_)
            if self.overhang is True:
                if i + 1 < len(self._partitioned_foreground):
                    for extra_value in self._partitioned_foreground[i + 1 :]:
                        self._zipped_partitions.append(extra_value)
                if i + 1 < len(self._partitioned_background):
                    for extra_value in self._partitioned_background[i + 1 :]:
                        self._zipped_partitions.append(extra_value)

        self._items = abjad.sequence.flatten(self._zipped_partitions, depth=-1)
        if self.repartition_counts is not None:
            self._items = abjad.sequence.partition_by_counts(
                self._items, self.repartition_counts, cyclic=True, overhang=True
            )

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        argument = type(self)(items=argument)
        items = self.items + argument.items
        return type(self)(items)

    def __contains__(self, argument):
        return argument in self._items

    def __eq__(self, argument):
        if isinstance(argument, type(self)):
            return self.items == argument.items
        return False

    def __getitem__(self, argument):
        result = self._items.__getitem__(argument)
        if isinstance(argument, slice):
            return type(self)(result)
        return result

    def __iter__(self):
        for item in self._items:
            yield item

    def __len__(self):
        return len(self._items)

    def __radd__(self, argument):
        argument = type(self)(items=argument)
        items = argument.items + self.items
        return type(self)(items)

    def __repr__(self):
        items = ", ".join([repr(_) for _ in self.items])
        string = f"{type(self).__name__}([{items}])"
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items

    @property
    def partitioned_items(self):
        return self._zipped_partitions

    @property
    def foreground(self):
        return self._foreground

    @property
    def partitioned_foreground(self):
        return self._partitioned_foreground

    @property
    def background(self):
        return self._background

    @property
    def partitioned_background(self):
        return self._partitioned_background


def combine_ts_lists(spans, start_offsets_only=True):
    if start_offsets_only is True:
        start_offsets = [span.start_offset for span in spans]
        start_offsets.append(spans.stop_offset)
        start_offsets = list(set(start_offsets))
        start_offsets.sort()
        new_spans = []
        for start, stop in abjad.sequence.nwise(start_offsets, 2):
            new_spans.append(abjad.Timespan(start, stop))
        spans = new_spans
    offset_counter = abjad.OffsetCounter(spans)
    offsets = list(set(item[0] for item in offset_counter.items.items()))
    offsets.sort()
    reduced_spans = []
    for start, stop in abjad.sequence.nwise(offsets, 2):
        reduced_spans.append(abjad.Timespan(start, stop))
    final_tsl = abjad.TimespanList(reduced_spans)
    return final_tsl


def make_time_signatures_from_ts_list(tsl):
    assert tsl.is_sorted
    durations = [_.duration for _ in tsl]
    assert sum(durations) == tsl.duration
    signatures = Sequence([abjad.TimeSignature(_) for _ in durations])
    out = signatures.reduce_time_signatures_in_list()
    return out


def time_signature_list_to_timespan_list(tsl):
    offsets = [abjad.Offset(_) for _ in tsl]
    cum_sums = abjad.math.cumulative_sums(offsets)
    spans = abjad.TimespanList()
    for pair in consort.iterate_nwise(cum_sums, 2):
        span = abjad.Timespan(pair[0], pair[1])
        spans.append(span)

    return spans


def intersect_time_signature_lists(
    *args, translation=(1, 4)
):  ### fix this. look at unity capsule process
    tsls = [time_signature_list_to_timespan_list(arg) for arg in args]
    tsls[1].translate(translation)
    combined = combine_ts_lists(abjad.TimespanList(tsls[0] + tsls[1]))
    out = make_time_signatures_from_ts_list(combined)
    return out


def fuse_signatures_below_threshold(
    signatures, threshhold=(1, 8), direction=abjad.LEFT
):
    threshhold = abjad.NonreducedFraction(threshhold)
    fracs = []
    delayed = None
    fracs.append(abjad.NonreducedFraction(signatures[0]))
    for signature in signatures[1:]:
        frac = abjad.NonreducedFraction(signature)
        if delayed is not None:
            frac = frac + delayed
            delayed = None
        if threshhold <= frac:
            fracs.append(frac)
        else:
            if direction == abjad.LEFT:
                fracs[-1] += frac
            elif direction == abjad.RIGHT:
                delayed = frac
            else:
                raise Exception(
                    f"Value of direction must be abjad.LEFT or abjad.RIGHT. Got {direction}"
                )
    fused_signatures = [abjad.TimeSignature(_) for _ in fracs]
    return fused_signatures


def cyclically_subtract_fraction(
    series,
    durations=[(1, 12), (1, 24), (1, 20)],
    target_indices=[2, 4, 8, 12, 15, 21],
    period=22,
):
    series = [abjad.NonreducedFraction(_) for _ in series]
    cyclic_durs = CyclicList(
        [abjad.NonreducedFraction(_) for _ in durations], forget=False
    )
    out = []
    for i, value in enumerate(series):
        if i % period in target_indices:
            subtracted_duration = cyclic_durs(r=1)[0]
            new_value = abjad.NonreducedFraction(value) - subtracted_duration
            out.append(new_value)
        else:
            out.append(value)
    assert len(out) == len(
        series
    ), f"len(out): {len(out)} != len(series): {len(series)}"
    return out
