from fractions import Fraction

import abjad
from evans.AttachmentHandlers.TextSpanHandler import TextSpanHandler

handler = TextSpanHandler(
    span_one_positions=["1/4", "2/4", "3/4"],
    span_one_style="solid-line",
    span_one_padding=1.4,
    attach_span_one_to="leaves",
    continuous=True,
)
staff = abjad.Staff("c'4 c'4 c'4 c'4")
handler(staff[0:3])
abjad.f(staff)
