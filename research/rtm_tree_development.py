import evans

demo_tree = evans.RTMTree([1, [2, [1, 2, 3]], 3, [4, [1, [2, [1, 2]], 3]]])


# print(demo_tree.list_format())
# print(demo_tree.insert_at_index(index=0, level=3, insertion=evans.RTMNode(9)).list_format())

# print(demo_tree.list_format())
# print(demo_tree.pop_at_index(index=0, level=1, with_children=True).list_format())

print(demo_tree.list_format())
tree_1 = demo_tree.random_funnel(
    indices=[0, 3, 7],
    allowable_levels=[1, 2],
    ranges=[(1, 9), (1, 6), (3, 7)],
    targets=[4, 5, 2],
    allowable_classes=None,
    random_seed=0,
)
tree_2 = tree_1.random_funnel(
    indices=[0, 3, 7],
    allowable_levels=[1, 2],
    ranges=[(1, 9), (1, 6), (3, 7)],
    targets=[4, 5, 2],
    allowable_classes=None,
    random_seed=1,
)

tree_3 = tree_2.random_funnel(
    indices=[0, 3, 7],
    allowable_levels=[1, 2],
    ranges=[(1, 9), (1, 6), (3, 7)],
    targets=[4, 5, 2],
    allowable_classes=None,
    random_seed=2,
)
tree_4 = tree_3.random_funnel(
    indices=[0, 3, 7],
    allowable_levels=[1, 2, 3],
    ranges=[(1, 9), (1, 6), (3, 7)],
    targets=[4, 5, 6],
    allowable_classes=None,
    random_seed=3,
)
print(tree_1.list_format())
print(tree_2.list_format())
print(tree_3.list_format())
print(tree_4.list_format())
