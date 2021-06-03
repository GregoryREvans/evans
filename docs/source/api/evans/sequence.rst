.. _evans--sequence:

sequence
========

.. automodule:: evans.sequence

.. currentmodule:: evans.sequence

.. container:: svg-container

   .. inheritance-diagram:: evans
      :lineage: evans.sequence

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~CyclicList
   ~MarkovChain
   ~PitchClassSegment
   ~PitchClassSet
   ~PitchSegment
   ~PitchSet
   ~Ratio
   ~RatioClassSegment
   ~RatioClassSet
   ~RatioSegment
   ~RatioSet
   ~Sequence

.. autoclass:: CyclicList

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __repr__
      __str__
      non_state_cyc
      state
      state_cyc

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: CyclicList.__call__

   .. automethod:: CyclicList.__repr__

   .. automethod:: CyclicList.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: CyclicList.non_state_cyc

   .. automethod:: CyclicList.state

   .. automethod:: CyclicList.state_cyc

.. autoclass:: MarkovChain

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __repr__
      __str__
      generate_states
      next_state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: MarkovChain.__repr__

   .. automethod:: MarkovChain.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: MarkovChain.generate_states

   .. automethod:: MarkovChain.next_state

.. autoclass:: PitchClassSegment

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      alpha
      to_sequence

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchClassSegment.__add__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__contains__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__getitem__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__iter__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__len__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__repr__

   .. container:: inherited

      .. automethod:: PitchClassSegment.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PitchClassSegment.alpha

   .. container:: inherited

      .. automethod:: PitchClassSegment.complement

   .. container:: inherited

      .. automethod:: PitchClassSegment.invert

   .. container:: inherited

      .. automethod:: PitchClassSegment.multiply

   .. container:: inherited

      .. automethod:: PitchClassSegment.retrograde

   .. container:: inherited

      .. automethod:: PitchClassSegment.rotate

   .. container:: inherited

      .. automethod:: PitchClassSegment.sorted

   .. automethod:: PitchClassSegment.to_sequence

   .. container:: inherited

      .. automethod:: PitchClassSegment.transpose

.. autoclass:: PitchClassSet

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      alpha
      to_sequence

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchClassSet.__add__

   .. container:: inherited

      .. automethod:: PitchClassSet.__contains__

   .. container:: inherited

      .. automethod:: PitchClassSet.__getitem__

   .. container:: inherited

      .. automethod:: PitchClassSet.__iter__

   .. container:: inherited

      .. automethod:: PitchClassSet.__len__

   .. container:: inherited

      .. automethod:: PitchClassSet.__repr__

   .. container:: inherited

      .. automethod:: PitchClassSet.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PitchClassSet.alpha

   .. container:: inherited

      .. automethod:: PitchClassSet.complement

   .. container:: inherited

      .. automethod:: PitchClassSet.invert

   .. container:: inherited

      .. automethod:: PitchClassSet.multiply

   .. container:: inherited

      .. automethod:: PitchClassSet.normal_order

   .. container:: inherited

      .. automethod:: PitchClassSet.prime_form

   .. container:: inherited

      .. automethod:: PitchClassSet.sorted

   .. automethod:: PitchClassSet.to_sequence

   .. container:: inherited

      .. automethod:: PitchClassSet.transpose

.. autoclass:: PitchSegment

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      alpha
      to_sequence

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchSegment.__add__

   .. container:: inherited

      .. automethod:: PitchSegment.__contains__

   .. container:: inherited

      .. automethod:: PitchSegment.__getitem__

   .. container:: inherited

      .. automethod:: PitchSegment.__iter__

   .. container:: inherited

      .. automethod:: PitchSegment.__len__

   .. container:: inherited

      .. automethod:: PitchSegment.__repr__

   .. container:: inherited

      .. automethod:: PitchSegment.__setitem__

   .. container:: inherited

      .. automethod:: PitchSegment.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PitchSegment.alpha

   .. container:: inherited

      .. automethod:: PitchSegment.complement

   .. container:: inherited

      .. automethod:: PitchSegment.invert

   .. container:: inherited

      .. automethod:: PitchSegment.multiply

   .. container:: inherited

      .. automethod:: PitchSegment.retrograde

   .. container:: inherited

      .. automethod:: PitchSegment.rotate

   .. container:: inherited

      .. automethod:: PitchSegment.sorted

   .. automethod:: PitchSegment.to_sequence

   .. container:: inherited

      .. automethod:: PitchSegment.transpose

.. autoclass:: PitchSet

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      alpha
      to_sequence

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PitchSet.__add__

   .. container:: inherited

      .. automethod:: PitchSet.__contains__

   .. container:: inherited

      .. automethod:: PitchSet.__getitem__

   .. container:: inherited

      .. automethod:: PitchSet.__iter__

   .. container:: inherited

      .. automethod:: PitchSet.__len__

   .. container:: inherited

      .. automethod:: PitchSet.__repr__

   .. container:: inherited

      .. automethod:: PitchSet.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PitchSet.alpha

   .. container:: inherited

      .. automethod:: PitchSet.complement

   .. container:: inherited

      .. automethod:: PitchSet.invert

   .. container:: inherited

      .. automethod:: PitchSet.multiply

   .. container:: inherited

      .. automethod:: PitchSet.sorted

   .. automethod:: PitchSet.to_sequence

   .. container:: inherited

      .. automethod:: PitchSet.transpose

.. autoclass:: Ratio

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      extract_sub_ratios

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Ratio.__contains__

   .. container:: inherited

      .. automethod:: Ratio.__eq__

   .. container:: inherited

      .. automethod:: Ratio.__getitem__

   .. container:: inherited

      .. automethod:: Ratio.__hash__

   .. container:: inherited

      .. automethod:: Ratio.__iter__

   .. container:: inherited

      .. automethod:: Ratio.__len__

   .. container:: inherited

      .. automethod:: Ratio.__rdiv__

   .. container:: inherited

      .. automethod:: Ratio.__repr__

   .. container:: inherited

      .. automethod:: Ratio.__reversed__

   .. container:: inherited

      .. automethod:: Ratio.__rtruediv__

   .. container:: inherited

      .. automethod:: Ratio.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Ratio.count

   .. automethod:: Ratio.extract_sub_ratios

   .. container:: inherited

      .. automethod:: Ratio.index

   .. container:: inherited

      .. automethod:: Ratio.partition_integer

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Ratio.multipliers

   .. container:: inherited

      .. autoattribute:: Ratio.numbers

   .. container:: inherited

      .. autoattribute:: Ratio.reciprocal

.. autoclass:: RatioClassSegment

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      to_sequence

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RatioClassSegment.__add__

   .. container:: inherited

      .. automethod:: RatioClassSegment.__contains__

   .. container:: inherited

      .. automethod:: RatioClassSegment.__getitem__

   .. container:: inherited

      .. automethod:: RatioClassSegment.__iter__

   .. container:: inherited

      .. automethod:: RatioClassSegment.__len__

   .. container:: inherited

      .. automethod:: RatioClassSegment.__repr__

   .. container:: inherited

      .. automethod:: RatioClassSegment.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RatioClassSegment.complement

   .. container:: inherited

      .. automethod:: RatioClassSegment.invert

   .. container:: inherited

      .. automethod:: RatioClassSegment.multiply

   .. container:: inherited

      .. automethod:: RatioClassSegment.retrograde

   .. container:: inherited

      .. automethod:: RatioClassSegment.rotate

   .. container:: inherited

      .. automethod:: RatioClassSegment.sorted

   .. automethod:: RatioClassSegment.to_sequence

   .. container:: inherited

      .. automethod:: RatioClassSegment.transpose

.. autoclass:: RatioClassSet

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      to_sequence

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RatioClassSet.__add__

   .. container:: inherited

      .. automethod:: RatioClassSet.__contains__

   .. container:: inherited

      .. automethod:: RatioClassSet.__getitem__

   .. container:: inherited

      .. automethod:: RatioClassSet.__iter__

   .. container:: inherited

      .. automethod:: RatioClassSet.__len__

   .. container:: inherited

      .. automethod:: RatioClassSet.__repr__

   .. container:: inherited

      .. automethod:: RatioClassSet.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RatioClassSet.complement

   .. container:: inherited

      .. automethod:: RatioClassSet.invert

   .. container:: inherited

      .. automethod:: RatioClassSet.multiply

   .. container:: inherited

      .. automethod:: RatioClassSet.sorted

   .. automethod:: RatioClassSet.to_sequence

   .. container:: inherited

      .. automethod:: RatioClassSet.transpose

.. autoclass:: RatioSegment

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      to_sequence

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RatioSegment.__add__

   .. container:: inherited

      .. automethod:: RatioSegment.__contains__

   .. container:: inherited

      .. automethod:: RatioSegment.__getitem__

   .. container:: inherited

      .. automethod:: RatioSegment.__iter__

   .. container:: inherited

      .. automethod:: RatioSegment.__len__

   .. container:: inherited

      .. automethod:: RatioSegment.__repr__

   .. container:: inherited

      .. automethod:: RatioSegment.__setitem__

   .. container:: inherited

      .. automethod:: RatioSegment.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RatioSegment.complement

   .. container:: inherited

      .. automethod:: RatioSegment.constrain_to_octave

   .. container:: inherited

      .. automethod:: RatioSegment.invert

   .. container:: inherited

      .. automethod:: RatioSegment.multiply

   .. container:: inherited

      .. automethod:: RatioSegment.retrograde

   .. container:: inherited

      .. automethod:: RatioSegment.rotate

   .. container:: inherited

      .. automethod:: RatioSegment.sorted

   .. automethod:: RatioSegment.to_sequence

   .. container:: inherited

      .. automethod:: RatioSegment.transpose

.. autoclass:: RatioSet

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      to_sequence

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RatioSet.__add__

   .. container:: inherited

      .. automethod:: RatioSet.__contains__

   .. container:: inherited

      .. automethod:: RatioSet.__getitem__

   .. container:: inherited

      .. automethod:: RatioSet.__iter__

   .. container:: inherited

      .. automethod:: RatioSet.__len__

   .. container:: inherited

      .. automethod:: RatioSet.__repr__

   .. container:: inherited

      .. automethod:: RatioSet.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: RatioSet.complement

   .. container:: inherited

      .. automethod:: RatioSet.constrain_to_octave

   .. container:: inherited

      .. automethod:: RatioSet.invert

   .. container:: inherited

      .. automethod:: RatioSet.multiply

   .. container:: inherited

      .. automethod:: RatioSet.sorted

   .. automethod:: RatioSet.to_sequence

   .. container:: inherited

      .. automethod:: RatioSet.transpose

.. autoclass:: Sequence

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      add_sequences
      alpha
      chen
      combination_addition
      combination_division
      combination_multiplication
      combination_subtraction
      combinations
      derive_added_sequences
      derive_multiplied_sequences
      divide_all
      e_bonacci_cycle
      e_dovan_cycle
      feigenbaum_bifurcations
      grouper
      guerrero_morales
      henon
      hexagonal_sequence
      josephus
      lindenmayer
      linear_asymmetric_inversion
      lorenz
      lu_chen
      mandelbrot_set
      map_dict
      map_indices
      markov
      matrix
      mirror
      mod
      multiply
      multiply_all
      multiply_sequences
      n_bonacci_cycle
      normalize_to_indices
      normalize_to_sum
      orbits
      permutations
      pitch_warp
      potamia
      prime_sequence
      prism_sequence
      random_walk
      ratio
      recaman_sequence
      reciprocals
      remove_none
      reproportion_by_base
      roessler
      rotate
      stack_intervals
      stack_pitches
      subtract_all
      transpose
      warp
      zipped_bifurcation

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Sequence.__add__

   .. container:: inherited

      .. automethod:: Sequence.__contains__

   .. container:: inherited

      .. automethod:: Sequence.__eq__

   .. container:: inherited

      .. automethod:: Sequence.__getitem__

   .. container:: inherited

      .. automethod:: Sequence.__hash__

   .. container:: inherited

      .. automethod:: Sequence.__iter__

   .. container:: inherited

      .. automethod:: Sequence.__len__

   .. container:: inherited

      .. automethod:: Sequence.__radd__

   .. container:: inherited

      .. automethod:: Sequence.__repr__

   .. container:: inherited

      .. automethod:: Sequence.__reversed__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: Sequence.accumulate

   .. automethod:: Sequence.add_sequences

   .. automethod:: Sequence.alpha

   .. container:: inherited

      .. automethod:: Sequence.boustrophedon

   .. automethod:: Sequence.combination_addition

   .. automethod:: Sequence.combination_division

   .. automethod:: Sequence.combination_multiplication

   .. automethod:: Sequence.combination_subtraction

   .. automethod:: Sequence.combinations

   .. container:: inherited

      .. automethod:: Sequence.count

   .. container:: inherited

      .. automethod:: Sequence.degree_of_rotational_symmetry

   .. automethod:: Sequence.derive_added_sequences

   .. automethod:: Sequence.derive_multiplied_sequences

   .. automethod:: Sequence.divide_all

   .. container:: inherited

      .. automethod:: Sequence.filter

   .. container:: inherited

      .. automethod:: Sequence.flatten

   .. container:: inherited

      .. automethod:: Sequence.fuse

   .. container:: inherited

      .. automethod:: Sequence.group_by

   .. container:: inherited

      .. automethod:: Sequence.group_by_sign

   .. automethod:: Sequence.grouper

   .. automethod:: Sequence.guerrero_morales

   .. container:: inherited

      .. automethod:: Sequence.helianthate

   .. automethod:: Sequence.hexagonal_sequence

   .. container:: inherited

      .. automethod:: Sequence.index

   .. container:: inherited

      .. automethod:: Sequence.is_decreasing

   .. container:: inherited

      .. automethod:: Sequence.is_increasing

   .. container:: inherited

      .. automethod:: Sequence.is_permutation

   .. container:: inherited

      .. automethod:: Sequence.is_repetition_free

   .. container:: inherited

      .. automethod:: Sequence.join

   .. automethod:: Sequence.josephus

   .. automethod:: Sequence.linear_asymmetric_inversion

   .. container:: inherited

      .. automethod:: Sequence.map

   .. automethod:: Sequence.map_dict

   .. automethod:: Sequence.map_indices

   .. automethod:: Sequence.matrix

   .. automethod:: Sequence.mirror

   .. automethod:: Sequence.mod

   .. automethod:: Sequence.multiply

   .. automethod:: Sequence.multiply_all

   .. automethod:: Sequence.multiply_sequences

   .. automethod:: Sequence.normalize_to_indices

   .. automethod:: Sequence.normalize_to_sum

   .. container:: inherited

      .. automethod:: Sequence.nwise

   .. container:: inherited

      .. automethod:: Sequence.partition

   .. container:: inherited

      .. automethod:: Sequence.partition_by_counts

   .. container:: inherited

      .. automethod:: Sequence.partition_by_ratio_of_lengths

   .. container:: inherited

      .. automethod:: Sequence.partition_by_ratio_of_weights

   .. container:: inherited

      .. automethod:: Sequence.partition_by_weights

   .. container:: inherited

      .. automethod:: Sequence.period_of_rotation

   .. automethod:: Sequence.permutations

   .. container:: inherited

      .. automethod:: Sequence.permute

   .. automethod:: Sequence.pitch_warp

   .. automethod:: Sequence.potamia

   .. automethod:: Sequence.prism_sequence

   .. container:: inherited

      .. automethod:: Sequence.quarters

   .. automethod:: Sequence.random_walk

   .. container:: inherited

      .. automethod:: Sequence.ratios

   .. automethod:: Sequence.recaman_sequence

   .. automethod:: Sequence.reciprocals

   .. container:: inherited

      .. automethod:: Sequence.remove

   .. automethod:: Sequence.remove_none

   .. container:: inherited

      .. automethod:: Sequence.remove_repeats

   .. container:: inherited

      .. automethod:: Sequence.repeat

   .. container:: inherited

      .. automethod:: Sequence.repeat_by

   .. container:: inherited

      .. automethod:: Sequence.repeat_to_length

   .. container:: inherited

      .. automethod:: Sequence.repeat_to_weight

   .. container:: inherited

      .. automethod:: Sequence.replace

   .. container:: inherited

      .. automethod:: Sequence.replace_at

   .. automethod:: Sequence.reproportion_by_base

   .. container:: inherited

      .. automethod:: Sequence.retain

   .. container:: inherited

      .. automethod:: Sequence.retain_pattern

   .. container:: inherited

      .. automethod:: Sequence.reveal

   .. container:: inherited

      .. automethod:: Sequence.reverse

   .. automethod:: Sequence.rotate

   .. container:: inherited

      .. automethod:: Sequence.sort

   .. container:: inherited

      .. automethod:: Sequence.split

   .. container:: inherited

      .. automethod:: Sequence.split_divisions

   .. automethod:: Sequence.stack_intervals

   .. automethod:: Sequence.stack_pitches

   .. automethod:: Sequence.subtract_all

   .. container:: inherited

      .. automethod:: Sequence.sum

   .. container:: inherited

      .. automethod:: Sequence.sum_by_sign

   .. automethod:: Sequence.transpose

   .. container:: inherited

      .. automethod:: Sequence.truncate

   .. automethod:: Sequence.warp

   .. container:: inherited

      .. automethod:: Sequence.weight

   .. container:: inherited

      .. automethod:: Sequence.zip

   .. automethod:: Sequence.zipped_bifurcation

   .. raw:: html

      <hr/>

   .. rubric:: Class & static methods
      :class: class-header

   .. automethod:: Sequence.chen

   .. automethod:: Sequence.e_bonacci_cycle

   .. automethod:: Sequence.e_dovan_cycle

   .. automethod:: Sequence.feigenbaum_bifurcations

   .. automethod:: Sequence.henon

   .. automethod:: Sequence.lindenmayer

   .. automethod:: Sequence.lorenz

   .. automethod:: Sequence.lu_chen

   .. automethod:: Sequence.mandelbrot_set

   .. automethod:: Sequence.markov

   .. automethod:: Sequence.n_bonacci_cycle

   .. automethod:: Sequence.orbits

   .. automethod:: Sequence.prime_sequence

   .. automethod:: Sequence.ratio

   .. automethod:: Sequence.roessler

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: Sequence.items

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~cyc
   ~flatten
   ~julia_set

.. autofunction:: cyc

.. autofunction:: flatten

.. autofunction:: julia_set