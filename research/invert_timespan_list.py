import abjad

total_duration = abjad.Timespan(0, 7)
timespans = [abjad.Timespan(*_) for _ in [(1, 2), (2, 3), (4, 5)]]
timespans = abjad.TimespanList(timespans)
print(abjad.storage(timespans))
print()

result = abjad.TimespanList()
result.append(total_duration)
for timespan in timespans:
    result -= timespan
print(abjad.storage(result))
