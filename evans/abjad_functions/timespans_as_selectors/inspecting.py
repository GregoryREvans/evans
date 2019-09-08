import abjad

staff = abjad.Staff(""" c'4 ~ c'16 """)
ties = abjad.select(staff).logical_ties(pitched=True)
tie = ties[0]
leaf = tie[0]
span = abjad.Timespan(start_offset=0, stop_offset=(1, 4))

print("span")
abjad.f(span)
print("tie")
abjad.f(leaf._get_timespan().stop_offset)
