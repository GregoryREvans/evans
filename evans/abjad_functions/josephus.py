def josephus(n, k):
    p, i, seq = list(range(n)), 0, []
    while p:
        i = (i+k-1) % len(p)
        seq.append(p.pop(i))
    sequences = [list(range(n))]
    for _ in seq:
        next = [x for x in sequences[-1]]
        next.remove(_)
        sequences.append(next)
    return sequences[:-1]

# tone_row = [0, 1, 3, 8, 2, 5, 9, 7, 4, 11, 10, 6]
#
# for i in range(16):
#     print(
#         josephus(len(tone_row), i + 2)
#     )
#
# print(
#     josephus(len(tone_row), 2)
# )
