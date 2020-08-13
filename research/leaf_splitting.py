import abjad

ts_list = abjad.TimespanList()
spans = [
    abjad.AnnotatedTimespan(0, (1, 8), "hello"),
    abjad.AnnotatedTimespan((1, 8), (1, 4), "world"),
]
print(spans)
for _ in spans:
    ts_list.append(_)
print(ts_list)
durations = [timespan.duration for timespan in ts_list]
print(durations)

staff = abjad.Staff("c'4")
print(abjad.lilypond(staff))
leaves = staff[:]

abjad.mutate.split(leaves, durations, tie_split_notes=False)

print(abjad.lilypond(staff))
