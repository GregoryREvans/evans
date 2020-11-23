.. _tsmakers--SilentTimespan:

SilentTimespan
==============

.. automodule:: tsmakers.SilentTimespan

.. currentmodule:: tsmakers.SilentTimespan

.. container:: svg-container

   .. inheritance-diagram:: tsmakers
      :lineage: tsmakers.SilentTimespan

.. autoclass:: SilentTimespan

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __repr__
      __str__
      forbid_fusing
      forbid_splitting
      handler
      is_left_broken
      is_right_broken
      layer
      minimum_duration
      voice_name

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. container:: inherited

      .. automethod:: SilentTimespan.__and__

   .. container:: inherited

      .. automethod:: SilentTimespan.__contains__

   .. container:: inherited

      .. automethod:: SilentTimespan.__eq__

   .. container:: inherited

      .. automethod:: SilentTimespan.__ge__

   .. container:: inherited

      .. automethod:: SilentTimespan.__gt__

   .. container:: inherited

      .. automethod:: SilentTimespan.__hash__

   .. container:: inherited

      .. automethod:: SilentTimespan.__le__

   .. container:: inherited

      .. automethod:: SilentTimespan.__len__

   .. container:: inherited

      .. automethod:: SilentTimespan.__lt__

   .. container:: inherited

      .. automethod:: SilentTimespan.__or__

   .. automethod:: SilentTimespan.__repr__

   .. automethod:: SilentTimespan.__str__

   .. container:: inherited

      .. automethod:: SilentTimespan.__sub__

   .. container:: inherited

      .. automethod:: SilentTimespan.__xor__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. container:: inherited

      .. automethod:: SilentTimespan.contains_timespan_improperly

   .. container:: inherited

      .. automethod:: SilentTimespan.curtails_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.delays_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.divide_by_ratio

   .. container:: inherited

      .. automethod:: SilentTimespan.get_overlap_with_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.happens_during_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.intersects_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.is_congruent_to_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.is_tangent_to_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.overlaps_all_of_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.overlaps_only_start_of_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.overlaps_only_stop_of_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.overlaps_start_of_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.overlaps_stop_of_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.reflect

   .. container:: inherited

      .. automethod:: SilentTimespan.round_offsets

   .. container:: inherited

      .. automethod:: SilentTimespan.scale

   .. container:: inherited

      .. automethod:: SilentTimespan.set_duration

   .. container:: inherited

      .. automethod:: SilentTimespan.set_offsets

   .. container:: inherited

      .. automethod:: SilentTimespan.split_at_offset

   .. container:: inherited

      .. automethod:: SilentTimespan.split_at_offsets

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_after_offset

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_after_timespan_starts

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_after_timespan_stops

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_at_offset

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_at_or_after_offset

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_before_offset

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_before_or_at_offset

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_before_timespan_starts

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_before_timespan_stops

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_during_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_when_timespan_starts

   .. container:: inherited

      .. automethod:: SilentTimespan.starts_when_timespan_stops

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_after_offset

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_after_timespan_starts

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_after_timespan_stops

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_at_offset

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_at_or_after_offset

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_before_offset

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_before_or_at_offset

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_before_timespan_starts

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_before_timespan_stops

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_during_timespan

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_when_timespan_starts

   .. container:: inherited

      .. automethod:: SilentTimespan.stops_when_timespan_stops

   .. container:: inherited

      .. automethod:: SilentTimespan.stretch

   .. container:: inherited

      .. automethod:: SilentTimespan.translate

   .. container:: inherited

      .. automethod:: SilentTimespan.translate_offsets

   .. container:: inherited

      .. automethod:: SilentTimespan.trisects_timespan

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. container:: inherited

      .. autoattribute:: SilentTimespan.axis

   .. container:: inherited

      .. autoattribute:: SilentTimespan.duration

   .. autoattribute:: SilentTimespan.forbid_fusing

   .. autoattribute:: SilentTimespan.forbid_splitting

   .. autoattribute:: SilentTimespan.handler

   .. autoattribute:: SilentTimespan.is_left_broken

   .. autoattribute:: SilentTimespan.is_right_broken

   .. autoattribute:: SilentTimespan.layer

   .. autoattribute:: SilentTimespan.minimum_duration

   .. container:: inherited

      .. autoattribute:: SilentTimespan.offsets

   .. container:: inherited

      .. autoattribute:: SilentTimespan.start_offset

   .. container:: inherited

      .. autoattribute:: SilentTimespan.stop_offset

   .. autoattribute:: SilentTimespan.voice_name

   .. container:: inherited

      .. autoattribute:: SilentTimespan.wellformed