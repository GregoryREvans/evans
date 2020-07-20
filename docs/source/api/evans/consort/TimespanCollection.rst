.. _evans--consort--TimespanCollection:

TimespanCollection
==================

.. automodule:: evans.consort.TimespanCollection

.. currentmodule:: evans.consort.TimespanCollection

.. container:: svg-container

   .. inheritance-diagram:: evans
      :lineage: evans.consort.TimespanCollection

.. autoclass:: TimespanCollection

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      __contains__
      __getitem__
      __iter__
      __len__
      __setitem__
      __sub__
      all_offsets
      all_start_offsets
      all_stop_offsets
      earliest_start_offset
      earliest_stop_offset
      find_timespans_intersecting_timespan
      find_timespans_overlapping_offset
      find_timespans_starting_at
      find_timespans_stopping_at
      get_simultaneity_at
      get_start_offset_after
      get_start_offset_before
      index
      insert
      iterate_simultaneities
      iterate_simultaneities_nwise
      latest_start_offset
      latest_stop_offset
      remove
      start_offset
      stop_offset

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: TimespanCollection.__contains__

   .. container:: inherited

      .. automethod:: TimespanCollection.__eq__

   .. container:: inherited

      .. automethod:: TimespanCollection.__format__

   .. automethod:: TimespanCollection.__getitem__

   .. container:: inherited

      .. automethod:: TimespanCollection.__hash__

   .. automethod:: TimespanCollection.__iter__

   .. automethod:: TimespanCollection.__len__

   .. container:: inherited

      .. automethod:: TimespanCollection.__ne__

   .. container:: inherited

      .. automethod:: TimespanCollection.__repr__

   .. automethod:: TimespanCollection.__setitem__

   .. container:: inherited

      .. automethod:: TimespanCollection.__str__

   .. automethod:: TimespanCollection.__sub__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: TimespanCollection.find_timespans_intersecting_timespan

   .. automethod:: TimespanCollection.find_timespans_overlapping_offset

   .. automethod:: TimespanCollection.find_timespans_starting_at

   .. automethod:: TimespanCollection.find_timespans_stopping_at

   .. automethod:: TimespanCollection.get_simultaneity_at

   .. automethod:: TimespanCollection.get_start_offset_after

   .. automethod:: TimespanCollection.get_start_offset_before

   .. automethod:: TimespanCollection.index

   .. automethod:: TimespanCollection.insert

   .. automethod:: TimespanCollection.iterate_simultaneities

   .. automethod:: TimespanCollection.iterate_simultaneities_nwise

   .. automethod:: TimespanCollection.remove

   .. raw:: html

      <hr/>

   .. rubric:: Read-only properties
      :class: class-header

   .. autoattribute:: TimespanCollection.all_offsets

   .. autoattribute:: TimespanCollection.all_start_offsets

   .. autoattribute:: TimespanCollection.all_stop_offsets

   .. autoattribute:: TimespanCollection.earliest_start_offset

   .. autoattribute:: TimespanCollection.earliest_stop_offset

   .. autoattribute:: TimespanCollection.latest_start_offset

   .. autoattribute:: TimespanCollection.latest_stop_offset

   .. autoattribute:: TimespanCollection.start_offset

   .. autoattribute:: TimespanCollection.stop_offset