Evans API
=========

.. toctree::
   :hidden:

   evans/index

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans <evans>`
   :class: section-header

Evans API

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.commands <evans--commands>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.commands.Command
   ~evans.commands.HandlerCommand
   ~evans.commands.RhythmCommand

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.commands.attach
   ~evans.commands.call
   ~evans.commands.detach
   ~evans.commands.replace

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.consort <evans--consort>`
   :class: section-header

A port of a variety of tools from ``Consort`` by Josiah Wolf Oberholtzer to
`Abjad 3.1`.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.consort.AbjadObject.AbjadObject
   ~evans.consort.AbjadValueObject.AbjadValueObject
   ~evans.consort.LogicalTieCollection.LogicalTieCollection
   ~evans.consort.RatioPartsExpression.RatioPartsExpression
   ~evans.consort.TimespanCollection.TimespanCollection
   ~evans.consort.TimespanCollectionNode.TimespanCollectionNode
   ~evans.consort.TimespanSimultaneity.TimespanSimultaneity

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.consort.iterate_nwise.iterate_nwise
   ~evans.consort.rotate.rotate

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.handlers <evans--handlers>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.handlers.ArticulationHandler
   ~evans.handlers.BendHandler
   ~evans.handlers.BisbigliandoHandler
   ~evans.handlers.ClefHandler
   ~evans.handlers.DynamicHandler
   ~evans.handlers.GettatoHandler
   ~evans.handlers.GlissandoHandler
   ~evans.handlers.GraceHandler
   ~evans.handlers.Handler
   ~evans.handlers.NoteheadHandler
   ~evans.handlers.PitchHandler
   ~evans.handlers.RhythmHandler
   ~evans.handlers.SlurHandler
   ~evans.handlers.TempoSpannerHandler
   ~evans.handlers.TextSpanHandler
   ~evans.handlers.TrillHandler

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.metmod <evans--metmod>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.metmod.calculate_metric_modulation
   ~evans.metmod.compare_speed
   ~evans.metmod.metric_modulation
   ~evans.metmod.mixed_number

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.pitch <evans--pitch>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.pitch.combination_tones
   ~evans.pitch.herz_combination_tone_ratios
   ~evans.pitch.return_vertical_moment_ties
   ~evans.pitch.to_nearest_eighth_tone
   ~evans.pitch.to_nearest_quarter_tone
   ~evans.pitch.to_nearest_sixth_tone
   ~evans.pitch.to_nearest_third_tone
   ~evans.pitch.to_nearest_twelfth_tone

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.rtm <evans--rtm>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.rtm.RTMMaker

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.rtm.funnel_inner_tree_to_x
   ~evans.rtm.funnel_tree_to_x
   ~evans.rtm.nested_list_to_rtm
   ~evans.rtm.rotate_tree

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.segmentmaker <evans--segmentmaker>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.segmentmaker.NoteheadBracketMaker
   ~evans.segmentmaker.SegmentMaker

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.segmentmaker.beam_meter

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.sequence <evans--sequence>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.sequence.CyclicList
   ~evans.sequence.MarkovChain

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.sequence.add_sequences
   ~evans.sequence.cyc
   ~evans.sequence.derive_added_sequences
   ~evans.sequence.derive_multiplied_sequences
   ~evans.sequence.e_bonacci_cycle
   ~evans.sequence.e_dovan_cycle
   ~evans.sequence.feigenbaum_bifurcations
   ~evans.sequence.flatten
   ~evans.sequence.grouper
   ~evans.sequence.guerrero_morales
   ~evans.sequence.harmonic_series
   ~evans.sequence.hexagonal_sequence
   ~evans.sequence.josephus
   ~evans.sequence.lindenmayer
   ~evans.sequence.mirror
   ~evans.sequence.mod
   ~evans.sequence.multiple_sequence
   ~evans.sequence.multiply_sequences
   ~evans.sequence.n_bonacci_cycle
   ~evans.sequence.normalize_sum
   ~evans.sequence.normalize_to_indices
   ~evans.sequence.orbits
   ~evans.sequence.perm
   ~evans.sequence.pitch_warp
   ~evans.sequence.prime_sequence
   ~evans.sequence.prism_sequence
   ~evans.sequence.random_walk
   ~evans.sequence.recaman_sequence
   ~evans.sequence.reciprocal
   ~evans.sequence.reduce_mod
   ~evans.sequence.reproportion_chord
   ~evans.sequence.reproportion_chromatic_decimals
   ~evans.sequence.reproportion_harmonics
   ~evans.sequence.reproportion_scale
   ~evans.sequence.rotate
   ~evans.sequence.warp

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.timespan <evans--timespan>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.timespan.TimespanMaker
   ~evans.timespan.TimespanSpecifier

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.timespan.add_silences_to_timespan_dict
   ~evans.timespan.add_silences_to_timespan_lists
   ~evans.timespan.add_silent_timespans
   ~evans.timespan.collect_offsets
   ~evans.timespan.human_sorted_keys
   ~evans.timespan.intercalate_silences
   ~evans.timespan.make_showable_list
   ~evans.timespan.make_split_list
   ~evans.timespan.sorted_keys
   ~evans.timespan.talea_timespans
   ~evans.timespan.to_digit

.. raw:: html

   <hr/>

.. rubric:: Timespans
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.timespan.SilentTimespan