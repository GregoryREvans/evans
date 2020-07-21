.. _tsmakers--tree:

tree
====

.. automodule:: tsmakers.tree

.. currentmodule:: tsmakers.tree

.. container:: svg-container

   .. inheritance-diagram:: tsmakers
      :lineage: tsmakers.tree

.. raw:: html

   <hr/>

.. rubric:: Classes
   :class: section-header

.. autosummary::
   :nosignatures:

   ~TimespanTree
   ~TimespanTreeNode

.. autoclass:: TimespanTree

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      get_level
      get_level_order
      get_level_order_value
      get_level_value
      replace_values
      show
      show_level
      tspanlist
      tspanlist_level

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: TimespanTree.get_level

   .. automethod:: TimespanTree.get_level_order

   .. automethod:: TimespanTree.get_level_order_value

   .. automethod:: TimespanTree.get_level_value

   .. automethod:: TimespanTree.replace_values

   .. automethod:: TimespanTree.show

   .. automethod:: TimespanTree.show_level

   .. automethod:: TimespanTree.tspanlist

   .. automethod:: TimespanTree.tspanlist_level

.. autoclass:: TimespanTreeNode

   .. raw:: html

      <hr/>

   .. rubric:: Attributes Summary
      :class: class-header

   .. autosummary::
      :nosignatures:

      find_root
      get_children
      get_childrensum
      get_fract_value
      get_number_of_children
      get_parent
      get_real_value
      get_timespan
      insert_child
      localoffset
      offset

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: TimespanTreeNode.find_root

   .. automethod:: TimespanTreeNode.get_children

   .. automethod:: TimespanTreeNode.get_childrensum

   .. automethod:: TimespanTreeNode.get_fract_value

   .. automethod:: TimespanTreeNode.get_number_of_children

   .. automethod:: TimespanTreeNode.get_parent

   .. automethod:: TimespanTreeNode.get_real_value

   .. automethod:: TimespanTreeNode.get_timespan

   .. automethod:: TimespanTreeNode.insert_child

   .. automethod:: TimespanTreeNode.localoffset

   .. automethod:: TimespanTreeNode.offset

.. raw:: html

   <hr/>

.. rubric:: Functions
   :class: section-header

.. autosummary::
   :nosignatures:

   ~divrewrite
   ~flatten
   ~levelbylevel
   ~levelorder
   ~tally

.. autofunction:: divrewrite

.. autofunction:: flatten

.. autofunction:: levelbylevel

.. autofunction:: levelorder

.. autofunction:: tally