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

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~add_sequences
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
   ~hexagonal_sequence
   ~josephus
   ~lindenmayer
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
   ~rotate
   ~warp

.. autofunction:: add_sequences

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

.. autofunction:: hexagonal_sequence

.. autofunction:: josephus

.. autofunction:: lindenmayer

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

.. autofunction:: rotate

.. autofunction:: warp