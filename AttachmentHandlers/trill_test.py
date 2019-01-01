import abjad
from TrillHandler import TrillHandler
#
# staff = abjad.Staff([
#     abjad.Note(6, (1, 8)),
#     abjad.Chord([3, 0, 1], abjad.Duration(1, 8)),
#     abjad.Note(1, (1, 4)),
#     abjad.Note(2, (1, 2)),
#     abjad.Chord([5, 8], (1, 2)),
#     abjad.Note(3, (1, 4))
# ])
trill_handler = TrillHandler()
# # print(format(staff))
# trill_handler(staff)
# # print(format(staff))
# # abjad.show(staff)
#
#
#
# lm = abjad.LeafMaker()
# pitches = [9, [10, 2], None, 1, None, [5, 6], 0, 11, [7, 8]]
# durations = [(n, 8) for n in [2, 3, 1, 2, 1, 3, 1, 2, 4]]
# leaves = lm(pitches, durations)
# staff = abjad.Staff()
# staff.append(leaves)
# # print(format(staff))
# trill_handler(staff)
# # print(format(staff))
# # abjad.show(staff)

staff = abjad.Staff(r'<a b>1 ~ <a b>4 \times 2/3 { a8 a8 <a b>8 } a4 a \times 2/3 { b8 a b }')
score = abjad.Score([staff])
trill_handler(score)
# print(format(score))
abjad.show(score)
