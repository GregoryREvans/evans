.. _evans--spanners:

spanners
========

.. automodule:: evans.spanners

.. currentmodule:: evans.spanners

.. container:: svg-container

   .. inheritance-diagram:: evans
      :lineage: evans.spanners

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~BowAnglePoint
   ~Damping
   ~DampingComponent

.. autoclass:: BowAnglePoint

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __ge__
      __gt__
      __le__
      __lt__
      __repr__
      __str__
      degrees
      markup

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: BowAnglePoint.__ge__

   .. automethod:: BowAnglePoint.__gt__

   .. automethod:: BowAnglePoint.__le__

   .. automethod:: BowAnglePoint.__lt__

   .. automethod:: BowAnglePoint.__repr__

   .. automethod:: BowAnglePoint.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: BowAnglePoint.degrees

   .. autoattribute:: BowAnglePoint.markup

.. autoclass:: Damping

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __repr__
      __str__
      markup

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Damping.__repr__

   .. automethod:: Damping.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: Damping.markup

.. autoclass:: DampingComponent

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __repr__
      __str__
      char_to_note_head
      length_to_paren_scale
      markup

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: DampingComponent.__repr__

   .. automethod:: DampingComponent.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: DampingComponent.markup

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~bow_angle_spanner

.. autofunction:: bow_angle_spanner