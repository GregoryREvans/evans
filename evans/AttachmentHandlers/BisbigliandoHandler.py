import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class BisbigliandoHandler:
    def __init__(
        self,
        fingering_list=[None,],
        boolean_vector=[1],
        padding=2,
        staff_padding=2,
        right_padding=2,
        continuous=True,
        bis_count=-1,
        bool_count=-1,
        name="Bisbigliando Handler",
    ):
        self._bis_count = bis_count
        self._bool_count = bool_count
        self.continuous = continuous
        self.padding = padding
        self.staff_padding = staff_padding
        self.right_padding = right_padding
        self.fingering_list = CyclicList(fingering_list, self.continuous, self._bis_count)
        self.boolean_vector = CyclicList(boolean_vector, self.continuous, self._bool_count)
        self.name = name

    def __call__(self, selections):
        self.add_spanner(selections)

    def add_spanner(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        values = self.boolean_vector(r=len(ties))
        for value, tie in zip(values, ties):
            if value == 1:
                fingering = self.fingering_list(r=1)[0]
                if fingering is None:
                    start_literal = abjad.LilyPondLiteral(
                        [
                            r"""- \tweak padding""" + f""" #{self.padding}""",
                            r"""- \tweak staff-padding""" + f""" #{self.staff_padding}""",
                            r"""- \tweak bound-details.right.padding""" + f""" #{self.right_padding}""",
                            r"""- \tweak bound-details.left.text""",
                            r"""\markup{ \raise #1 \teeny \musicglyph #"scripts.halfopenvertical" }""",
                        	r"""\startTrillSpan""",
                        ],
                        format_slot="after",
                    )
                    stop_literal = abjad.LilyPondLiteral(
                        r"\stopTrillSpan",
                        format_slot="after"
                    )
                    abjad.attach(start_literal, tie[0])
                    abjad.attach(stop_literal, abjad.inspect(tie[-1]).leaf(1))
                else:
                    start_literal_pre = abjad.LilyPondLiteral(
                        [
                            r"""- \tweak padding""" + f""" #{self.padding}""",
                            r"""- \tweak staff-padding""" + f""" #{self.staff_padding}""",
                            r"""- \tweak bound-details.right.padding""" + f""" #{self.right_padding}""",
                            r"""- \tweak bound-details.left.text""",
                        ],
                        format_slot="after"
                    )
                    start_literal = abjad.LilyPondLiteral(fingering, format_slot="after")
                    start_literal_post = abjad.LilyPondLiteral(
                        [
                            r"""\startTrillSpan""",
                        ],
                        format_slot="after"
                    )
                    stop_literal = abjad.LilyPondLiteral(
                        r"\stopTrillSpan",
                        format_slot="after"
                    )
                    abjad.attach(start_literal_pre, tie[0])
                    abjad.attach(start_literal, tie[0])
                    abjad.attach(start_literal_post, tie[0])
                    abjad.attach(stop_literal, abjad.inspect(tie[-1]).leaf(1))

    def name(self):
        return self.name

    def state(self):
        return f"""count\n{self.boolean_vector.state()}"""

# ###demo###
# s = abjad.Staff("c''4 c''4 c''4 c''4")
# m = [
#         r"\markup {",
#         r"\lower #1.5",
#         r"\override #'(graphical . #t)",
#         r"\override #'(size . 0.4)",
#         r"\override #'(thickness . 0.25)",
#         r"\woodwind-diagram",
#         r"#'flute",
#         r"#'((cc . (one two three four five six)) (lh . (bes b gis)) (rh . (bes d dis ees cis c gz)))",
#         r"}",
#     ]
# handler = BisbigliandoHandler(
#     fingering_list=[None, m],
#     boolean_vector=[1],
#     staff_padding=2,
#     continuous=True,
# )
# handler(s[:-1])
# abjad.f(s)
