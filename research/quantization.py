import evans

nested_list = [1, [[1, [1, 1]], 1, [1, [1, 1, 1]], [1, [1, 1]], 1]]
# rtm = evans.nested_list_to_rtm(nested_list)
flat = evans.flatten(nested_list)

rtm = "(1 ((1 (2 3)) 4 (3 (2 1 2)) (3 (4 3)) 2))"
rotations = []
for i in range(len(evans.flatten(nested_list))):
    new_rtm = evans.rotate_tree(rtm, i)
    rotations.append(new_rtm)

funnels = []
for rotation in rotations:
    funnel = evans.funnel_inner_tree_to_x(rtm_string=rotation, x=6)
    funnels.append(funnel)

index_cycle = evans.cyc([i for i in range(len(funnels[0]))])
tuple_list = []
for i in range(len(rotations)):
    tuple_ = (i, next(index_cycle))
    tuple_list.append(tuple_)

final_rtm_list = []
for tuple_ in tuple_list:
    a = tuple_[0]
    b = tuple_[-1]
    final_rtm_list.append(funnels[a][b])

final_rtm_list = evans.Sequence(final_rtm_list).rotate(1)

for _ in final_rtm_list:
    print(_)

quantizer = evans.RhythmTreeQuantizer()
final_rtm_list = [quantizer(_) for _ in final_rtm_list]

print("")

for _ in final_rtm_list:
    print(_)
