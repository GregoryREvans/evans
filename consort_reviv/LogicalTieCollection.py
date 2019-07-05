from evans.consort_reviv.AbjadObject import AbjadObject
from abjad import system
from abjad.top.inspect import inspect


class LogicalTieCollection(AbjadObject):
    r"""A mutable always-sorted collection of logical_ties.

    ::

        >>> logical_ties = (
        ...     abjad.LogicalTie(0, 3),
        ...     abjad.LogicalTie(1, 3),
        ...     abjad.LogicalTie(1, 2),
        ...     abjad.LogicalTie(2, 5),
        ...     abjad.LogicalTie(6, 9),
        ...     )
        >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_root_node",)

    ### INITIALIZER ###

    def __init__(self, logical_ties=None):
        self._root_node = None
        if logical_ties is not None and logical_ties:
            self.insert(logical_ties)

    ### SPECIAL METHODS ###

    def __contains__(self, logical_tie):
        r"""Is true if this logical_tie collection contains `logical_tie`. Otherwise
        false.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> logical_ties[0] in logical_tie_collection
            True

        ::

            >>> abjad.LogicalTie(-1, 100) in logical_tie_collection
            False

        Returns boolean.
        """
        assert LogicalTieCollection._is_logical_tie(logical_tie)
        candidates = self.find_logical_ties_starting_at(
            inspect(logical_tie).timespan().start_offset
        )
        result = logical_tie in candidates
        return result

    def __getitem__(self, i):
        r"""Gets logical_tie at index `i`.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> logical_tie_collection[-1]
            LogicalTie(start_offset=Offset(6, 1), stop_offset=Offset(9, 1))

        ::

            >>> for logical_tie in logical_tie_collection[:3]:
            ...     logical_tie
            ...
            LogicalTie(start_offset=Offset(0, 1), stop_offset=Offset(3, 1))
            LogicalTie(start_offset=Offset(1, 1), stop_offset=Offset(2, 1))
            LogicalTie(start_offset=Offset(1, 1), stop_offset=Offset(3, 1))

        Returns logical_tie or logical_ties.
        """

        def recurse_by_index(node, index):
            if node.node_start_index <= index < node.node_stop_index:
                return node.payload[index - node.node_start_index]
            elif node.left_child and index < node.node_start_index:
                return recurse_by_index(node.left_child, index)
            elif node.right_child and node.node_stop_index <= index:
                return recurse_by_index(node.right_child, index)

        def recurse_by_slice(node, start, stop):
            result = []
            if node is None:
                return result
            if start < node.node_start_index and node.left_child:
                result.extend(recurse_by_slice(node.left_child, start, stop))
            if start < node.node_stop_index and node.node_start_index < stop:
                node_start = start - node.node_start_index
                if node_start < 0:
                    node_start = 0
                node_stop = stop - node.node_start_index
                result.extend(node.payload[node_start:node_stop])
            if node.node_stop_index <= stop and node.right_child:
                result.extend(recurse_by_slice(node.right_child, start, stop))
            return result

        if isinstance(i, int):
            if self._root_node is None:
                raise IndexError
            if i < 0:
                i = self._root_node.subtree_stop_index + i
            if i < 0 or self._root_node.subtree_stop_index <= i:
                raise IndexError
            return recurse_by_index(self._root_node, i)
        elif isinstance(i, slice):
            if self._root_node is None:
                return []
            indices = i.indices(self._root_node.subtree_stop_index)
            start, stop = indices[0], indices[1]
            return recurse_by_slice(self._root_node, start, stop)

        raise TypeError("Indices must be integers or slices, got {}".format(i))

    def __iter__(self):
        r"""Iterates logical_ties in this logical_tie collection.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> for logical_tie in logical_tie_collection:
            ...     logical_tie
            ...
            LogicalTie(start_offset=Offset(0, 1), stop_offset=Offset(3, 1))
            LogicalTie(start_offset=Offset(1, 1), stop_offset=Offset(2, 1))
            LogicalTie(start_offset=Offset(1, 1), stop_offset=Offset(3, 1))
            LogicalTie(start_offset=Offset(2, 1), stop_offset=Offset(5, 1))
            LogicalTie(start_offset=Offset(6, 1), stop_offset=Offset(9, 1))

        Returns generator.
        """

        def recurse(node):
            if node is not None:
                if node.left_child is not None:
                    for logical_tie in recurse(node.left_child):
                        yield logical_tie
                for logical_tie in node.payload:
                    yield logical_tie
                if node.right_child is not None:
                    for logical_tie in recurse(node.right_child):
                        yield logical_tie

        return recurse(self._root_node)

    def __len__(self):
        r"""Gets length of this logical_tie collection.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> len(logical_tie_collection)
            5

        Returns integer.
        """
        if self._root_node is None:
            return 0
        return self._root_node.subtree_stop_index

    def __setitem__(self, i, new):
        r"""Sets logical_ties at index `i` to `new`.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> logical_tie_collection[:3] = [abjad.LogicalTie(100, 200)]

        Returns none.
        """
        if isinstance(i, (int, slice)):
            old = self[i]
            self.remove(old)
            self.insert(new)
        else:
            message = "Indices must be ints or slices, got {}".format(i)
            raise TypeError(message)

    def __sub__(self, timespan):
        r"""Delete material that intersects `timespan`:

        ::

            >>> logical_tie_collection = consort.LogicalTieCollection([
            ...     abjad.LogicalTie(0, 16),
            ...     abjad.LogicalTie(5, 12),
            ...     abjad.LogicalTie(-2, 8),
            ...     ])

        ::

            >>> timespan = abjad.Timespan(5, 10)
            >>> result = logical_tie_collection - timespan

        ::

            >>> print(format(logical_tie_collection))
            consort.tools.LogicalTieCollection(
                [
                    abjad.LogicalTie(
                        start_offset=abjad.Offset(-2, 1),
                        stop_offset=abjad.Offset(5, 1),
                        ),
                    abjad.LogicalTie(
                        start_offset=abjad.Offset(0, 1),
                        stop_offset=abjad.Offset(5, 1),
                        ),
                    abjad.LogicalTie(
                        start_offset=abjad.Offset(10, 1),
                        stop_offset=abjad.Offset(12, 1),
                        ),
                    abjad.LogicalTie(
                        start_offset=abjad.Offset(10, 1),
                        stop_offset=abjad.Offset(16, 1),
                        ),
                    ]
                )

        Operates in place and returns logical_tie collection.
        """
        intersecting_logical_ties = self.find_logical_ties_intersecting_timespan(
            timespan
        )
        self.remove(intersecting_logical_ties)
        for intersecting_logical_tie in intersecting_logical_ties:
            for x in intersecting_logical_tie - timespan:
                self.insert(x)
        return self

    ### PRIVATE METHODS ###

    def _insert_node(self, node, start_offset):
        from evans.consort_reviv.TimespanCollectionNode import TimespanCollectionNode

        if node is None:
            return TimespanCollectionNode(start_offset)
        if start_offset < node.start_offset:
            node.left_child = self._insert_node(node.left_child, start_offset)
        elif node.start_offset < start_offset:
            node.right_child = self._insert_node(node.right_child, start_offset)
        return self._rebalance(node)

    def _insert_logical_tie(self, logical_tie):
        self._root_node = self._insert_node(
            self._root_node, inspect(logical_tie).timespan().start_offset
        )
        node = self._search(
            self._root_node, inspect(logical_tie).timespan().start_offset
        )
        node.payload.append(logical_tie)
        node.payload.sort(key=lambda x: inspect(x).timespan().stop_offset)

    @staticmethod
    def _is_logical_tie(expr):
        if inspect(expr).timespan() is not None:
            return True
        return False

    def _rebalance(self, node):
        if node is not None:
            if 1 < node.balance:
                if 0 <= node.right_child.balance:
                    node = self._rotate_right_right(node)
                else:
                    node = self._rotate_right_left(node)
            elif node.balance < -1:
                if node.left_child.balance <= 0:
                    node = self._rotate_left_left(node)
                else:
                    node = self._rotate_left_right(node)
            assert -1 <= node.balance <= 1
        return node

    def _remove_node(self, node, start_offset):
        if node is not None:
            if node.start_offset == start_offset:
                if node.left_child and node.right_child:
                    next_node = node.right_child
                    while next_node.left_child:
                        next_node = next_node.left_child
                    node._start_offset = next_node._start_offset
                    node._payload = next_node._payload
                    node.right_child = self._remove_node(
                        node.right_child, next_node.start_offset
                    )
                else:
                    node = node.left_child or node.right_child
            elif start_offset < node.start_offset:
                node.left_child = self._remove_node(node.left_child, start_offset)
            elif node.start_offset < start_offset:
                node.right_child = self._remove_node(node.right_child, start_offset)
        return self._rebalance(node)

    def _remove_logical_tie(self, logical_tie, old_start_offset=None):
        start_offset = inspect(logical_tie).timespan().start_offset
        if old_start_offset is not None:
            start_offset = old_start_offset
        node = self._search(self._root_node, start_offset)
        if node is None:
            return
        if logical_tie in node.payload:
            node.payload.remove(logical_tie)
        if not node.payload:
            self._root_node = self._remove_node(self._root_node, start_offset)
        if isinstance(logical_tie, LogicalTieCollection):
            logical_tie._parents.remove(self)

    def _rotate_left_left(self, node):
        next_node = node.left_child
        node.left_child = next_node.right_child
        next_node.right_child = node
        return next_node

    def _rotate_left_right(self, node):
        node.left_child = self._rotate_right_right(node.left_child)
        next_node = self._rotate_left_left(node)
        return next_node

    def _rotate_right_left(self, node):
        node.right_child = self._rotate_left_left(node.right_child)
        next_node = self._rotate_right_right(node)
        return next_node

    def _rotate_right_right(self, node):
        next_node = node.right_child
        node.right_child = next_node.left_child
        next_node.left_child = node
        return next_node

    def _search(self, node, start_offset):
        if node is not None:
            if node.start_offset == start_offset:
                return node
            elif node.left_child and start_offset < node.start_offset:
                return self._search(node.left_child, start_offset)
            elif node.right_child and node.start_offset < start_offset:
                return self._search(node.right_child, start_offset)
        return None

    def _update_indices(self, node):
        def recurse(node, parent_stop_index=None):
            if node is None:
                return
            if node.left_child is not None:
                recurse(node.left_child, parent_stop_index=parent_stop_index)
                node._node_start_index = node.left_child.subtree_stop_index
                node._subtree_start_index = node.left_child.subtree_start_index
            elif parent_stop_index is None:
                node._node_start_index = 0
                node._subtree_start_index = 0
            else:
                node._node_start_index = parent_stop_index
                node._subtree_start_index = parent_stop_index
            node._node_stop_index = node.node_start_index + len(node.payload)
            node._subtree_stop_index = node.node_stop_index
            if node.right_child is not None:
                recurse(node.right_child, parent_stop_index=node.node_stop_index)
                node._subtree_stop_index = node.right_child.subtree_stop_index

        recurse(node)

    def _update_offsets(self, node):
        if node is None:
            return
        stop_offset_low = min(inspect(x).timespan().stop_offset for x in node.payload)
        stop_offset_high = max(inspect(x).timespan().stop_offset for x in node.payload)
        if node.left_child:
            left_child = self._update_offsets(node.left_child)
            if left_child.stop_offset_low < stop_offset_low:
                stop_offset_low = left_child.stop_offset_low
            if stop_offset_high < left_child.stop_offset_high:
                stop_offset_high = left_child.stop_offset_high
        if node.right_child:
            right_child = self._update_offsets(node.right_child)
            if right_child.stop_offset_low < stop_offset_low:
                stop_offset_low = right_child.stop_offset_low
            if stop_offset_high < right_child.stop_offset_high:
                stop_offset_high = right_child.stop_offset_high
        node._stop_offset_low = stop_offset_low
        node._stop_offset_high = stop_offset_high
        return node

    def _get_format_specification(self):
        values = []
        logical_ties = [x for x in self]
        if logical_ties:
            values.append(logical_ties)
        names = []
        return system.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=names,
        )

    ### PUBLIC METHODS ###

    def find_logical_ties_starting_at(self, offset):
        results = []
        node = self._search(self._root_node, offset)
        if node is not None:
            results.extend(node.payload)
        return tuple(results)

    def find_logical_ties_stopping_at(self, offset):
        def recurse(node, offset):
            result = []
            if node is not None:
                if node.stop_offset_low <= offset <= node.stop_offset_high:
                    for logical_tie in node.payload:
                        if inspect(logical_tie).timespan().stop_offset == offset:
                            result.append(logical_tie)
                    if node.left_child is not None:
                        result.extend(recurse(node.left_child, offset))
                    if node.right_child is not None:
                        result.extend(recurse(node.right_child, offset))
            return result

        results = recurse(self._root_node, offset)
        results.sort(
            key=lambda x: (
                inspect(x).timespan().start_offset,
                inspect(x).timespan().stop_offset,
            )
        )
        return tuple(results)

    def find_logical_ties_overlapping_offset(self, offset):
        r"""Finds logical_ties overlapping `offset`.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> for x in logical_tie_collection.find_logical_ties_overlapping_offset(1.5):
            ...     x
            ...
            LogicalTie(start_offset=Offset(0, 1), stop_offset=Offset(3, 1))
            LogicalTie(start_offset=Offset(1, 1), stop_offset=Offset(2, 1))
            LogicalTie(start_offset=Offset(1, 1), stop_offset=Offset(3, 1))

        Returns tuple of 0 or more logical_ties.
        """

        def recurse(node, offset, indent=0):
            result = []
            if node is not None:
                if node.start_offset < offset < node.stop_offset_high:
                    result.extend(recurse(node.left_child, offset, indent + 1))
                    for logical_tie in node.payload:
                        if offset < inspect(logical_tie).timespan().stop_offset:
                            result.append(logical_tie)
                    result.extend(recurse(node.right_child, offset, indent + 1))
                elif offset <= node.start_offset:
                    result.extend(recurse(node.left_child, offset, indent + 1))
            return result

        results = recurse(self._root_node, offset)
        results.sort(
            key=lambda x: (
                inspect(x).timespan().start_offset,
                inspect(x).timespan().stop_offset,
            )
        )
        return tuple(results)

    def find_logical_ties_intersecting_timespan(self, timespan):
        r"""Finds logical_ties overlapping `timespan`.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> timespan = abjad.Timespan(2, 4)
            >>> for x in logical_tie_collection.find_logical_ties_intersecting_logical_tie(timespan):
            ...     x
            ...
            LogicalTie(start_offset=Offset(0, 1), stop_offset=Offset(3, 1))
            LogicalTie(start_offset=Offset(1, 1), stop_offset=Offset(3, 1))
            LogicalTie(start_offset=Offset(2, 1), stop_offset=Offset(5, 1))

        Returns tuple of 0 or more logical_ties.
        """

        def recurse(node, timespan):
            result = []
            if node is not None:
                if timespan.intersects_timespan(node):
                    result.extend(recurse(node.left_child, timespan))
                    for candidate_logical_tie in node.payload:
                        if (
                            inspect(candidate_logical_tie)
                            .timespan()
                            .intersects_timespan(timespan)
                        ):
                            result.append(candidate_logical_tie)
                    result.extend(recurse(node.right_child, timespan))
                elif (timespan.start_offset <= node.start_offset) or (
                    timespan.stop_offset <= node.start_offset
                ):
                    result.extend(recurse(node.left_child, timespan))
            return result

        results = recurse(self._root_node, timespan)
        results.sort(
            key=lambda x: (
                inspect(x).timespan().start_offset,
                inspect(x).timespan().stop_offset,
            )
        )
        return tuple(results)
#new from greg...spotty when to check node vs timespan? What even is in the node?
    def find_logical_ties_starting_during_timespan(self, timespan):
        def recurse(node, timespan):
            result = []
            if node is not None:
                if timespan.intersects_timespan(node):
                    result.extend(recurse(node.left_child, timespan))
                    for candidate_logical_tie in node.payload:
                        if (
                            inspect(candidate_logical_tie)
                            .timespan()
                            .starts_during_timespan(timespan)
                        ):
                            result.append(candidate_logical_tie)
                    result.extend(recurse(node.right_child, timespan))
                elif (timespan.start_offset <= node.start_offset) or (
                    timespan.stop_offset <= node.start_offset
                ):
                    result.extend(recurse(node.left_child, timespan))
            return result

        results = recurse(self._root_node, timespan)
        results.sort(
            key=lambda x: (
                inspect(x).timespan().start_offset,
                inspect(x).timespan().stop_offset,
            )
        )
        print(tuple(results))
        return tuple(results)

    def get_simultaneity_at(self, offset):
        r"""Gets simultaneity at `offset`.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> logical_tie_collection.get_simultaneity_at(1)
            <logical_tiesimultaneity(1 <<3>>)>

        ::

            >>> logical_tie_collection.get_simultaneity_at(6.5)
            <logical_tiesimultaneity(6.5 <<1>>)>

        """
        import evans.consort_reviv

        start_logical_ties = self.find_logical_ties_starting_at(offset)
        stop_logical_ties = self.find_logical_ties_stopping_at(offset)
        overlap_logical_ties = self.find_logical_ties_overlapping_offset(offset)
        simultaneity = evans.consort_reviv.logical_tiesimultaneity(
            logical_tie_collection=self,
            overlap_logical_ties=overlap_logical_ties,
            start_logical_ties=start_logical_ties,
            start_offset=offset,
            stop_logical_ties=stop_logical_ties,
        )
        return simultaneity

    def get_start_offset_after(self, offset):
        r"""Gets start offst in this logical_tie collection after `offset`.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> logical_tie_collection.get_start_offset_after(-1)
            Offset(0, 1)

        ::

            >>> logical_tie_collection.get_start_offset_after(0)
            Offset(1, 1)

        ::

            >>> logical_tie_collection.get_start_offset_after(1)
            Offset(2, 1)

        ::

            >>> logical_tie_collection.get_start_offset_after(2)
            Offset(6, 1)

        ::

            >>> logical_tie_collection.get_start_offset_after(6) is None
            True

        """

        def recurse(node, offset):
            if node is None:
                return None
            result = None
            if node.start_offset <= offset and node.right_child:
                result = recurse(node.right_child, offset)
            elif offset < node.start_offset:
                result = recurse(node.left_child, offset) or node
            return result

        result = recurse(self._root_node, offset)
        if result is None:
            return None
        return result.start_offset

    def get_start_offset_before(self, offset):
        r"""Gets start offst in this logical_tie collection before `offset`.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> logical_tie_collection.get_start_offset_before(7)
            Offset(6, 1)

        ::

            >>> logical_tie_collection.get_start_offset_before(6)
            Offset(2, 1)

        ::

            >>> logical_tie_collection.get_start_offset_before(2)
            Offset(1, 1)

        ::

            >>> logical_tie_collection.get_start_offset_before(1)
            Offset(0, 1)

        ::

            >>> logical_tie_collection.get_start_offset_before(0) is None
            True

        """

        def recurse(node, offset):
            if node is None:
                return None
            result = None
            if node.start_offset < offset:
                result = recurse(node.right_child, offset) or node
            elif offset <= node.start_offset and node.left_child:
                result = recurse(node.left_child, offset)
            return result

        result = recurse(self._root_node, offset)
        if result is None:
            return None
        return result.start_offset

    def index(self, logical_tie):
        assert self._is_logical_tie(logical_tie)
        node = self._search(
            self._root_node, inspect(logical_tie).timespan().start_offset
        )
        if node is None or logical_tie not in node.payload:
            raise ValueError("{} not in logical_tie collection.".format(logical_tie))
        index = node.payload.index(logical_tie) + node.node_start_index
        return index

    def insert(self, logical_ties):
        r"""Inserts `logical_ties` into this logical_tie collection.

        ::

            >>> logical_tie_collection = consort.LogicalTieCollection()
            >>> logical_tie_collection.insert(abjad.LogicalTie(1, 3))
            >>> logical_tie_collection.insert((
            ...     abjad.LogicalTie(0, 4),
            ...     abjad.LogicalTie(2, 6),
            ...     ))

        ::

            >>> for x in logical_tie_collection:
            ...     x
            ...
            LogicalTie(start_offset=Offset(0, 1), stop_offset=Offset(4, 1))
            LogicalTie(start_offset=Offset(1, 1), stop_offset=Offset(3, 1))
            LogicalTie(start_offset=Offset(2, 1), stop_offset=Offset(6, 1))

        `logical_ties` may be a single logical_tie or an iterable of logical_ties.

        Returns none.
        """
        if self._is_logical_tie(logical_ties):
            logical_ties = [logical_ties]
        for logical_tie in logical_ties:
            if not self._is_logical_tie(logical_tie):
                continue
            self._insert_logical_tie(logical_tie)
        self._update_indices(self._root_node)
        self._update_offsets(self._root_node)

    def iterate_simultaneities(self, reverse=False):
        r"""Iterates simultaneities in this logical_tie collection.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> for x in logical_tie_collection.iterate_simultaneities():
            ...     x
            ...
            <logical_tiesimultaneity(0 <<1>>)>
            <logical_tiesimultaneity(1 <<3>>)>
            <logical_tiesimultaneity(2 <<3>>)>
            <logical_tiesimultaneity(6 <<1>>)>

        ::

            >>> for x in logical_tie_collection.iterate_simultaneities(
            ...     reverse=True):
            ...     x
            ...
            <logical_tiesimultaneity(6 <<1>>)>
            <logical_tiesimultaneity(2 <<3>>)>
            <logical_tiesimultaneity(1 <<3>>)>
            <logical_tiesimultaneity(0 <<1>>)>

        Returns generator.
        """

        if reverse:
            start_offset = self.latest_start_offset
            simultaneity = self.get_simultaneity_at(start_offset)
            yield simultaneity
            simultaneity = simultaneity.previous_simultaneity
            while simultaneity is not None:
                yield simultaneity
                simultaneity = simultaneity.previous_simultaneity
        else:
            start_offset = self.earliest_start_offset
            simultaneity = self.get_simultaneity_at(start_offset)
            yield simultaneity
            simultaneity = simultaneity.next_simultaneity
            while simultaneity is not None:
                yield simultaneity
                simultaneity = simultaneity.next_simultaneity

    def iterate_simultaneities_nwise(self, n=3, reverse=False):
        r"""Iterates simultaneities in this logical_tie collection in groups of
        `n`.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> for x in logical_tie_collection.iterate_simultaneities_nwise(n=2):
            ...     x
            ...
            (<logical_tiesimultaneity(0 <<1>>)>, <logical_tiesimultaneity(1 <<3>>)>)
            (<logical_tiesimultaneity(1 <<3>>)>, <logical_tiesimultaneity(2 <<3>>)>)
            (<logical_tiesimultaneity(2 <<3>>)>, <logical_tiesimultaneity(6 <<1>>)>)

        ::

            >>> for x in logical_tie_collection.iterate_simultaneities_nwise(
            ...     n=2, reverse=True):
            ...     x
            ...
            (<logical_tiesimultaneity(2 <<3>>)>, <logical_tiesimultaneity(6 <<1>>)>)
            (<logical_tiesimultaneity(1 <<3>>)>, <logical_tiesimultaneity(2 <<3>>)>)
            (<logical_tiesimultaneity(0 <<1>>)>, <logical_tiesimultaneity(1 <<3>>)>)

        Returns generator.
        """
        n = int(n)
        assert 0 < n
        if reverse:
            for simultaneity in self.iterate_simultaneities(reverse=True):
                simultaneities = [simultaneity]
                while len(simultaneities) < n:
                    next_simultaneity = simultaneities[-1].next_simultaneity
                    if next_simultaneity is None:
                        break
                    simultaneities.append(next_simultaneity)
                if len(simultaneities) == n:
                    yield tuple(simultaneities)
        else:
            for simultaneity in self.iterate_simultaneities():
                simultaneities = [simultaneity]
                while len(simultaneities) < n:
                    previous_simultaneity = simultaneities[-1].previous_simultaneity
                    if previous_simultaneity is None:
                        break
                    simultaneities.append(previous_simultaneity)
                if len(simultaneities) == n:
                    yield tuple(reversed(simultaneities))

    def remove(self, logical_ties):
        r"""Removes logical_ties from this logical_tie collection.

        ::

            >>> logical_ties = (
            ...     abjad.LogicalTie(0, 3),
            ...     abjad.LogicalTie(1, 3),
            ...     abjad.LogicalTie(1, 2),
            ...     abjad.LogicalTie(2, 5),
            ...     abjad.LogicalTie(6, 9),
            ...     )
            >>> logical_tie_collection = consort.LogicalTieCollection(logical_ties)

        ::

            >>> logical_tie_collection.remove(logical_ties[1:-1])

        ::

            >>> for logical_tie in logical_tie_collection:
            ...     logical_tie
            ...
            LogicalTie(start_offset=Offset(0, 1), stop_offset=Offset(3, 1))
            LogicalTie(start_offset=Offset(6, 1), stop_offset=Offset(9, 1))

        """
        if self._is_logical_tie(logical_ties):
            logical_ties = [logical_ties]
        for logical_tie in logical_ties:
            if not self._is_logical_tie(logical_tie):
                continue
            self._remove_logical_tie(logical_tie)
        self._update_indices(self._root_node)
        self._update_offsets(self._root_node)

    ### PUBLIC PROPERTIES ###

    @property
    def all_offsets(self):
        offsets = set()
        for logical_tie in self:
            offsets.add(inspect(logical_tie).timespan().start_offset)
            offsets.add(inspect(logical_tie).timespan().stop_offset)
        return tuple(sorted(offsets))

    @property
    def all_start_offsets(self):
        start_offsets = set()
        for logical_tie in self:
            start_offsets.add(inspect(logical_tie).timespan().start_offset)
        return tuple(sorted(start_offsets))

    @property
    def all_stop_offsets(self):
        stop_offsets = set()
        for logical_tie in self:
            stop_offsets.add(inspect(logical_tie).timespan().stop_offset)
        return tuple(sorted(stop_offsets))

    @property
    def earliest_start_offset(self):
        def recurse(node):
            if node.left_child is not None:
                return recurse(node.left_child)
            return node.start_offset

        if self._root_node is not None:
            return recurse(self._root_node)
        return float("-inf")

    @property
    def earliest_stop_offset(self):
        if self._root_node is not None:
            return self._root_node.stop_offset_low
        return float("inf")

    @property
    def latest_start_offset(self):
        def recurse(node):
            if node.right_child is not None:
                return recurse(node._right_child)
            return node.start_offset

        if self._root_node is not None:
            return recurse(self._root_node)
        return float("-inf")

    @property
    def latest_stop_offset(self):
        if self._root_node is not None:
            return self._root_node.stop_offset_high
        return float("inf")

    @property
    def start_offset(self):
        return self.earliest_start_offset

    @property
    def stop_offset(self):
        return self.latest_stop_offset
