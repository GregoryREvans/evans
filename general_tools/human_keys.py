import re


def to_digit(string):
    return int(string) if string.isdigit() else string


def human_sorted_keys(text):
    return [to_digit(_) for _ in re.split(r"(\d+)", text)]


###DEMO###
# import abjad

# alist=[
#     "voice 1",
#     "voice 12",
#     "voice 17",
#     "voice 2",
#     "voice 25",
#     "voice 29"]
#
# anotherlist=[
#     "1 Flute",
#     "2 Violin",
#     "3 Bass",]

# timespans = [abjad.AnnotatedTimespan(annotation=f'Voice {x + 6}',  start_offset=(0, 1), stop_offset=(1, 1)) for x in range(5)]
# timespan_list = abjad.TimespanList()
# for x in timespans:
#     timespan_list.append(x)
# timespan_list.append(abjad.AnnotatedTimespan(annotation='Voice 1',  start_offset=(0, 1), stop_offset=(1, 1)))
#
# abjad.f(timespan_list)

# abjad.show(timespan_list, key='annotation')

# alist.sort(key=human_sorted_keys)
# anotherlist.sort(key=human_sorted_keys)
# print(alist)
# print(anotherlist)
