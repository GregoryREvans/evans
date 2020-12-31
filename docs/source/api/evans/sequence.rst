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
   ~Ratio
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

.. autoclass:: Sequence

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      stack_intervals
      stack_pitches

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

   .. container:: inherited

      .. automethod:: Sequence.boustrophedon

   .. container:: inherited

      .. automethod:: Sequence.count

   .. container:: inherited

      .. automethod:: Sequence.degree_of_rotational_symmetry

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

   .. container:: inherited

      .. automethod:: Sequence.helianthate

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

   .. container:: inherited

      .. automethod:: Sequence.map

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

   .. container:: inherited

      .. automethod:: Sequence.permute

   .. container:: inherited

      .. automethod:: Sequence.quarters

   .. container:: inherited

      .. automethod:: Sequence.ratios

   .. container:: inherited

      .. automethod:: Sequence.remove

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

   .. container:: inherited

      .. automethod:: Sequence.retain

   .. container:: inherited

      .. automethod:: Sequence.retain_pattern

   .. container:: inherited

      .. automethod:: Sequence.reveal

   .. container:: inherited

      .. automethod:: Sequence.reverse

   .. container:: inherited

      .. automethod:: Sequence.rotate

   .. container:: inherited

      .. automethod:: Sequence.sort

   .. container:: inherited

      .. automethod:: Sequence.split

   .. container:: inherited

      .. automethod:: Sequence.split_divisions

   .. automethod:: Sequence.stack_intervals

   .. automethod:: Sequence.stack_pitches

   .. container:: inherited

      .. automethod:: Sequence.sum

   .. container:: inherited

      .. automethod:: Sequence.sum_by_sign

   .. container:: inherited

      .. automethod:: Sequence.truncate

   .. container:: inherited

      .. automethod:: Sequence.weight

   .. container:: inherited

      .. automethod:: Sequence.zebra

   .. container:: inherited

      .. automethod:: Sequence.zip

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

   ~add_sequences
   ~chen
   ~cyc
   ~derive_added_sequences
   ~derive_multiplied_sequences
   ~e_bonacci_cycle
   ~e_dovan_cycle
   ~feigenbaum_bifurcations
   ~flatten
   ~grouper
   ~guerrero_morales
   ~harmonic_series
   ~henon
   ~hexagonal_sequence
   ~josephus
   ~julia_set
   ~lindenmayer
   ~lorenz
   ~lu_chen
   ~mandelbrot_set
   ~mirror
   ~mod
   ~multiple_sequence
   ~multiply_all
   ~multiply_sequences
   ~n_bonacci_cycle
   ~normalize_sum
   ~normalize_to_indices
   ~orbits
   ~perm
   ~pitch_warp
   ~prime_sequence
   ~prism_sequence
   ~random_walk
   ~recaman_sequence
   ~reciprocal
   ~reduce_mod
   ~reproportion_chord
   ~reproportion_chromatic_decimals
   ~reproportion_harmonics
   ~reproportion_scale
   ~roessler
   ~rotate
   ~warp

.. autofunction:: add_sequences

.. autofunction:: chen

.. autofunction:: cyc

.. autofunction:: derive_added_sequences

.. autofunction:: derive_multiplied_sequences

.. autofunction:: e_bonacci_cycle

.. autofunction:: e_dovan_cycle

.. autofunction:: feigenbaum_bifurcations

.. autofunction:: flatten

.. autofunction:: grouper

.. autofunction:: guerrero_morales

.. autofunction:: harmonic_series

.. autofunction:: henon

.. autofunction:: hexagonal_sequence

.. autofunction:: josephus

.. autofunction:: julia_set

.. autofunction:: lindenmayer

.. autofunction:: lorenz

.. autofunction:: lu_chen

.. autofunction:: mandelbrot_set

.. autofunction:: mirror

.. autofunction:: mod

.. autofunction:: multiple_sequence

.. autofunction:: multiply_all

.. autofunction:: multiply_sequences

.. autofunction:: n_bonacci_cycle

.. autofunction:: normalize_sum

.. autofunction:: normalize_to_indices

.. autofunction:: orbits

.. autofunction:: perm

.. autofunction:: pitch_warp

.. autofunction:: prime_sequence

.. autofunction:: prism_sequence

.. autofunction:: random_walk

.. autofunction:: recaman_sequence

.. autofunction:: reciprocal

.. autofunction:: reduce_mod

.. autofunction:: reproportion_chord

.. autofunction:: reproportion_chromatic_decimals

.. autofunction:: reproportion_harmonics

.. autofunction:: reproportion_scale

.. autofunction:: roessler

.. autofunction:: rotate

.. autofunction:: warp