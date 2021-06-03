.. _evans--segmentmaker:

segmentmaker
============

.. automodule:: evans.segmentmaker

.. currentmodule:: evans.segmentmaker

.. container:: svg-container

   .. inheritance-diagram:: evans
      :lineage: evans.segmentmaker

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~NoteheadBracketMaker
   ~SegmentMaker

.. autoclass:: NoteheadBracketMaker

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

   .. automethod:: NoteheadBracketMaker.__call__

   .. automethod:: NoteheadBracketMaker.__repr__

   .. automethod:: NoteheadBracketMaker.__str__

.. autoclass:: SegmentMaker

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __repr__
      __str__
      beam_score
      beaming
      build_segment
      call_handlers
      rewrite_meter
      transform_brackets

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SegmentMaker.__repr__

   .. automethod:: SegmentMaker.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: SegmentMaker.beam_score

   .. automethod:: SegmentMaker.build_segment

   .. automethod:: SegmentMaker.call_handlers

   .. automethod:: SegmentMaker.rewrite_meter

   .. automethod:: SegmentMaker.transform_brackets

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~annotate_leaves
   ~beam_meter

.. autofunction:: annotate_leaves

.. autofunction:: beam_meter