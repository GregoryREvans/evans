import abjad

ts_list = abjad.TimespanList()
spans = [abjad.AnnotatedTimespan(0, 2, 'hello'), abjad.AnnotatedTimespan(0, 2, 'world'),]
for _ in spans:
    ts_list.append(_)
location = [abjad.Offset(1), ]
ts_list.split_at_offsets(location)
#annotation is preserved through splitting!
