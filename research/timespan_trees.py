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
abjad.show(demotree_list, scale=0.7)
