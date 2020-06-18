# -*- coding: utf-8 -*-
from evans.consort_reviv.AbjadObject import AbjadObject


class AbjadValueObject(AbjadObject):
    r"""Abstract base class for classes which compare equally based on their
    storage format.
    """

    # ### CLASS VARIABLES ###

    __slots__ = ()

    # ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        r"""Copies Abjad value object.
        Returns new Abjad value object.
        """
        from abjad.top import new

        return new(self)

    def __eq__(self, argument):
        r"""Is true when all initialization values of Abjad value object equal
        the initialization values of `argument`.
        Returns true or false.
        """
        from abjad import system

        return system.TestManager.compare_objects(self, argument)

    def __hash__(self):
        r"""Hashes Abjad value object.
        Returns integer.
        """
        from abjad import system

        hash_values = format.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            message = "unhashable type: {}".format(self)
            raise TypeError(message)
        return result
