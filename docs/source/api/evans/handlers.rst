.. _evans--handlers:

handlers
========

.. automodule:: evans.handlers

.. currentmodule:: evans.handlers

.. container:: svg-container

   .. inheritance-diagram:: evans
      :lineage: evans.handlers

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~ArticulationHandler
   ~BendHandler
   ~BisbigliandoHandler
   ~ClefHandler
   ~DynamicHandler
   ~GettatoHandler
   ~GlissandoHandler
   ~GraceHandler
   ~Handler
   ~NoteheadHandler
   ~PitchHandler
   ~RhythmHandler
   ~SlurHandler
   ~TempoSpannerHandler
   ~TextSpanHandler
   ~TrillHandler

.. autoclass:: ArticulationHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      add_articulations
      identifiers
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: ArticulationHandler.__call__

   .. container:: inherited

      .. automethod:: ArticulationHandler.__repr__

   .. container:: inherited

      .. automethod:: ArticulationHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: ArticulationHandler.add_articulations

   .. automethod:: ArticulationHandler.identifiers

   .. automethod:: ArticulationHandler.name

   .. automethod:: ArticulationHandler.state

.. autoclass:: BendHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      add_bend
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: BendHandler.__call__

   .. container:: inherited

      .. automethod:: BendHandler.__repr__

   .. container:: inherited

      .. automethod:: BendHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: BendHandler.add_bend

   .. automethod:: BendHandler.name

   .. automethod:: BendHandler.state

.. autoclass:: BisbigliandoHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      add_spanner
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: BisbigliandoHandler.__call__

   .. container:: inherited

      .. automethod:: BisbigliandoHandler.__repr__

   .. container:: inherited

      .. automethod:: BisbigliandoHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: BisbigliandoHandler.add_spanner

   .. automethod:: BisbigliandoHandler.name

   .. automethod:: BisbigliandoHandler.state

.. autoclass:: ClefHandler

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

   .. automethod:: ClefHandler.__call__

   .. container:: inherited

      .. automethod:: ClefHandler.__repr__

   .. container:: inherited

      .. automethod:: ClefHandler.__str__

.. autoclass:: DynamicHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: DynamicHandler.__call__

   .. container:: inherited

      .. automethod:: DynamicHandler.__repr__

   .. container:: inherited

      .. automethod:: DynamicHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: DynamicHandler.name

   .. automethod:: DynamicHandler.state

.. autoclass:: GettatoHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      add_gettato
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: GettatoHandler.__call__

   .. container:: inherited

      .. automethod:: GettatoHandler.__repr__

   .. container:: inherited

      .. automethod:: GettatoHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: GettatoHandler.add_gettato

   .. automethod:: GettatoHandler.name

   .. automethod:: GettatoHandler.state

.. autoclass:: GlissandoHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      add_glissando
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: GlissandoHandler.__call__

   .. container:: inherited

      .. automethod:: GlissandoHandler.__repr__

   .. container:: inherited

      .. automethod:: GlissandoHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: GlissandoHandler.add_glissando

   .. automethod:: GlissandoHandler.name

   .. automethod:: GlissandoHandler.state

.. autoclass:: GraceHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: GraceHandler.__call__

   .. container:: inherited

      .. automethod:: GraceHandler.__repr__

   .. container:: inherited

      .. automethod:: GraceHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: GraceHandler.name

   .. automethod:: GraceHandler.state

.. autoclass:: Handler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __repr__
      __str__

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: Handler.__repr__

   .. automethod:: Handler.__str__

.. autoclass:: NoteheadHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      add_noteheads
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: NoteheadHandler.__call__

   .. container:: inherited

      .. automethod:: NoteheadHandler.__repr__

   .. container:: inherited

      .. automethod:: NoteheadHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: NoteheadHandler.add_noteheads

   .. automethod:: NoteheadHandler.name

   .. automethod:: NoteheadHandler.state

.. autoclass:: PitchHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: PitchHandler.__call__

   .. container:: inherited

      .. automethod:: PitchHandler.__repr__

   .. container:: inherited

      .. automethod:: PitchHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: PitchHandler.name

   .. automethod:: PitchHandler.state

.. autoclass:: RhythmHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      name
      return_state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: RhythmHandler.__call__

   .. container:: inherited

      .. automethod:: RhythmHandler.__repr__

   .. container:: inherited

      .. automethod:: RhythmHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: RhythmHandler.name

   .. automethod:: RhythmHandler.return_state

.. autoclass:: SlurHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      add_slurs
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: SlurHandler.__call__

   .. container:: inherited

      .. automethod:: SlurHandler.__repr__

   .. container:: inherited

      .. automethod:: SlurHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: SlurHandler.add_slurs

   .. automethod:: SlurHandler.name

   .. automethod:: SlurHandler.state

.. autoclass:: TempoSpannerHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      add_spanner
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: TempoSpannerHandler.__call__

   .. container:: inherited

      .. automethod:: TempoSpannerHandler.__repr__

   .. container:: inherited

      .. automethod:: TempoSpannerHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: TempoSpannerHandler.add_spanner

   .. automethod:: TempoSpannerHandler.name

   .. automethod:: TempoSpannerHandler.state

.. autoclass:: TextSpanHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: TextSpanHandler.__call__

   .. container:: inherited

      .. automethod:: TextSpanHandler.__repr__

   .. container:: inherited

      .. automethod:: TextSpanHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: TextSpanHandler.name

   .. automethod:: TextSpanHandler.state

.. autoclass:: TrillHandler

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      name
      state

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: TrillHandler.__call__

   .. container:: inherited

      .. automethod:: TrillHandler.__repr__

   .. container:: inherited

      .. automethod:: TrillHandler.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: TrillHandler.name

   .. automethod:: TrillHandler.state