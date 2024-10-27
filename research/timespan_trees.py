import abjad
import tsmakers

a = tsmakers.TimespanTreeNode(30)
proportions = [3, 2, 1, 4, 5, 1, 4]

for prop in proportions:
    a.insert_child(prop)

for child in a.children:
    for prop in proportions:
        child.insert_child(prop)


demotree = tsmakers.TimespanTree(a)

demotree_list = demotree.tspanlist()

# demotree_list = demotree_list.round_offsets(
#     abjad.Duration((1, 8)),
#     anchor=abjad.Left,
# )
# illustration = abjad.illustrate(demotree_list)
# file = abjad.LilyPondFile(
#     items=[
#         """#(set-default-paper-size "11x17landscape")""",
#         illustration,
#     ],
# )
# # print(illiustration)
# abjad.show(file, scale=3)

total_time = 0
total = 30
time = 30 * 60
for child in demotree.get_level(2):
    # print(f"{child.get_timespan().duration}\n")
    duration = child.get_timespan().duration
    derived_clock_time = (duration * time) / total
    total_time += derived_clock_time
    print(float(derived_clock_time))
    print("")

# print("")
# print(total_time / 60)
