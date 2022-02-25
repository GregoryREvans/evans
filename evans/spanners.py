import abjad


class DurationLine:  # don't forget to force notehead shape

    ### CLASS VARIABLES ###

    __slots__ = "_tweaks"

    _format_slot = "after"

    _time_orientation = abjad.enums.Right

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        tweaks: abjad.TweakInterface = None,
    ):
        if tweaks is not None:
            assert isinstance(tweaks, abjad.TweakInterface), repr(tweaks)
        self._tweaks = abjad.TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return f"<{type(self).__name__}()>"

    def __str__(self):
        return r"\-"

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.articulations.extend(tweaks)
        bundle.after.articulations.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def tweaks(self):
        return self._tweaks
