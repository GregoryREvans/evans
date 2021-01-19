.. _evans--rtm:

rtm
===

.. automodule:: evans.rtm

.. currentmodule:: evans.rtm

.. container:: svg-container

   .. inheritance-diagram:: evans
      :lineage: evans.rtm

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~RhythmTreeQuantizer

.. autoclass:: RhythmTreeQuantizer

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: RhythmTreeQuantizer.__call__

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~flatten_tree_level
   ~funnel_inner_tree_to_x
   ~funnel_tree_to_x
   ~nested_list_to_rtm
   ~rotate_tree

.. autofunction:: flatten_tree_level

.. autofunction:: funnel_inner_tree_to_x

.. autofunction:: funnel_tree_to_x

.. autofunction:: nested_list_to_rtm

.. autofunction:: rotate_tree

.. raw:: html

   <hr/>

.. rubric:: Rhythm-makers
   :class: section-header

.. autosummary::
   :nosignatures:

   ~RTMMaker

.. autoclass:: RTMMaker

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __repr__
      __str__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: RTMMaker.__call__

   .. container:: inherited

      .. automethod:: RTMMaker.__eq__

   .. container:: inherited

      .. automethod:: RTMMaker.__hash__

   .. automethod:: RTMMaker.__repr__

   .. automethod:: RTMMaker.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: RTMMaker.previous_state

   .. container:: inherited

      .. autoattribute:: RTMMaker.spelling

   .. container:: inherited

      .. autoattribute:: RTMMaker.state

   .. container:: inherited

      .. autoattribute:: RTMMaker.tag