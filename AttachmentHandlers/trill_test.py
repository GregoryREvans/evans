import abjad
from TrillHandler import TrillHandler

staff = abjad.Staff([abjad.Chord([0, 3], abjad.Duration(1, 4))])

TrillHandler(staff)

abjad.show(staff)
