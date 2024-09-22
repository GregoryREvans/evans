from fractions import Fraction

import abjad
import baca

from .sequence import CyclicList, fuse_signatures_below_threshold


def preprocess_divisions(
    divisions,
    sum=False,
    quarters=False,
    eighths=False,
    fuse_counts=None,
    cyclic_fuse=True,
    flatten_before_fuse=True,
    split_at_measure_boundaries=False,
    split_divisions_by_proportions=None,
):
    old_divisions = divisions
    divisions = [abjad.Duration(_.pair) for _ in divisions]
    if sum is True:
        divisions = [abjad.sequence.sum(divisions)]
    if quarters is True:
        divisions = [baca.sequence.quarters([_]) for _ in divisions]
    if eighths is True:
        divisions = [
            baca.sequence.split_divisions([_], [(1, 8)], cyclic=True) for _ in divisions
        ]
    if split_divisions_by_proportions is not None:
        cyc_partitions = CyclicList(split_divisions_by_proportions, forget=False)
        pulled_partitions = cyc_partitions(r=len(divisions))
        temp = []
        for division, partition in zip(divisions, pulled_partitions):
            full_partition = 0
            for integer in partition:
                full_partition += integer
            partition_fractions = [Fraction(_, full_partition) for _ in partition]
            for fraction in partition_fractions:
                temp.append(division * fraction)
        divisions = temp
    if fuse_counts is not None:
        if flatten_before_fuse is True:
            divisions = abjad.sequence.flatten(divisions, depth=-1)
            divisions = abjad.sequence.partition_by_counts(
                divisions,
                fuse_counts,
                cyclic=cyclic_fuse,
                overhang=True,
            )
            divisions = [abjad.sequence.sum(_) for _ in divisions]
        else:
            temp = []
            for measure in divisions:
                m = abjad.sequence.partition_by_counts(
                    measure,
                    fuse_counts,
                    cyclic=cyclic_fuse,
                    overhang=True,
                )
                m_ = [abjad.sequence.sum(_) for _ in m]
                temp.append(m_)
            divisions = abjad.sequence.flatten(temp, depth=-1)
    divisions = abjad.sequence.flatten(divisions, depth=-1)
    if split_at_measure_boundaries is True:
        divisions = abjad.sequence.split(divisions, old_divisions)
        divisions = abjad.sequence.flatten(divisions, depth=-1)
    return divisions


def make_preprocessor(
    sum=False,
    quarters=False,
    eighths=False,
    fuse_counts=None,
    cyclic_fuse=True,
    split_at_measure_boundaries=False,
    split_divisions_by_proportions=None,
):
    def returned_function(divisions):
        divisions_ = preprocess_divisions(
            divisions,
            sum=sum,
            fuse_counts=fuse_counts,
            cyclic_fuse=cyclic_fuse,
            quarters=quarters,
            eighths=eighths,
            split_at_measure_boundaries=split_at_measure_boundaries,
            split_divisions_by_proportions=split_divisions_by_proportions,
        )
        return divisions_

    return returned_function


# Polillas Preprocessors


def fuse_preprocessor(divisions):
    return [abjad.sequence.sum(divisions)]


def fuse_preprocessor_2(divisions):
    divisions = abjad.sequence.partition_by_counts(
        divisions, (2,), cyclic=True, overhang=True
    )
    return [sum(_) for _ in divisions]


def fuse_preprocessor_3(divisions):
    divisions = abjad.sequence.partition_by_counts(
        divisions, (3,), cyclic=True, overhang=True
    )
    return [sum(_) for _ in divisions]


def fuse_preprocessor_2_1(divisions):
    divisions = abjad.sequence.partition_by_counts(
        divisions, (2, 1), cyclic=True, overhang=True
    )
    return [sum(_) for _ in divisions]


def fuse_preprocessor_3_1(divisions):
    divisions = abjad.sequence.partition_by_counts(
        divisions, (3, 1), cyclic=True, overhang=True
    )
    return [sum(_) for _ in divisions]


def fuse_preprocessor_3_2(divisions):
    divisions = abjad.sequence.partition_by_counts(
        divisions, (3, 2), cyclic=True, overhang=True
    )
    return [sum(_) for _ in divisions]


def fuse_quarters_preprocessor(divisions):
    duration = abjad.sequence.sum(divisions)
    divisions = [duration]
    divisions = [baca.sequence.quarters([_]) for _ in divisions]
    divisions = abjad.sequence.flatten(divisions, depth=-1)
    return divisions


def fuse_quarters_preprocessor_2_1(divisions):
    duration = abjad.sequence.sum(divisions)
    divisions = [duration]
    divisions = [baca.sequence.quarters([_]) for _ in divisions]
    divisions = abjad.sequence.flatten(divisions, depth=-1)
    divisions = abjad.sequence.partition_by_counts(
        divisions, (2, 1), cyclic=True, overhang=True
    )
    return [sum(_) for _ in divisions]


def fuse_quarters_preprocessor_1_2(divisions):
    duration = abjad.sequence.sum(divisions)
    divisions = [duration]
    divisions = [baca.sequence.quarters([_]) for _ in divisions]
    divisions = abjad.sequence.flatten(divisions, depth=-1)
    divisions = abjad.sequence.partition_by_counts(
        divisions, (1, 2), cyclic=True, overhang=True
    )
    return [sum(_) for _ in divisions]


def fuse_quarters_preprocessor_1_1_2(divisions):
    duration = abjad.sequence.sum(divisions)
    divisions = [duration]
    divisions = [baca.sequence.quarters([_]) for _ in divisions]
    divisions = abjad.sequence.flatten(divisions, depth=-1)
    divisions = abjad.sequence.partition_by_counts(
        divisions, (1, 1, 2), cyclic=True, overhang=True
    )
    return [sum(_) for _ in divisions]


def fuse_quarters_preprocessor_2_2_5(divisions):
    duration = abjad.sequence.sum(divisions)
    divisions = [duration]
    divisions = [baca.sequence.quarters([_]) for _ in divisions]
    divisions = abjad.sequence.flatten(divisions, depth=-1)
    divisions = abjad.sequence.partition_by_counts(
        divisions, (2, 2, 5), cyclic=False, overhang=True
    )
    return [sum(_) for _ in divisions]


def quarters_preprocessor_2_1(divisions):
    divisions = [baca.sequence.quarters([_]) for _ in divisions]
    temp = []
    for measure in divisions:
        partitions = abjad.sequence.flatten(measure, depth=-1)
        partitions = abjad.sequence.partition_by_counts(
            partitions,
            (2, 1),
            cyclic=True,
            overhang=True,
        )
        sums = [sum(_) for _ in partitions]
        temp.append(sums)
    divisions = abjad.sequence.flatten(temp, depth=-1)
    return divisions


def quarters_preprocessor_2(divisions):
    divisions = [baca.sequence.quarters([_]) for _ in divisions]
    temp = []
    for measure in divisions:
        partitions = abjad.sequence.flatten(measure, depth=-1)
        partitions = abjad.sequence.partition_by_counts(
            partitions,
            (2,),
            cyclic=True,
            overhang=True,
        )
        sums = [sum(_) for _ in partitions]
        temp.append(sums)
    divisions = abjad.sequence.flatten(temp, depth=-1)
    return divisions


# def pure_quarters_preprocessor(divisions):
#     divisions = [baca.sequence.quarters([_]) for _ in divisions]
#     divisions = abjad.sequence.flatten(divisions, depth=-1)
#     return divisions


def pure_quarters_preprocessor(divisions):
    divisions = [abjad.Duration(_) for _ in divisions]  # WARNING: must coerce type?
    divisions = [baca.sequence.quarters([_]) for _ in divisions]
    divisions = abjad.sequence.flatten(divisions, depth=-1)
    return divisions


def quarters_preprocessor_3_1_2(divisions):
    divisions = [baca.sequence.quarters([_]) for _ in divisions]
    temp = []
    for measure in divisions:
        partitions = abjad.sequence.flatten(measure, depth=-1)
        partitions = abjad.sequence.partition_by_counts(
            partitions,
            (3, 1, 2),
            cyclic=True,
            overhang=True,
        )
        sums = [sum(_) for _ in partitions]
        temp.append(sums)
    divisions = abjad.sequence.flatten(temp, depth=-1)
    return divisions


def fuse_quarters_preprocessor_3_1(divisions):
    duration = abjad.sequence.sum(divisions)
    divisions = [duration]
    divisions = [baca.sequence.quarters([_]) for _ in divisions]
    divisions = abjad.sequence.flatten(divisions, depth=-1)
    divisions = abjad.sequence.partition_by_counts(
        divisions, (3, 1), cyclic=True, overhang=True
    )
    return [sum(_) for _ in divisions]


def quarters_preprocessor(divisions):
    divisions = [baca.sequence.quarters([_], compound=(3, 2)) for _ in divisions]
    divisions = abjad.sequence.flatten(divisions, depth=-1)
    return divisions


def fuse_quarters_preprocessor_2_20(divisions):
    duration = abjad.sequence.sum(divisions)
    divisions = [duration]
    divisions = [baca.sequence.quarters([_]) for _ in divisions]
    divisions = abjad.sequence.flatten(divisions, depth=-1)
    divisions = abjad.sequence.partition_by_counts(
        divisions, (2, 20), cyclic=True, overhang=True
    )
    return [sum(_) for _ in divisions]


def time_signatures_to_quarters(sigs, threshhold=(2, 4)):
    out = []
    size = sum([abjad.Duration(sig) for sig in sigs])
    quarters = make_preprocessor(quarters=True)([size])
    out.append(quarters[0])
    for quarter in quarters[1:]:
        if out[-1] < abjad.Duration(4, 4):
            out[-1] += quarter
        else:
            out.append(quarter)
    signatures = [abjad.TimeSignature(_) for _ in out]
    signatures_ = fuse_signatures_below_threshold(
        signatures, threshhold=threshhold, direction=abjad.LEFT
    )
    return signatures_


def reduce_measure_ranges_to_common_time(signatures, ranges, threshhold=(2, 4)):
    returned_signatures = []
    out = []
    if 1 < len(ranges):
        nwise_ranges = abjad.sequence.nwise(ranges, 2)
        constructed_ranges = []
        for range_ in nwise_ranges:
            constructed_ranges.append(range_[0])
            constructed_ranges.append((range_[0][-1], range_[1][0]))
            constructed_ranges.append(range_[1])
        constructed_ranges = list(set(constructed_ranges))
    else:
        constructed_ranges = [_ for _ in ranges]
    if ranges[-1][-1] <= len(signatures) - 1:
        constructed_ranges.append((ranges[-1][-1], len(signatures)))
    constructed_ranges.sort(key=lambda _: _[0])
    for range__ in constructed_ranges:
        if range__ in ranges:
            commons = time_signatures_to_quarters(
                signatures[range__[0] : range__[1]], threshhold=threshhold
            )
            returned_signatures.extend(commons)
        else:
            group = signatures[range__[0] : range__[1]]
            returned_signatures.extend(group)
    for i, meter in enumerate(returned_signatures):
        non_reduced_fraction = abjad.NonreducedFraction(meter.pair).with_denominator(4)
        new_sig = abjad.TimeSignature(non_reduced_fraction)
        returned_signatures[i] = new_sig
    assert sum([abjad.Duration(_) for _ in returned_signatures]) == sum(
        [abjad.Duration(_) for _ in signatures]
    )
    return returned_signatures
