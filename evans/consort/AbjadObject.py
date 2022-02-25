import abjad
import black


class AbjadObject:
    # ### CLASS VARIABLES ###

    __slots__ = ()

    # ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r"""Is true when ID of `argument` equals ID of Abjad object.
        Otherwise false.
        Returns true or false.
        """
        return id(self) == id(argument)

    def __format__(self, format_specification=""):
        r"""Formats Abjad object.
        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.
        Returns string.
        """

        if format_specification in ("", "storage"):
            string = str(self)
            string = black.format_str(string, mode=black.mode.Mode())
            return string
        return str(self)

    def __getstate__(self):
        r"""Gets state of Abjad object.
        Returns dictionary.
        """
        if hasattr(self, "__dict__") and hasattr(vars(self), "copy"):
            state = vars(self).copy()
        else:
            state = {}
        for class_ in type(self).__mro__:
            for slot in getattr(class_, "__slots__", ()):
                try:
                    state[slot] = getattr(self, slot)
                except AttributeError:
                    pass
        return state

    def __hash__(self):
        r"""Hashes Abjad object.
        Required to be explicitly redefined on Python 3 if __eq__ changes.
        Returns integer.
        """
        return super(AbjadObject, self).__hash__()

    def __ne__(self, argument):
        r"""Is true when Abjad object does not equal `argument`.
        Otherwise false.
        Returns true or false.
        """
        return not self == argument

    def __repr__(self):
        r"""Gets interpreter representation of Abjad object.
        Returns string.
        """

        return f"<{type(self).__name__}()>"

    def __str__(self):
        return f"<{type(self).__name__}()>"

    def __setstate__(self, state):
        r"""Sets state of Abjad object.
        Returns none.
        """
        for key, value in state.items():
            setattr(self, key, value)

    # ### PRIVATE METHODS ###

    def _debug(self, value, annotation=None, blank=False):
        if annotation is None:
            print("debug: {!r}".format(value))
        else:
            print("debug ({}): {!r}".format(annotation, value))
        if blank:
            print()

    def _debug_values(self, values, annotation=None, blank=True):
        if values:
            for value in values:
                self._debug(value, annotation=annotation)
            if blank:
                print()
        else:
            self._debug(repr(values), annotation=annotation)
            if blank:
                print()

    def _get_format_specification(self):

        return abjad.FormatSpecification()
