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

      add_sequences
      chen
      derive_added_sequences
      derive_multiplied_sequences
      e_bonacci_cycle
      e_dovan_cycle
      feigenbaum_bifurcations
      grouper
      guerrero_morales
      henon
      hexagonal_sequence
      josephus
      lindenmayer
      lorenz
      lu_chen
      mandelbrot_set
      map_dict
      map_indices
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
      prime_sequence
      prism_sequence
      random_walk
      recaman_sequence
      reciprocals
      reproportion_by_base
      roessler
      rotate
      stack_intervals
      stack_pitches
      transpose
      warp

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

   .. container:: inherited

      .. automethod:: Sequence.boustrophedon

   .. container:: inherited

      .. automethod:: Sequence.count

   .. container:: inherited

      .. automethod:: Sequence.degree_of_rotational_symmetry

   .. automethod:: Sequence.derive_added_sequences

   .. automethod:: Sequence.derive_multiplied_sequences

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

   .. container:: inherited

      .. automethod:: Sequence.map

   .. automethod:: Sequence.map_dict

   .. automethod:: Sequence.map_indices

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

      .. automethod:: Sequence.zebra

   .. container:: inherited

      .. automethod:: Sequence.zip

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

   .. automethod:: Sequence.n_bonacci_cycle

   .. automethod:: Sequence.orbits

   .. automethod:: Sequence.prime_sequence

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