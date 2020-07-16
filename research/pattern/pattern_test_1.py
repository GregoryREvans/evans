import abjad

#
# pattern = abjad.Pattern(
#     indices=[0, 1, 7],
#     period=8,
#     )
#
# total_length = 16
# for index in range(16):
#     match = pattern.matches_index(index, total_length)
#     match = match or ''
#     print(index, match)
#
# ###
#
# pattern_1 = abjad.index_first(3)
# pattern_2 = abjad.index_last(3)
# pattern = pattern_1 & pattern_2
# abjad.lilypond(pattern)
#
# ###
#
# pattern_1 = abjad.index_first(3)
# pattern_2 = abjad.index_last(3)
# pattern_3 = abjad.index([0], 2)
# pattern = pattern_1 & pattern_2 & pattern_3
# abjad.lilypond(pattern)
#
# ###
#
# pattern_1 = abjad.index_first(3)
# pattern_2 = abjad.index_last(3)
# pattern_3 = abjad.index([0], 2)
# pattern = pattern_1 & pattern_2 | pattern_3
# abjad.lilypond(pattern)
#
# ###
#
# pattern = abjad.index_first(3)
# abjad.lilypond(pattern)
#
# pattern = ~pattern
# abjad.lilypond(pattern)
#
# ###
#
# pattern_1 = abjad.index_first(3)
# pattern_2 = abjad.index_last(3)
# pattern = pattern_1 | pattern_2
# abjad.lilypond(pattern)
#
# ###
#
# pattern_1 = abjad.index_first(3)
# pattern_2 = abjad.index_last(3)
# pattern = pattern_1 | pattern_2
# abjad.lilypond(pattern)
#
# ###
#
# pattern_1 = abjad.index_first(3)
# pattern_2 = abjad.index_last(3)
# pattern_3 = abjad.index([0], 2)
# pattern = pattern_1 | pattern_2 | pattern_3
# abjad.lilypond(pattern)
#
# ###
#
# pattern_1 = abjad.index_first(3)
# pattern_2 = abjad.index_last(3)
# pattern_3 = abjad.index([0], 2)
# pattern = pattern_1 | pattern_2 & pattern_3
# abjad.lilypond(pattern)
#
# ###
#
# pattern_1 = abjad.index_first(3)
# pattern_2 = abjad.index_last(3)
# pattern = pattern_1 ^ pattern_2
# abjad.lilypond(pattern)
#
# ###
#
# pattern_1 = abjad.index_first(3)
# pattern_2 = abjad.index_last(3)
# pattern_3 = abjad.index([0], 2)
# pattern = pattern_1 ^ pattern_2 ^ pattern_3
# abjad.lilypond(pattern)
#
# ###
#
# pattern_1 = abjad.index_first(3)
# pattern_2 = abjad.index_last(3)
# pattern_3 = abjad.index([0], 2)
# pattern = pattern_1 ^ pattern_2 & pattern_3
# abjad.lilypond(pattern)
#
# ###
#
# pattern = abjad.Pattern(
#     indices=[4, 5, 6, 7],
#     )
# pattern.get_boolean_vector(16)
#
# ###
#
# pattern = abjad.Pattern(
#     indices=[4, 5, 6, 7],
#     )
# pattern.get_matching_items('abcdefghijklmnopqrstuvwxyz')
#
# ###
#
# pattern = abjad.Pattern(
#     indices=[0, 1, 7],
#     period=8,
#     )
# pattern = pattern.rotate(n=2)
# abjad.lilypond(pattern)
#
# ###
#
# pattern = [1, 0, 0, 1, 1]
# pattern = abjad.Pattern.from_vector(pattern)
# abjad.lilypond(pattern)
#
# ###
#
# pattern = abjad.Pattern(
#     indices=[0, 1, 7],
#     payload='Allegro non troppo',
#     period=8,
#     )
# total_length = 10
# for index in range(10):
#     match = pattern.matches_index(index, total_length)
#     if match:
#         payload = pattern.payload
#     else:
#         payload = ''
#     print(index, repr(payload))

# ##

pattern = abjad.Pattern(indices=[2, 3, 6], payload="Allegro non troppo", period=8)

total_length = 10
for index in range(10):
    match = pattern.matches_index(index, total_length)
    if match:
        payload = pattern.payload
    else:
        payload = ""
    print(index, repr(payload))
