import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class TempoSpannerHandler:
    def __init__(
        self,
        tempo_list=[(3, 0, 1, "87"), (3, 0, 1, "95")],
        boolean_vector=[1],
        staff_padding=2,
        continuous=True,
        tempo_count=-1,
        bool_count=-1,
        name="Tempo Spanner Handler",
    ):
        self._tempo_count = tempo_count
        self._bool_count = bool_count
        self.continuous = continuous
        self.staff_padding = staff_padding
        self.tempo_list = CyclicList(tempo_list, self.continuous, self._tempo_count)
        self.boolean_vector = CyclicList(boolean_vector, self.continuous, self._bool_count)
        self.name = name

    def __call__(self, selections):
        self.add_spanner(selections)

    def add_spanner(self, selections):
        ties = abjad.select(selections).logical_ties()
        value = self.boolean_vector(r=1)[0]
        if value == 1:
            start_temp = self.tempo_list(r=1)[0]
            stop_temp = self.tempo_list(r=1)[0]
            start_literal = abjad.LilyPondLiteral(
                [
                    r"- \abjad-dashed-line-with-arrow",
                    r"- \baca-metronome-mark-spanner-left-text " + f"{start_temp[0]} {start_temp[1]} {start_temp[2]} \"{start_temp[3]}\"",
                    r"- \tweak staff-padding #" + f"{self.staff_padding}",
                    r"\bacaStartTextSpanMM",
                ],
                format_slot="after",
            )
            stop_literal = abjad.LilyPondLiteral(
                [
                    r"\bacaStopTextSpanMM",
                    r"- \abjad-invisible-line",
                    r"- \baca-metronome-mark-spanner-left-text " + f"{stop_temp[0]} {stop_temp[1]} {stop_temp[2]} \"{stop_temp[3]}\"",
                    r"- \tweak staff-padding #" + f"{self.staff_padding}",
                    r"\bacaStartTextSpanMM",
                ],
                format_slot="after",
            )
            stopper = abjad.LilyPondLiteral(
                r"\bacaStopTextSpanMM",
                format_slot="after",
                )
            abjad.attach(
                start_literal,
                abjad.select(ties).leaves()[0]
                )
            abjad.attach(
                stop_literal,
                abjad.select(ties).leaves()[-1]
                )
            abjad.attach(
                stopper,
                abjad.inspect(abjad.select(ties).leaves()[-1]).leaf(1)
                )

    def name(self):
        return self.name

    def state(self):
        return f"""count\n{self.boolean_vector.state()}"""

# ###demo###
# s = abjad.Staff("s4 s4 s4 s4")
# handler = TempoSpannerHandler()
# handler(s[:-1])
# abjad.f(s)
