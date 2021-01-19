Perllan API
===========

.. toctree::
   :hidden:

   abjadext/index
   evans/index
   tsmakers/index

.. raw:: html

   <hr/>

.. rubric:: :ref:`abjadext <abjadext>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: :ref:`abjadext.microtones <abjadext--microtones>`
   :class: section-header

Abjad's microtonal extension.

.. raw:: html

   <hr/>

.. rubric:: :ref:`abjadext.microtones.et <abjadext--microtones--et>`
   :class: section-header

Package for equal tempered microtones.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~abjadext.microtones.et.ETBundle

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~abjadext.microtones.et.apply_alteration
   ~abjadext.microtones.et.get_accidental_value
   ~abjadext.microtones.et.get_alteration
   ~abjadext.microtones.et.get_value_sum

.. raw:: html

   <hr/>

.. rubric:: :ref:`abjadext.microtones.ji <abjadext--microtones--ji>`
   :class: section-header

Package for Just Intonation.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~abjadext.microtones.ji.JIBundle
   ~abjadext.microtones.ji.JIVector

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~abjadext.microtones.ji.make_ji_bundle
   ~abjadext.microtones.ji.return_cent_deviation_markup
   ~abjadext.microtones.ji.tune_to_ratio

.. raw:: html

   <hr/>

.. rubric:: :ref:`abjadext.microtones.utilities <abjadext--microtones--utilities>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~abjadext.microtones.utilities.PitchClassSegment
   ~abjadext.microtones.utilities.PitchClassSet
   ~abjadext.microtones.utilities.PitchSegment
   ~abjadext.microtones.utilities.PitchSet
   ~abjadext.microtones.utilities.RatioClassSegment
   ~abjadext.microtones.utilities.RatioClassSet
   ~abjadext.microtones.utilities.RatioSegment
   ~abjadext.microtones.utilities.RatioSet

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans <evans>`
   :class: section-header

Evans API

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.commands <evans--commands>`
   :class: section-header

Command classes.

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
   ~evans.commands.duplicate
   ~evans.commands.replace

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.consort <evans--consort>`
   :class: section-header

A port of a variety of tools from Josiah Wolf Oberholtzer's ``Consort`` to
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

Handler classes.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.handlers.ArticulationHandler
   ~evans.handlers.BendHandler
   ~evans.handlers.BisbigliandoHandler
   ~evans.handlers.BowAngleHandler
   ~evans.handlers.ClefHandler
   ~evans.handlers.CompositeHandler
   ~evans.handlers.DynamicHandler
   ~evans.handlers.GettatoHandler
   ~evans.handlers.GlissandoHandler
   ~evans.handlers.GraceHandler
   ~evans.handlers.Handler
   ~evans.handlers.IntermittentVoiceHandler
   ~evans.handlers.NoteheadHandler
   ~evans.handlers.OnBeatGraceHandler
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

Metric modulation.

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.metmod.calculate_metric_modulation
   ~evans.metmod.calculate_tempo_modulated_duration
   ~evans.metmod.compare_speed
   ~evans.metmod.metric_modulation
   ~evans.metmod.mixed_number

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.pitch <evans--pitch>`
   :class: section-header

Pitch functions.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.pitch.JIPitch

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.pitch.combination_tones
   ~evans.pitch.herz_combination_tone_ratios
   ~evans.pitch.return_cent_markup
   ~evans.pitch.return_vertical_moment_ties
   ~evans.pitch.to_nearest_eighth_tone
   ~evans.pitch.to_nearest_quarter_tone
   ~evans.pitch.to_nearest_sixth_tone
   ~evans.pitch.to_nearest_third_tone
   ~evans.pitch.to_nearest_twelfth_tone
   ~evans.pitch.tonnetz
   ~evans.pitch.tune_to_ratio

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.rtm <evans--rtm>`
   :class: section-header

Rhythm tree functions.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.rtm.RhythmTreeQuantizer

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.rtm.flatten_tree_level
   ~evans.rtm.funnel_inner_tree_to_x
   ~evans.rtm.funnel_tree_to_x
   ~evans.rtm.nested_list_to_rtm
   ~evans.rtm.rotate_tree

.. raw:: html

   <hr/>

.. rubric:: Rhythm-makers
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.rtm.RTMMaker

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.segmentmaker <evans--segmentmaker>`
   :class: section-header

SegmentMaker with supporting classes and functions.

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

Sequence classes and functions.

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.sequence.CyclicList
   ~evans.sequence.MarkovChain
   ~evans.sequence.PitchClassSegment
   ~evans.sequence.PitchClassSet
   ~evans.sequence.PitchSegment
   ~evans.sequence.PitchSet
   ~evans.sequence.Ratio
   ~evans.sequence.RatioClassSegment
   ~evans.sequence.RatioClassSet
   ~evans.sequence.RatioSegment
   ~evans.sequence.RatioSet
   ~evans.sequence.Sequence

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.sequence.cyc
   ~evans.sequence.flatten
   ~evans.sequence.julia_set

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.spanners <evans--spanners>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.spanners.BowAnglePoint
   ~evans.spanners.Damping
   ~evans.spanners.DampingComponent

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~evans.spanners.bow_angle_spanner

.. raw:: html

   <hr/>

.. rubric:: :ref:`evans.timespan <evans--timespan>`
   :class: section-header

Timespan classes and functions.

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

.. raw:: html

   <hr/>

.. rubric:: :ref:`tsmakers <tsmakers>`
   :class: section-header

Timespan Makers

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~tsmakers.BoundaryTimespanMaker.BoundaryTimespanMaker
   ~tsmakers.CascadingTimespanMaker.CascadingTimespanMaker
   ~tsmakers.CompositeMusicSpecifier.CompositeMusicSpecifier
   ~tsmakers.Cursor.Cursor
   ~tsmakers.DependentTimespanMaker.DependentTimespanMaker
   ~tsmakers.FloodedTimespanMaker.FloodedTimespanMaker
   ~tsmakers.HashCachingObject.HashCachingObject
   ~tsmakers.MusicSpecifier.MusicSpecifier
   ~tsmakers.MusicSpecifierSequence.MusicSpecifierSequence
   ~tsmakers.TaleaTimespanMaker.TaleaTimespanMaker
   ~tsmakers.TimespanMaker.TimespanMaker
   ~tsmakers.TimespanSpecifier.TimespanSpecifier

.. raw:: html

   <hr/>

.. rubric:: Timespans
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~tsmakers.PerformedTimespan.PerformedTimespan
   ~tsmakers.SilentTimespan.SilentTimespan

.. raw:: html

   <hr/>

.. rubric:: :ref:`tsmakers.tree <tsmakers--tree>`
   :class: section-header

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~tsmakers.tree.TimespanTree
   ~tsmakers.tree.TimespanTreeNode

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: subsection-header

.. autosummary::
   :nosignatures:

   ~tsmakers.tree.divrewrite
   ~tsmakers.tree.flatten
   ~tsmakers.tree.levelbylevel
   ~tsmakers.tree.levelorder
   ~tsmakers.tree.tally