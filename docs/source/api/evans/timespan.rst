.. _evans--timespan:

timespan
========

.. automodule:: evans.timespan

.. currentmodule:: evans.timespan

.. container:: svg-container

   .. inheritance-diagram:: evans
      :lineage: evans.timespan

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~TimespanMaker
   ~TimespanSpecifier

.. autoclass:: TimespanMaker

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __call__
      __repr__
      __str__
      denominator
      total_duration

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: TimespanMaker.__call__

   .. automethod:: TimespanMaker.__repr__

   .. automethod:: TimespanMaker.__str__

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: TimespanMaker.denominator

   .. autoattribute:: TimespanMaker.total_duration

.. autoclass:: TimespanSpecifier

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

   .. automethod:: TimespanSpecifier.__repr__

   .. automethod:: TimespanSpecifier.__str__

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~add_silences_to_timespan_dict
   ~add_silences_to_timespan_lists
   ~add_silent_timespans
   ~collect_offsets
   ~human_sorted_keys
   ~intercalate_silences
   ~make_showable_list
   ~make_split_list
   ~sorted_keys
   ~talea_timespans
   ~to_digit

.. autofunction:: add_silences_to_timespan_dict

.. autofunction:: add_silences_to_timespan_lists

.. autofunction:: add_silent_timespans

.. autofunction:: collect_offsets

.. autofunction:: human_sorted_keys

.. autofunction:: intercalate_silences

.. autofunction:: make_showable_list

.. autofunction:: make_split_list

.. autofunction:: sorted_keys

.. autofunction:: talea_timespans

.. autofunction:: to_digit

.. raw:: html

   <hr/>

.. rubric:: Timespans
   :class: section-header

.. autosummary::
   :nosignatures:

   ~SilentTimespan

.. autoclass:: SilentTimespan

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

   .. container:: inherited

      .. autoattribute:: SilentTimespan.offsets

   .. container:: inherited

      .. autoattribute:: SilentTimespan.start_offset

   .. container:: inherited

      .. autoattribute:: SilentTimespan.stop_offset

   .. container:: inherited

      .. autoattribute:: SilentTimespan.wellformed