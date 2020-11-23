.. _tsmakers--PerformedTimespan:

PerformedTimespan
=================

.. automodule:: tsmakers.PerformedTimespan

.. currentmodule:: tsmakers.PerformedTimespan

.. container:: svg-container

   .. inheritance-diagram:: tsmakers
      :lineage: tsmakers.PerformedTimespan

.. autoclass:: PerformedTimespan

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __lt__
      __repr__
      __str__
      divisions
      forbid_fusing
      forbid_splitting
      handler
      is_left_broken
      is_right_broken
      layer
      minimum_duration
      music
      music_specifier
      original_start_offset
      original_stop_offset
      split_at_offset
      voice_name

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PerformedTimespan.__and__

   .. container:: inherited

      .. automethod:: PerformedTimespan.__contains__

   .. container:: inherited

      .. automethod:: PerformedTimespan.__eq__

   .. container:: inherited

      .. automethod:: PerformedTimespan.__ge__

   .. container:: inherited

      .. automethod:: PerformedTimespan.__gt__

   .. container:: inherited

      .. automethod:: PerformedTimespan.__hash__

   .. container:: inherited

      .. automethod:: PerformedTimespan.__le__

   .. container:: inherited

      .. automethod:: PerformedTimespan.__len__

   .. automethod:: PerformedTimespan.__lt__

   .. container:: inherited

      .. automethod:: PerformedTimespan.__or__

   .. automethod:: PerformedTimespan.__repr__

   .. automethod:: PerformedTimespan.__str__

   .. container:: inherited

      .. automethod:: PerformedTimespan.__sub__

   .. container:: inherited

      .. automethod:: PerformedTimespan.__xor__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: PerformedTimespan.contains_timespan_improperly

   .. container:: inherited

      .. automethod:: PerformedTimespan.curtails_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.delays_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.divide_by_ratio

   .. container:: inherited

      .. automethod:: PerformedTimespan.get_overlap_with_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.happens_during_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.intersects_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.is_congruent_to_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.is_tangent_to_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.overlaps_all_of_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.overlaps_only_start_of_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.overlaps_only_stop_of_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.overlaps_start_of_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.overlaps_stop_of_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.reflect

   .. container:: inherited

      .. automethod:: PerformedTimespan.round_offsets

   .. container:: inherited

      .. automethod:: PerformedTimespan.scale

   .. container:: inherited

      .. automethod:: PerformedTimespan.set_duration

   .. container:: inherited

      .. automethod:: PerformedTimespan.set_offsets

   .. automethod:: PerformedTimespan.split_at_offset

   .. container:: inherited

      .. automethod:: PerformedTimespan.split_at_offsets

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_after_offset

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_after_timespan_starts

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_after_timespan_stops

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_at_offset

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_at_or_after_offset

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_before_offset

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_before_or_at_offset

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_before_timespan_starts

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_before_timespan_stops

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_during_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_when_timespan_starts

   .. container:: inherited

      .. automethod:: PerformedTimespan.starts_when_timespan_stops

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_after_offset

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_after_timespan_starts

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_after_timespan_stops

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_at_offset

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_at_or_after_offset

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_before_offset

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_before_or_at_offset

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_before_timespan_starts

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_before_timespan_stops

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_during_timespan

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_when_timespan_starts

   .. container:: inherited

      .. automethod:: PerformedTimespan.stops_when_timespan_stops

   .. container:: inherited

      .. automethod:: PerformedTimespan.stretch

   .. container:: inherited

      .. automethod:: PerformedTimespan.translate

   .. container:: inherited

      .. automethod:: PerformedTimespan.translate_offsets

   .. container:: inherited

      .. automethod:: PerformedTimespan.trisects_timespan

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: PerformedTimespan.axis

   .. autoattribute:: PerformedTimespan.divisions

   .. container:: inherited

      .. autoattribute:: PerformedTimespan.duration

   .. autoattribute:: PerformedTimespan.forbid_fusing

   .. autoattribute:: PerformedTimespan.forbid_splitting

   .. autoattribute:: PerformedTimespan.handler

   .. autoattribute:: PerformedTimespan.is_left_broken

   .. autoattribute:: PerformedTimespan.is_right_broken

   .. autoattribute:: PerformedTimespan.layer

   .. autoattribute:: PerformedTimespan.minimum_duration

   .. autoattribute:: PerformedTimespan.music

   .. autoattribute:: PerformedTimespan.music_specifier

   .. container:: inherited

      .. autoattribute:: PerformedTimespan.offsets

   .. autoattribute:: PerformedTimespan.original_start_offset

   .. autoattribute:: PerformedTimespan.original_stop_offset

   .. container:: inherited

      .. autoattribute:: PerformedTimespan.start_offset

   .. container:: inherited

      .. autoattribute:: PerformedTimespan.stop_offset

   .. autoattribute:: PerformedTimespan.voice_name

   .. container:: inherited

      .. autoattribute:: PerformedTimespan.wellformed